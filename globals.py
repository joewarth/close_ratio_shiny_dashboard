# globals.py

# Libraries ===================================================================
from pathlib import Path
import pandas as pd

# Parameters ==================================================================
param_raw_data_dir = Path("data/raw_data.csv")

# Import / process data =======================================================
quote_data = pd.read_csv(
  param_raw_data_dir
)

quote_data.columns = quote_data.columns.str.lower()

# Field List ==================================================================
FIELD_CHOICES = {
  "": "<None>",
  "quote_id": "Quote ID",
  "agency": "Agency Name",
  "issued": "Issued Indicator",
  "quote_platform": "Quote Platform",
  "eff_date": "Effective Date",
  "liab_only": "Liability Only Indicator",
  "st": "State",
  "zipcode": "Zip Code",
  "terr": "Territory",
  "min_veh_yr": "Minimum Vehicle Year",
  "max_veh_yr": "Maximum Vehicle Year",
  "multiproduct_discount": "Multi-Product Discount Indicator",
  "life_discount": "Life Discount Indicator",
  "multicar": "Multi-Car Discount Indicator",
  "acc_viol_score": "Accident/Violation Score",
  "ins_score": "Insurance Score",
  "bi_limit": "CSL/BI Limit",
  "driver1_age": "Driver 1 Age",
  "driver2_age": "Driver 2 Age",
}

# Identify numeric fields =====================================================
NUMERIC_FIELDS = [
    col
    for col in quote_data.columns
    if pd.api.types.is_numeric_dtype(quote_data[col])
]