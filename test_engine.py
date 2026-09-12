"""Integration test for HAQX statutory engine and PDF generation."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
# Prevent Streamlit from auto-running
import unittest.mock
with unittest.mock.patch.dict('os.environ', {'STREAMLIT_SERVER_HEADLESS': 'true'}):
    from app import (
        CitizenProfile, evaluate_all_schemes, GAZETTE_ENTRIES,
        generate_pdf_dossier, EvaluationResult
    )
print(f"Gazette entries: {len(GAZETTE_ENTRIES)}")
# Test case 1: Disabled rural BPL male, age 55
cp1 = CitizenProfile(
    full_name="Ramesh Patel",
    age=55,
    gender="male",
    disability_percentage=80,
    disability_types=["Locomotor"],
    annual_income=40000,
    monthly_household_income=3333,
