"""
ML Model Feature Documentation
Real Credit Risk Model - 32 features
Accuracy: 83.9% | ROC-AUC: 0.867
"""

# Model Features (32 total)
MODEL_FEATURES = [
    'year',
    'loan_limit',
    'Gender',
    'approv_in_adv',
    'loan_type',
    'loan_purpose',
    'Credit_Worthiness',
    'open_credit',
    'business_or_commercial',
    'loan_amount',
    'rate_of_interest',
    'Interest_rate_spread',
    'Upfront_charges',
    'term',
    'Neg_ammortization',
    'interest_only',
    'lump_sum_payment',
    'property_value',
    'construction_type',
    'occupancy_type',
    'Secured_by',
    'total_units',
    'income',
    'credit_type',
    'Credit_Score',
    'co-applicant_credit_type',
    'age',
    'submission_of_application',
    'LTV',
    'Region',
    'Security_Type',
    'dtir1'
]

# Feature Categories
NUMERIC_FEATURES = [
    'year',
    'loan_amount',
    'rate_of_interest',
    'Interest_rate_spread',
    'Upfront_charges',
    'term',
    'property_value',
    'total_units',
    'income',
    'Credit_Score',
    'age',
    'LTV',
    'dtir1'
]

CATEGORICAL_FEATURES = [
    'loan_limit',
    'Gender',
    'approv_in_adv',
    'loan_type',
    'loan_purpose',
    'Credit_Worthiness',
    'open_credit',
    'business_or_commercial',
    'Neg_ammortization',
    'interest_only',
    'lump_sum_payment',
    'construction_type',
    'occupancy_type',
    'Secured_by',
    'credit_type',
    'co-applicant_credit_type',
    'submission_of_application',
    'Region',
    'Security_Type'
]

# Feature Descriptions
FEATURE_DESCRIPTIONS = {
    'year': 'Year of application',
    'loan_limit': 'Loan limit category',
    'Gender': 'Applicant gender',
    'approv_in_adv': 'Pre-approval status',
    'loan_type': 'Type of loan',
    'loan_purpose': 'Purpose of loan',
    'Credit_Worthiness': 'Credit worthiness rating',
    'open_credit': 'Open credit lines',
    'business_or_commercial': 'Business or commercial type',
    'loan_amount': 'Loan amount in currency',
    'rate_of_interest': 'Interest rate (%)',
    'Interest_rate_spread': 'Interest rate spread',
    'Upfront_charges': 'Upfront charges',
    'term': 'Loan term in months',
    'Neg_ammortization': 'Negative amortization flag',
    'interest_only': 'Interest-only flag',
    'lump_sum_payment': 'Lump sum payment flag',
    'property_value': 'Property value',
    'construction_type': 'Type of construction',
    'occupancy_type': 'Type of occupancy',
    'Secured_by': 'Security type',
    'total_units': 'Total units',
    'income': 'Annual income',
    'credit_type': 'Credit type',
    'Credit_Score': 'Credit score (300-900)',
    'co-applicant_credit_type': 'Co-applicant credit type',
    'age': 'Age in years',
    'submission_of_application': 'Application submission type',
    'LTV': 'Loan-to-Value ratio',
    'Region': 'Geographic region',
    'Security_Type': 'Type of security',
    'dtir1': 'Debt-to-Income ratio'
}

# Feature Value Ranges (for validation)
FEATURE_RANGES = {
    'age': (18, 100),
    'Credit_Score': (300, 900),
    'income': (0, 1000000),
    'loan_amount': (0, 5000000),
    'LTV': (0, 200),
    'dtir1': (0, 100),
    'term': (12, 480),
    'rate_of_interest': (0, 20),
}

# Model Performance
MODEL_PERFORMANCE = {
    'accuracy': 0.839,
    'roc_auc': 0.867,
    'precision': 0.82,
    'recall': 0.85,
    'f1_score': 0.835,
    'default_rate': 0.246,
}

print("✓ ML Model Features Loaded")
print(f"  Total Features: {len(MODEL_FEATURES)}")
print(f"  Numeric: {len(NUMERIC_FEATURES)}")
print(f"  Categorical: {len(CATEGORICAL_FEATURES)}")
print(f"  Accuracy: {MODEL_PERFORMANCE['accuracy']*100:.1f}%")
print(f"  ROC-AUC: {MODEL_PERFORMANCE['roc_auc']:.3f}")
