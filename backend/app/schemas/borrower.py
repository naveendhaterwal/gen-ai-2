"""
Borrower Schema - Data model for loan applicant information.
Uses Pydantic for validation and documentation.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional


class BorrowerInput(BaseModel):
    """
    Input schema - what we receive from the frontend form.
    All fields are validated automatically.
    """
    
    # Personal Info
    full_name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=18, le=70)
    
    # Financial Info
    monthly_income: float = Field(..., gt=0, description="Monthly income in rupees")
    employment_type: str = Field(
        ..., 
        description="Employment type: Salaried, Self-Employed, Business"
    )
    
    # Credit Info
    credit_score: int = Field(..., ge=300, le=900)
    existing_loan_amount: float = Field(default=0, ge=0)
    existing_emi_monthly: float = Field(default=0, ge=0)
    
    # Loan Details
    loan_amount_requested: float = Field(..., gt=0)
    loan_purpose: str = Field(
        ..., 
        description="Home, Auto, Personal, Business"
    )
    loan_tenure_months: int = Field(default=60, ge=12, le=360)
    
    class Config:
        """Example data for API documentation"""
        json_schema_extra = {
            "example": {
                "full_name": "Rajesh Kumar",
                "age": 35,
                "monthly_income": 50000,
                "employment_type": "Salaried",
                "credit_score": 720,
                "existing_loan_amount": 200000,
                "existing_emi_monthly": 5000,
                "loan_amount_requested": 500000,
                "loan_purpose": "Home",
                "loan_tenure_months": 120
            }
        }
    
    @validator("employment_type")
    def validate_employment_type(cls, v):
        """Check employment type is valid"""
        valid_types = ["Salaried", "Self-Employed", "Business"]
        if v not in valid_types:
            raise ValueError(f"Must be one of {valid_types}")
        return v
    
    @validator("loan_purpose")
    def validate_loan_purpose(cls, v):
        """Check loan purpose is valid"""
        valid_purposes = ["Home", "Auto", "Personal", "Business"]
        if v not in valid_purposes:
            raise ValueError(f"Must be one of {valid_purposes}")
        return v


class BorrowerProfile(BaseModel):
    """
    Enriched borrower profile with calculated fields.
    Used internally in the system.
    """
    
    # From input
    full_name: str
    age: int
    monthly_income: float
    employment_type: str
    credit_score: int
    existing_loan_amount: float
    existing_emi_monthly: float
    loan_amount_requested: float
    loan_purpose: str
    loan_tenure_months: int
    
    # Calculated fields
    foir: float = Field(..., description="Fixed Obligation to Income Ratio")
    dti: float = Field(..., description="Debt-to-Income Ratio")
    proposed_emi: float = Field(..., description="Proposed EMI for new loan")
    total_emi_after_loan: float = Field(..., description="Total EMI including new loan")
    
    class Config:
        """Allows computed fields"""
        from_attributes = True
