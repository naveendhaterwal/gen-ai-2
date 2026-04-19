"""
Machine Learning Service
Loads and uses the credit risk prediction model.
"""

import joblib
import logging
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, List, Dict, Any

from app.core.config import settings
from app.schemas.borrower import BorrowerProfile

logger = logging.getLogger(__name__)


class MLService:
    """
    Service for ML model predictions.
    Loads the model once and reuses it.
    """
    
    def __init__(self):
        """Initialize the service - load model on startup"""
        self.model = None
        self.feature_columns: List[str] = []
        self.model_loaded = False
        self.use_fallback = False
        self._load_model()
    
    def _load_model(self):
        """Load the ML model from disk"""
        try:
            model_path = Path(settings.ML_MODEL_PATH)
            feature_path = Path(settings.FEATURE_COLUMNS_PATH)
            
            if not model_path.exists():
                logger.warning(f"Model not found at {model_path}. Switching to rule-based fallback.")
                self.use_fallback = True
                return

            if not feature_path.exists():
                logger.warning(f"Feature columns not found at {feature_path}. Switching to rule-based fallback.")
                self.use_fallback = True
                return
            
            # Load the trained model
            self.model = joblib.load(model_path)
            self.feature_columns = joblib.load(feature_path)
            self.model_loaded = True
            logger.info(f"Loaded ML model from {model_path}")
            logger.info(f"Loaded {len(self.feature_columns)} feature columns")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}. Enabling rule-based fallback.")
            self.model = None
            self.feature_columns = []
            self.model_loaded = False
            self.use_fallback = True

    def _map_age_bucket(self, age: int) -> str:
        """Map numeric age to bucket labels typically used in credit datasets."""
        if age < 25:
            return "<25"
        if age < 35:
            return "25-34"
        if age < 45:
            return "35-44"
        if age < 55:
            return "45-54"
        if age < 65:
            return "55-64"
        if age < 75:
            return "65-74"
        return ">74"

    def _loan_purpose_to_model(self, purpose: str) -> str:
        """Map app loan purpose to dataset categories."""
        purpose_map = {
            "Home": "p1",
            "Auto": "p2",
            "Personal": "p3",
            "Business": "p4",
        }
        return purpose_map.get(purpose, "p3")

    def _build_model_input(self, borrower: BorrowerProfile) -> pd.DataFrame:
        """Build a one-row DataFrame aligned to the trained model feature columns."""
        if not self.feature_columns:
            raise ValueError("Feature columns are not loaded")

        # Start with NaN so the model's imputers can fill missing values.
        row = {col: np.nan for col in self.feature_columns}

        # Numeric values from borrower profile.
        row["income"] = float(borrower.monthly_income * 12)
        row["loan_amount"] = float(borrower.loan_amount_requested)
        row["Credit_Score"] = int(borrower.credit_score)
        row["dtir1"] = float(max(0.0, min(100.0, borrower.dti * 100.0)))
        row["LTV"] = 80.0
        row["term"] = int(borrower.loan_tenure_months)

        # Categorical values mapped to model vocabulary used in training UI.
        row["loan_purpose"] = self._loan_purpose_to_model(borrower.loan_purpose)
        row["Credit_Worthiness"] = "l1" if borrower.credit_score >= 700 else "l2"
        row["open_credit"] = "opc" if borrower.existing_loan_amount > 0 else "nopc"
        row["interest_only"] = "not_int"
        row["loan_limit"] = "cf"
        row["business_or_commercial"] = "ob/c" if borrower.loan_purpose == "Business" else "nob/c"
        row["occupancy_type"] = "pr"
        row["age"] = self._map_age_bucket(borrower.age)

        # Defaults for remaining categorical fields from common mortgage dataset values.
        row["year"] = 2019
        row["Gender"] = "Sex Not Available"
        row["approv_in_adv"] = "nopre"
        row["loan_type"] = "type1"
        row["rate_of_interest"] = 8.5
        row["Interest_rate_spread"] = 0.0
        row["Upfront_charges"] = 0.0
        row["Neg_ammortization"] = "not_neg"
        row["lump_sum_payment"] = "not_lpsm"
        row["property_value"] = float(borrower.loan_amount_requested / 0.8) if borrower.loan_amount_requested > 0 else 0.0
        row["construction_type"] = "sb"
        row["Secured_by"] = "home"
        row["total_units"] = "1U"
        row["credit_type"] = "EXP"
        row["co-applicant_credit_type"] = "CIB"
        row["submission_of_application"] = "to_inst"
        row["Region"] = "south"
        row["Security_Type"] = "direct"

        ordered_row = {col: row.get(col, np.nan) for col in self.feature_columns}
        return pd.DataFrame([ordered_row])
    
    def _prepare_features(self, borrower: BorrowerProfile) -> pd.DataFrame:
        """Prepare borrower data for the saved sklearn pipeline."""
        return self._build_model_input(borrower)
    
    def predict_risk(self, borrower: BorrowerProfile) -> Tuple[str, float, float, Dict[str, Any]]:
        """
        Predict credit risk using a hybrid model (40% ML + 60% Rule-based).
        Ensures sensitivity to risk even if the ML model is biased.
        """
        
        try:
            # 1. Calculate Rule-Based Score (Standard for manual/deterministic logic)
            rule_level, rule_score, rule_conf, rule_breakdown = self._predict_fallback(borrower)
            
            # 2. Calculate ML Model Score (if available)
            ml_score = 0.0
            ml_prob = 0.0
            ml_available = False
            ml_details = {}

            if not self.use_fallback and self.model_loaded:
                # Prepare features
                features = self._prepare_features(borrower)
                
                if hasattr(self.model, "predict_proba"):
                    probabilities = self.model.predict_proba(features)[0]
                    positive_index = int(np.argmax(self.model.classes_ == 1)) if 1 in self.model.classes_ else 1
                    ml_prob = float(probabilities[positive_index])
                    ml_score = round(ml_prob * 100.0, 2)
                    ml_available = True
                    ml_details = {
                        "ml_default_probability": round(ml_prob, 6),
                        "ml_class_probabilities": [round(float(p), 6) for p in probabilities],
                        "ml_classes": [int(c) if isinstance(c, (int, np.integer)) else str(c) for c in self.model.classes_]
                    }

            # 3. Blend Scores (Hybrid Model)
            if ml_available:
                # 40% ML weight, 60% Rule weight
                hybrid_score = (ml_score * 0.4) + (rule_score * 0.6)
                method = "hybrid_model"
            else:
                hybrid_score = rule_score
                method = "rule_based_fallback"

            # 4. Final Interpretations
            risk_score = round(hybrid_score, 2)
            risk_level, _ = self._interpret_prediction(risk_score / 100.0)
            
            # Use ML confidence if available, else fallback confidence
            confidence = 0.85 if ml_available else 0.7

            score_breakdown = {
                "method": method,
                "formula": "risk_score = (ML_score * 0.4) + (Rule_score * 0.6)" if ml_available else "rule_based_fallback",
                "risk_score": risk_score,
                "components": {
                    "ml_model_contribution": round(ml_score * 0.4, 2) if ml_available else 0,
                    "rule_engine_contribution": round(rule_score * 0.6 if ml_available else rule_score, 2),
                    "raw_ml_score": ml_score if ml_available else None,
                    "raw_rule_score": rule_score
                },
                "rule_details": rule_breakdown.get("components", {}),
                **ml_details
            }
            
            logger.info(f"Risk Prediction ({method}): {risk_level} (Score: {risk_score}, Confidence: {confidence})")
            
            return risk_level, risk_score, confidence, score_breakdown
            
        except Exception as e:
            logger.error(f"Error in hybrid prediction: {str(e)}. Falling back to pure rule-based logic.")
            return self._predict_fallback(borrower)
            
    def _predict_fallback(self, borrower: BorrowerProfile) -> Tuple[str, float, float, Dict[str, Any]]:
        """Rule-based risk calculation as a fallback for missing or incompatible ML model."""
        logger.info("Using rule-based risk prediction fallback")
        
        # Base score from Credit Score (higher = better)
        # Convert 300-900 range to 0-100 (inverted for risk)
        base_risk = 100 - ((borrower.credit_score - 300) / 600 * 100)
        
        # Adjust for FOIR (Banks prefer < 40%)
        # FOIR of 0.5 adds significant risk
        foir_penalty = max(0, (borrower.foir - 0.4) * 100)
        
        # Adjust for DTI (Banks prefer < 40%)
        dti_penalty = max(0, (borrower.dti - 0.4) * 50)
        
        # Employment stability
        employment_bonus = -5 if borrower.employment_type == "Salaried" else 5
        
        total_risk = base_risk + foir_penalty + dti_penalty + employment_bonus
        total_risk = max(0, min(100, total_risk))
        
        risk_level, _ = self._interpret_prediction(total_risk / 100.0)
        
        score_breakdown = {
            "method": "rule_based_fallback",
            "formula": "risk = clamp(base_risk + foir_penalty + dti_penalty + employment_adjustment, 0, 100)",
            "strict_no_fallbacks": settings.STRICT_NO_FALLBACKS,
            "components": {
                "base_risk_from_credit_score": round(base_risk, 4),
                "foir_penalty": round(foir_penalty, 4),
                "dti_penalty": round(dti_penalty, 4),
                "employment_adjustment": employment_bonus,
            },
        }

        return risk_level, round(total_risk, 2), 0.7, score_breakdown  # Constant confidence for fallback
    
    def _interpret_prediction(self, prediction: float) -> Tuple[str, float]:
        """
        Convert raw model prediction to risk level and score.
        
        Assumes prediction is between 0-1 where:
        - 0 = Low risk
        - 1 = High risk
        """
        
        # Convert to 0-100 scale
        risk_score = float(prediction * 100)
        
        # Classify into levels
        if risk_score < 40:
            risk_level = "Low"
        elif risk_score < 60:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return risk_level, risk_score


# Global instance - created once and reused
ml_service = MLService()
