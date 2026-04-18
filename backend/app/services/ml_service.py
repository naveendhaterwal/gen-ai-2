"""
Machine Learning Service
Loads and uses the credit risk prediction model.
"""

import joblib
import logging
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, List

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
        self._load_model()
    
    def _load_model(self):
        """Load the ML model from disk"""
        try:
            model_path = Path(settings.ML_MODEL_PATH)
            feature_path = Path(settings.FEATURE_COLUMNS_PATH)
            
            if not model_path.exists():
                raise FileNotFoundError(f"Model not found at {model_path}")

            if not feature_path.exists():
                raise FileNotFoundError(f"Feature columns file not found at {feature_path}")
            
            # Load the trained model
            self.model = joblib.load(model_path)
            self.feature_columns = joblib.load(feature_path)
            self.model_loaded = True
            logger.info(f"Loaded ML model from {model_path}")
            logger.info(f"Loaded {len(self.feature_columns)} feature columns")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            self.model = None
            self.feature_columns = []
            self.model_loaded = False
            raise

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
    
    def predict_risk(self, borrower: BorrowerProfile) -> Tuple[str, float, float]:
        """
        Predict credit risk for a borrower.
        
        Args:
            borrower: BorrowerProfile object
            
        Returns:
            Tuple of (risk_level, risk_score, confidence)
            - risk_level: "Low", "Medium", or "High"
            - risk_score: 0-100
            - confidence: 0-1
        """
        
        try:
            if not self.model_loaded:
                raise RuntimeError("ML model is not loaded. Check model files in backend/models")
            
            # Prepare features
            features = self._prepare_features(borrower)
            
            if not hasattr(self.model, "predict_proba"):
                raise AttributeError("Loaded model does not support predict_proba")

            # Probability of positive class = default risk
            probabilities = self.model.predict_proba(features)[0]
            positive_index = int(np.argmax(self.model.classes_ == 1)) if 1 in self.model.classes_ else 1
            default_probability = float(probabilities[positive_index])

            risk_score = round(default_probability * 100.0, 2)
            confidence = round(float(np.max(probabilities)), 3)
            risk_level, _ = self._interpret_prediction(default_probability)
            
            logger.info(f"Risk Prediction: {risk_level} (Score: {risk_score}, Confidence: {confidence})")
            
            return risk_level, risk_score, confidence
            
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            raise
    
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
