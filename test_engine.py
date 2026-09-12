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
 area="rural",
    is_bpl=True,
    bpl_score=15,
    is_gujarat_domicile=True,
)
r1 = evaluate_all_schemes(cp1, "TEST-001")
print(f"\n=== Test 1: Disabled BPL Rural Male, Age 55, 80% Disability ===")
print(f"Qualified: {r1.total_schemes_qualified}/12")
print(f"Annual cash: INR {r1.total_annual_cash:,.0f}")
print(f"One-time cash: INR {r1.total_one_time_cash:,.0f}")
print(f"Hardware items: {r1.total_hardware_items}")
print(f"Service items: {r1.total_service_items}")
for s in r1.schemes:
    status = "PASS" if s.qualified else "FAIL"
    print(f"  [{status}] {s.scheme_id} — {s.scheme_name}")
    if s.qualified and s.annual_cash_value > 0:
        print(f"         -> INR {s.annual_cash_value:,.0f}/yr")
    if s.qualified and s.one_time_cash_value > 0:
        print(f"         -> INR {s.one_time_cash_value:,.0f} one-time")
    if s.qualified and s.hardware_grants:
        print(f"         -> Hardware: {', '.join(s.hardware_grants)}")
    if s.qualified and s.service_grants:
        print(f"         -> Services: {', '.join(s.service_grants)}")
# Test case 2: Widowed elderly woman
cp2 = CitizenProfile(
    full_name="Sunita Devi",
    age=82,
    gender="female",
    marital_status="widowed",
    disability_percentage=0,
    annual_income=90000,
    monthly_household_income=7500,
    area="rural",
    has_adult_son_over_21=False,
    is_gujarat_domicile=True,
)
r2 = evaluate_all_schemes(cp2, "TEST-002")
print(f"\n=== Test 2: Widowed Elderly Woman, Age 82, No Disability ===")
print(f"Qualified: {r2.total_schemes_qualified}/12")
print(f"Annual cash: INR {r2.total_annual_cash:,.0f}")
for s in r2.schemes:
    status = "PASS" if s.qualified else "FAIL"
    print(f"  [{status}] {s.scheme_id} — {s.scheme_name}")
# Test case 3: Young disabled female student (SC)
cp3 = CitizenProfile(
    full_name="Meena Vaghela",
    age=15,
    gender="female",
    disability_percentage=45,
    disability_types=["Hearing"],
    annual_income=80000,
    monthly_household_income=6666,
    area="rural",
    is_student=True,
    education_standard=10,
    caste_category="SC",
    is_gujarat_domicile=True,
)

r3 = evaluate_all_schemes(cp3, "TEST-003")
print(f"\n=== Test 3: Young Disabled SC Female Student, Age 15, 45% ===")
print(f"Qualified: {r3.total_schemes_qualified}/12")
for s in r3.schemes:
    status = "PASS" if s.qualified else "FAIL"
    print(f"  [{status}] {s.scheme_id} — {s.scheme_name}")
# Test PDF generation
print("\n=== PDF Generation Test ===")
pdf_bytes = generate_pdf_dossier(r1)
print(f"PDF generated: {len(pdf_bytes):,} bytes")
assert len(pdf_bytes) > 1000, "PDF too small"
assert pdf_bytes[:5] == b'%PDF-', "Not a valid PDF"
print("PDF validation: OK")
print("\n✓ ALL TESTS PASSED")
