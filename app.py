"""
HAQX CORE v2.0-Sovereign
Neuro-Symbolic Civic Execution Engine
UN Digital Public Goods Standard · SDG 1.3 · Universal Social Protection Floors
(c) 2026 — Zero-Hallucination Deterministic Statutory Architecture
"""

import streamlit as st
import json
import hashlib
import uuid
import io
import re
import datetime
from typing import List, Optional, Tuple, Dict, Any
from pydantic import BaseModel, Field
import requests
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1: CONFIGURATION & CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

VERSION = "v2.0-Sovereign"
ENGINE_STATUS = "DETERMINISTIC · ZERO-HALLUCINATION"
SDG_BADGE = "SDG 1.3 · Universal Social Protection Floors"
PRIVACY_STATUS = "ZERO-PII RETENTION · SESSION-EPHEMERAL"

OBSIDIAN = "#06080F"
CARBON = "#0F172A"
GUNMETAL = "#1E293B"
SLATE_700 = "#334155"
EMERALD = "#10B981"
EMERALD_DIM = "#065F46"
SOVEREIGN_BLUE = "#2563EB"
BLUE_DIM = "#1E3A5F"
AMBER = "#F59E0B"
AMBER_DIM = "#78350F"
WHITE_PRIMARY = "#F8FAFC"
WHITE_SECONDARY = "#E2E8F0"
MUTED = "#94A3B8"
RED_ALERT = "#EF4444"

GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]

DISABILITY_TYPE_OPTIONS = [
    "Locomotor", "Visual", "Hearing", "Speech & Language",
    "Intellectual", "Autism Spectrum", "Cerebral Palsy",
    "Multiple Disabilities", "Mental Illness", "Chronic Neurological",
    "Blood Disorder (Thalassemia/Hemophilia)", "Acid Attack Survivor",
]

NIRAMAYA_QUALIFYING_TYPES = {"autism spectrum", "cerebral palsy", "intellectual", "multiple disabilities"}

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2: PYDANTIC SCHEMAS
# ══════════════════════════════════════════════════════════════════════════════

class CitizenProfile(BaseModel):
    full_name: str = Field(default="Anonymous Citizen")
    age: int = Field(default=0, ge=0, le=120)
    gender: str = Field(default="male", description="male | female | other")
    marital_status: str = Field(default="unmarried", description="unmarried | married | widowed | divorced")
    is_orphan: bool = Field(default=False)
    disability_percentage: int = Field(default=0, ge=0, le=100)
    disability_types: List[str] = Field(default_factory=list)
    annual_income: float = Field(default=0.0, ge=0)
    monthly_household_income: float = Field(default=0.0, ge=0)
    area: str = Field(default="rural", description="rural | urban")
    state: str = Field(default="Gujarat")
    is_bpl: bool = Field(default=False)
    bpl_score: Optional[int] = Field(default=None, ge=0, le=100)
    has_adult_son_over_21: bool = Field(default=False)
    is_student: bool = Field(default=False)
    education_standard: Optional[int] = Field(default=None, ge=1, le=12)
    caste_category: Optional[str] = Field(default=None, description="SC | ST | OBC | General")
    is_breadwinner_deceased: bool = Field(default=False)
    deceased_breadwinner_age: Optional[int] = Field(default=None, ge=0, le=120)
    is_marriage_registered: bool = Field(default=False)
    spouse_disability_percentage: int = Field(default=0, ge=0, le=100)
    spouse_age: Optional[int] = Field(default=None, ge=0, le=120)
    spouse_gender: Optional[str] = Field(default=None)
    is_gujarat_domicile: bool = Field(default=True)
    has_foster_guardian: bool = Field(default=False)
    guardian_annual_income: Optional[float] = Field(default=None, ge=0)


class SchemeResult(BaseModel):
    scheme_id: str
    scheme_name: str
    administering_body: str
    qualified: bool
    entitlement_type: str = Field(description="cash | hardware | service | composite | one_time_cash")
    annual_cash_value: float = 0.0
    one_time_cash_value: float = 0.0
    monthly_cash_value: float = 0.0
    hardware_grants: List[str] = Field(default_factory=list)
    service_grants: List[str] = Field(default_factory=list)
    legal_citation: str = ""
    required_documents: List[str] = Field(default_factory=list)
    notes: str = ""
    review_flag: bool = False
    disqualification_reasons: List[str] = Field(default_factory=list)


class EvaluationResult(BaseModel):
    citizen: CitizenProfile
    schemes: List[SchemeResult]
    total_annual_cash: float = 0.0
    total_one_time_cash: float = 0.0
    total_schemes_qualified: int = 0
    total_hardware_items: int = 0
    total_service_items: int = 0
    execution_hash: str = ""
    timestamp: str = ""
    session_id: str = ""


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3: GAZETTE KNOWLEDGE BASE DATA
# ══════════════════════════════════════════════════════════════════════════════

GAZETTE_ENTRIES: List[Dict[str, Any]] = [
    {
        "scheme_id": "SSY-GJ-DSD-001",
        "name": "Sant Surdas Yojana",
        "administering_body": "Directorate of Social Defence, Government of Gujarat",
        "gr_number": "GR No. SSD/102018/1137/CH",
        "category": "Disability Pension",
        "target_group": "Persons with Disability (≥60%)",
        "income_cap": "₹47,000/yr (Rural) · ₹68,000/yr (Urban) · BPL Score ≤20",
        "entitlement": "₹1,000/month (₹12,000/yr) via DBT",
        "legal_basis": "Gujarat State Disability Welfare Act; RPwD Act 2016, Section 24",
        "criteria": [
            "Age: 0–79 years",
            "Certified disability ≥ 60%",
            "Rural income ≤ ₹47,000/yr OR Urban income ≤ ₹68,000/yr OR BPL Score ≤ 20",
        ],
    },
    {
        "scheme_id": "ADIP-GOI-MSJE-002",
        "name": "ADIP Scheme (Assistance to Disabled Persons)",
        "administering_body": "Ministry of Social Justice & Empowerment, Government of India",
        "gr_number": "F.No. 19-1/2014-DD-III (GoI MSJE)",
        "category": "Assistive Devices & Hardware",
        "target_group": "Persons with Disability (≥40%)",
        "income_cap": "Monthly household income ≤ ₹30,000",
        "entitlement": "100% free device (≤₹22,500/mo) · 50% subsidy (₹22,501–₹30,000/mo) · Motorized Tricycle (≥80% disability, age ≥16)",
        "legal_basis": "RPwD Act 2016, Section 42; ADIP Scheme Guidelines 2014 (Revised 2022)",
        "criteria": [
            "Certified disability ≥ 40%",
            "Monthly household income ≤ ₹30,000",
            "Motorized Tricycle: disability ≥ 80% AND age ≥ 16",
        ],
    },
    {
        "scheme_id": "GSFA-GJ-WCD-003",
        "name": "Ganga Swarupa Financial Assistance",
        "administering_body": "Women & Child Development Department, Government of Gujarat",
        "gr_number": "GR No. WCD/2019/Widow-Pension/GS",
        "category": "Widow Pension",
        "target_group": "Widowed Women (age ≥ 18)",
        "income_cap": "₹1,20,000/yr (Rural) · ₹1,50,000/yr (Urban)",
        "entitlement": "₹1,250/month (₹15,000/yr) DBT",
        "legal_basis": "Gujarat Widows Welfare Act; National Policy for Women 2016",
        "criteria": [
            "Gender: Female",
            "Marital Status: Widowed",
            "Age ≥ 18",
            "Rural income ≤ ₹1,20,000/yr OR Urban income ≤ ₹1,50,000/yr",
        ],
    },
    {
        "scheme_id": "PMP-GJ-SJE-004",
        "name": "Palak Mata Pita Yojana",
        "administering_body": "Social Justice & Empowerment Department, Government of Gujarat",
        "gr_number": "GR No. SJE/2023/PMP/OrphanWelfare",
        "category": "Orphan Child Development",
        "target_group": "Minor Orphan Children (age < 18)",
        "income_cap": "Guardian annual income ≤ ₹20,00,000",
        "entitlement": "₹4,000/month (₹48,000/yr) child development grant",
        "legal_basis": "Juvenile Justice (Care and Protection of Children) Act 2015; Gujarat State Orphan Welfare Policy",
        "criteria": [
            "Orphan minor child (age < 18)",
            "Surviving foster parents/guardians annual income ≤ ₹20,00,000",
        ],
    },
    {
        "scheme_id": "IGNDPS-GOI-MORD-005",
        "name": "Indira Gandhi National Disability Pension Scheme (IGNDPS)",
        "administering_body": "Ministry of Rural Development, Government of India",
        "gr_number": "NSAP/IGNDPS/2009/MoRD (Revised 2015)",
        "category": "Central Disability Pension",
        "target_group": "Severe Disability (≥80%), BPL",
        "income_cap": "Must hold verified BPL card",
        "entitlement": "₹500/month (₹6,000/yr) central DBT floor",
        "legal_basis": "National Social Assistance Programme (NSAP) Guidelines; RPwD Act 2016",
        "criteria": [
            "Age: 18–79 years",
            "Severe/multiple disability ≥ 80%",
            "Must hold verified BPL card",
        ],
    },
    {
        "scheme_id": "DEDPP-GJ-DSD-006",
        "name": "Destitute Elderly & Disabled Persons Pension",
        "administering_body": "Directorate of Social Defence, Government of Gujarat",
        "gr_number": "GR No. DSD/2020/DEDP/ElderlyDisabled",
        "category": "Elderly / Disability Pension",
        "target_group": "Destitute Elderly (≥60) / Disabled (≥45, ≥75%)",
        "income_cap": "₹1,20,000/yr (Rural) · ₹1,50,000/yr (Urban)",
        "entitlement": "₹1,000/month (₹12,000/yr) · ₹1,250/month (₹15,000/yr) if age ≥ 80",
        "legal_basis": "Maintenance and Welfare of Parents and Senior Citizens Act 2007; Gujarat State Pension Rules",
        "criteria": [
            "(Age ≥ 60 AND no adult son ≥ 21) OR (Age ≥ 45 AND disability ≥ 75%)",
            "Rural income ≤ ₹1,20,000/yr OR Urban income ≤ ₹1,50,000/yr",
        ],
    },
    {
        "scheme_id": "DFTP-GJ-GSRTC-007",
        "name": "Divyang Universal Free Transit Pass",
        "administering_body": "GSRTC & Government of Gujarat",
        "gr_number": "GR No. TRN/2021/GSRTC/DivyangPass",
        "category": "Universal Mobility",
        "target_group": "Persons with Disability (≥40%), Gujarat Domicile",
        "income_cap": "No income restriction",
        "entitlement": "100% free lifetime travel on all GSRTC buses",
        "legal_basis": "RPwD Act 2016, Section 27; Gujarat State Transport Policy",
        "criteria": [
            "Certified disability ≥ 40%",
            "Gujarat state domicile",
        ],
    },
    {
        "scheme_id": "NRMY-GOI-NT-008",
        "name": "Niramaya Health Insurance Scheme",
        "administering_body": "The National Trust & Government of Gujarat",
        "gr_number": "National Trust / Niramaya / 2008 (Revised 2018)",
        "category": "Health Insurance",
        "target_group": "Autism, Cerebral Palsy, Intellectual Disability, Multiple Disabilities",
        "income_cap": "No income restriction",
        "entitlement": "₹1,00,000 annual cashless medical treatment, surgical correction, OPD insurance",
        "legal_basis": "National Trust for Welfare of Persons with Autism, Cerebral Palsy, Mental Retardation and Multiple Disabilities Act 1999",
        "criteria": [
            "Certified: Autism Spectrum, Cerebral Palsy, Intellectual Disability, or Multiple Disabilities",
        ],
    },
    {
        "scheme_id": "DSSY-GJ-ESK-009",
        "name": "Divyang Sadhan Sahay Yojana",
        "administering_body": "e-Samaj Kalyan, Government of Gujarat",
        "gr_number": "GR No. ESK/2020/SadhanSahay/Divyang",
        "category": "Livelihood Equipment",
        "target_group": "Persons with Disability (≥40%), Age 16–60",
        "income_cap": "₹1,20,000/yr (Rural) · ₹1,50,000/yr (Urban)",
        "entitlement": "Free professional equipment kits (sewing machines, orthotic calipers, tricycles)",
        "legal_basis": "RPwD Act 2016, Section 38; Gujarat State Livelihood Support Policy",
        "criteria": [
            "Age: 16–60 years",
            "Certified disability ≥ 40%",
            "Rural income ≤ ₹1,20,000/yr OR Urban income ≤ ₹1,50,000/yr",
        ],
    },
    {
        "scheme_id": "NFBS-GOI-MORD-010",
        "name": "National Family Benefit Scheme (NFBS)",
        "administering_body": "Ministry of Rural Development, Government of India",
        "gr_number": "NSAP/NFBS/1998/MoRD (Revised 2013)",
        "category": "Emergency Bereavement Relief",
        "target_group": "BPL Households with Deceased Breadwinner (18–59)",
        "income_cap": "Annual income ≤ ₹47,000 (BPL)",
        "entitlement": "₹20,000 one-time emergency lump-sum relief",
        "legal_basis": "National Social Assistance Programme (NSAP) Guidelines; National Family Benefit Scheme Rules",
        "criteria": [
            "Household living below poverty line (BPL)",
            "Primary breadwinner deceased, aged 18–59 at time of death",
            "Annual income ≤ ₹47,000",
        ],
    },
    {
        "scheme_id": "SSdY-GJ-SJE-011",
        "name": "Saraswati Sadhana Yojana",
        "administering_body": "Social Justice & Empowerment Department, Government of Gujarat",
        "gr_number": "GR No. SJE/2019/SSdY/SC-OBC-Education",
        "category": "Education Retention",
        "target_group": "Female SC/Low-Income OBC Students (Std 9+)",
        "income_cap": "₹1,20,000/yr (Rural) · ₹1,50,000/yr (Urban)",
        "entitlement": "100% free commuter bicycle for institutional education retention",
        "legal_basis": "Right to Education Act 2009; Gujarat SC/ST Welfare Policy; Gujarat OBC Welfare Act",
        "criteria": [
            "Gender: Female",
            "Enrolled in secondary school (Std 9+)",
            "Caste: Scheduled Caste (SC) or Low-Income OBC",
            "Rural income ≤ ₹1,20,000/yr OR Urban income ≤ ₹1,50,000/yr",
        ],
    },
    {
        "scheme_id": "DSS-GJ-DSD-012",
        "name": "Divyang Shadi Sahay (Marriage Incentive) Yojana",
        "administering_body": "Directorate of Social Defence, Government of Gujarat",
        "gr_number": "GR No. DSD/2021/DSS/MarriageIncentive",
        "category": "Rehabilitation Grant",
        "target_group": "Married Couples (at least one spouse ≥40% disability)",
        "income_cap": "No income restriction",
        "entitlement": "₹50,000 one-time direct financial rehabilitation grant",
        "legal_basis": "RPwD Act 2016, Section 24; Gujarat State Marriage Incentive Policy for PwD",
        "criteria": [
            "Either bride or groom has certified disability ≥ 40%",
            "Marriage legally registered",
            "Bride age ≥ 18; Groom age ≥ 21",
        ],
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4: DETERMINISTIC STATUTORY ENGINE — 12 SCHEME EVALUATORS
# ══════════════════════════════════════════════════════════════════════════════

def _check_rural_urban_income(c: CitizenProfile, rural_cap: float, urban_cap: float) -> Tuple[bool, str]:
    if c.area == "rural" and c.annual_income <= rural_cap:
        return True, ""
    if c.area == "urban" and c.annual_income <= urban_cap:
        return True, ""
    cap = rural_cap if c.area == "rural" else urban_cap
    return False, f"Annual income ₹{c.annual_income:,.0f} exceeds ₹{cap:,.0f} cap for {c.area} area."


def _base_docs() -> List[str]:
    return [
        "Aadhaar Card (linked to bank account for DBT)",
        "Bank Passbook (nationalized bank, DBT-enabled)",
        "Passport-size Photographs (2 copies)",
    ]


def evaluate_sant_surdas(c: CitizenProfile) -> SchemeResult:
    reasons = []
    age_ok = 0 <= c.age <= 79
    if not age_ok:
        reasons.append(f"Age {c.age} outside statutory range 0–79.")
    disability_ok = c.disability_percentage >= 60
    if not disability_ok:
        reasons.append(f"Disability {c.disability_percentage}% below 60% threshold.")
    income_ok = False
    if c.is_bpl and c.bpl_score is not None and c.bpl_score <= 20:
        income_ok = True
    elif c.area == "rural" and c.annual_income <= 47000:
        income_ok = True
    elif c.area == "urban" and c.annual_income <= 68000:
        income_ok = True
    if not income_ok:
        reasons.append(f"Income ₹{c.annual_income:,.0f} exceeds cap (Rural ≤₹47,000 / Urban ≤₹68,000 / BPL Score ≤20).")
    qualified = age_ok and disability_ok and income_ok
    return SchemeResult(
        scheme_id="SSY-GJ-DSD-001",
        scheme_name="Sant Surdas Yojana",
        administering_body="Directorate of Social Defence, Government of Gujarat",
        qualified=qualified,
        entitlement_type="cash",
        annual_cash_value=12000.0 if qualified else 0.0,
        monthly_cash_value=1000.0 if qualified else 0.0,
        legal_citation="GR No. SSD/102018/1137/CH · RPwD Act 2016, Section 24",
        required_documents=_base_docs() + [
            "Disability Certificate (≥60%) issued by Civil Surgeon / District Medical Board",
            "BPL Card or Income Certificate from Mamlatdar / Taluka Development Officer",
            "Domicile Certificate (Gujarat)",
        ],
        notes="Qualified: ₹1,000/month (₹12,000/yr) direct DBT pension." if qualified else "",
        disqualification_reasons=reasons,
    )


def evaluate_adip(c: CitizenProfile) -> SchemeResult:
    reasons = []
    disability_ok = c.disability_percentage >= 40
    if not disability_ok:
        reasons.append(f"Disability {c.disability_percentage}% below 40% threshold.")
    income_ok = c.monthly_household_income <= 30000
    if not income_ok:
        reasons.append(f"Monthly household income ₹{c.monthly_household_income:,.0f} exceeds ₹30,000 cap.")
    qualified = disability_ok and income_ok
    hardware = []
    notes_parts = []
    subsidy_tier = ""
    if qualified:
        if c.monthly_household_income <= 22500:
            subsidy_tier = "100% free assistive device"
            notes_parts.append("Tier A: 100% free assistive device (household income ≤ ₹22,500/mo).")
        else:
            subsidy_tier = "50% subsidized assistive device"
            notes_parts.append("Tier B: 50% subsidized assistive device (household income ₹22,501–₹30,000/mo).")
        if c.disability_percentage >= 80 and c.age >= 16:
            hardware.append("Motorized Tricycle (disability ≥80%, age ≥16)")
            notes_parts.append("Motorized Tricycle: GRANTED (disability ≥80%, age ≥16).")
        else:
            hardware.extend(["Wheelchair", "Manual Tricycle", "Digital Hearing Aid (as applicable)"])
            notes_parts.append("Standard assistive devices: wheelchair, manual tricycle, or digital hearing aid as per clinical assessment.")
    return SchemeResult(
        scheme_id="ADIP-GOI-MSJE-002",
        scheme_name="ADIP Scheme (Assistance to Disabled Persons)",
        administering_body="Ministry of Social Justice & Empowerment, Government of India",
        qualified=qualified,
        entitlement_type="hardware",
        hardware_grants=hardware,
        legal_citation="F.No. 19-1/2014-DD-III · RPwD Act 2016, Section 42 · ADIP Guidelines 2014 (Rev. 2022)",
        required_documents=_base_docs() + [
            "Disability Certificate (≥40%) from District Medical Board",
            "Monthly Household Income Certificate from Revenue Authority",
            "Prescription for assistive device from Rehabilitation Professional",
            "Domicile Certificate",
        ],
        notes=" ".join(notes_parts) if qualified else "",
        disqualification_reasons=reasons,
    )


def evaluate_ganga_swarupa(c: CitizenProfile) -> SchemeResult:
    reasons = []
    gender_ok = c.gender == "female"
    if not gender_ok:
        reasons.append("Applicant is not female.")
    widow_ok = c.marital_status == "widowed"
    if not widow_ok:
        reasons.append(f"Marital status '{c.marital_status}' — must be 'widowed'.")
    age_ok = c.age >= 18
    if not age_ok:
        reasons.append(f"Age {c.age} below minimum 18.")
    income_ok, income_reason = _check_rural_urban_income(c, 120000, 150000)
    if not income_ok:
        reasons.append(income_reason)
    qualified = gender_ok and widow_ok and age_ok and income_ok
    return SchemeResult(
        scheme_id="GSFA-GJ-WCD-003",
        scheme_name="Ganga Swarupa Financial Assistance",
        administering_body="Women & Child Development Department, Government of Gujarat",
        qualified=qualified,
        entitlement_type="cash",
        annual_cash_value=15000.0 if qualified else 0.0,
        monthly_cash_value=1250.0 if qualified else 0.0,
        legal_citation="GR No. WCD/2019/Widow-Pension/GS · National Policy for Women 2016",
        required_documents=_base_docs() + [
            "Husband's Death Certificate",
            "Widow Certificate from Mamlatdar / Competent Authority",
            "Income Certificate (Rural ≤₹1,20,000 / Urban ≤₹1,50,000)",
            "Ration Card",
            "Domicile Certificate (Gujarat)",
        ],
        notes="Qualified: ₹1,250/month (₹15,000/yr) widow pension via DBT." if qualified else "",
        disqualification_reasons=reasons,
    )


def evaluate_palak_mata_pita(c: CitizenProfile) -> SchemeResult:
    reasons = []
    orphan_ok = c.is_orphan
    if not orphan_ok:
        reasons.append("Citizen is not declared as orphan.")
    age_ok = c.age < 18
    if not age_ok:
        reasons.append(f"Age {c.age} — must be minor (< 18).")
    income_ok = True
    if c.guardian_annual_income is not None and c.guardian_annual_income > 2000000:
        income_ok = False
        reasons.append(f"Guardian income ₹{c.guardian_annual_income:,.0f} exceeds ₹20,00,000 cap.")
    elif c.guardian_annual_income is None and not c.has_foster_guardian:
        income_ok = True
    qualified = orphan_ok and age_ok and income_ok
    return SchemeResult(
        scheme_id="PMP-GJ-SJE-004",
        scheme_name="Palak Mata Pita Yojana",
        administering_body="Social Justice & Empowerment Department, Government of Gujarat",
        qualified=qualified,
        entitlement_type="cash",
        annual_cash_value=48000.0 if qualified else 0.0,
        monthly_cash_value=4000.0 if qualified else 0.0,
        legal_citation="GR No. SJE/2023/PMP/OrphanWelfare · JJ Act 2015",
        required_documents=_base_docs() + [
            "Orphan Certificate from District Child Protection Officer (DCPO)",
            "Parents' Death Certificates (both parents)",
            "Foster Guardian Identity & Income Proof (if applicable)",
            "Child's Birth Certificate",
            "School Enrollment Certificate (if school-age)",
        ],
        notes="Qualified: ₹4,000/month (₹48,000/yr) child development grant via DBT." if qualified else "",
        disqualification_reasons=reasons,
    )


def evaluate_igndps(c: CitizenProfile) -> SchemeResult:
    reasons = []
    age_ok = 18 <= c.age <= 79
    if not age_ok:
        reasons.append(f"Age {c.age} outside 18–79 range.")
    disability_ok = c.disability_percentage >= 80
    if not disability_ok:
        reasons.append(f"Disability {c.disability_percentage}% below 80% severe/multiple threshold.")
    bpl_ok = c.is_bpl
    if not bpl_ok:
        reasons.append("Verified BPL card not held.")
    qualified = age_ok and disability_ok and bpl_ok
    return SchemeResult(
        scheme_id="IGNDPS-GOI-MORD-005",
        scheme_name="Indira Gandhi National Disability Pension Scheme (IGNDPS)",
        administering_body="Ministry of Rural Development, Government of India",
        qualified=qualified,
        entitlement_type="cash",
        annual_cash_value=6000.0 if qualified else 0.0,
        monthly_cash_value=500.0 if qualified else 0.0,
        legal_citation="NSAP/IGNDPS/2009/MoRD (Rev. 2015) · RPwD Act 2016",
        required_documents=_base_docs() + [
            "Disability Certificate (≥80%) from District Medical Board",
            "BPL Card (verified by Block/District authority)",
            "Age Proof (Birth Certificate / School Certificate / Aadhaar)",
            "Domicile Certificate",
        ],
        notes="Qualified: ₹500/month (₹6,000/yr) central DBT pension floor." if qualified else "",
        disqualification_reasons=reasons,
    )


def evaluate_destitute_elderly_disabled(c: CitizenProfile) -> SchemeResult:
    reasons = []
    path_a = c.age >= 60 and not c.has_adult_son_over_21
    path_b = c.age >= 45 and c.disability_percentage >= 75
    eligibility_path_ok = path_a or path_b
    if not eligibility_path_ok:
        if c.age < 45:
            reasons.append(f"Age {c.age} below minimum 45 for disability path or 60 for elderly path.")
        elif c.age < 60 and c.disability_percentage < 75:
            reasons.append(f"Age {c.age} with disability {c.disability_percentage}% — needs age ≥60 (no adult son) OR age ≥45 with disability ≥75%.")
        elif c.age >= 60 and c.has_adult_son_over_21:
            reasons.append("Age ≥60 but has adult son ≥21 — does not meet destitution criterion on elderly path.")
    income_ok, income_reason = _check_rural_urban_income(c, 120000, 150000)
    if not income_ok:
        reasons.append(income_reason)
    qualified = eligibility_path_ok and income_ok
    monthly = 0.0
    annual = 0.0
    if qualified:
        if c.age >= 80:
            monthly = 1250.0
            annual = 15000.0
        else:
            monthly = 1000.0
            annual = 12000.0
    return SchemeResult(
        scheme_id="DEDPP-GJ-DSD-006",
        scheme_name="Destitute Elderly & Disabled Persons Pension",
        administering_body="Directorate of Social Defence, Government of Gujarat",
        qualified=qualified,
        entitlement_type="cash",
        annual_cash_value=annual,
        monthly_cash_value=monthly,
        legal_citation="GR No. DSD/2020/DEDP/ElderlyDisabled · Senior Citizens Act 2007",
        required_documents=_base_docs() + [
            "Age Proof (Birth Certificate / School Leaving Certificate)",
            "Income Certificate from Mamlatdar / TDO",
            "Self-Declaration: No adult son ≥21 (if elderly path)",
            "Disability Certificate ≥75% (if disability path)",
            "Domicile Certificate (Gujarat)",
        ],
        notes=f"Qualified: ₹{monthly:,.0f}/month (₹{annual:,.0f}/yr) pension via DBT." + (
            " UPGRADED rate: age ≥80." if c.age >= 80 else "") if qualified else "",
        disqualification_reasons=reasons,
    )


def evaluate_divyang_transit_pass(c: CitizenProfile) -> SchemeResult:
    reasons = []
    disability_ok = c.disability_percentage >= 40
    if not disability_ok:
        reasons.append(f"Disability {c.disability_percentage}% below 40% threshold.")
    domicile_ok = c.is_gujarat_domicile
    if not domicile_ok:
        reasons.append("Not a Gujarat domicile holder.")
    qualified = disability_ok and domicile_ok
    return SchemeResult(
        scheme_id="DFTP-GJ-GSRTC-007",
        scheme_name="Divyang Universal Free Transit Pass",
        administering_body="GSRTC & Government of Gujarat",
        qualified=qualified,
        entitlement_type="service",
        service_grants=["100% Free Lifetime Travel — All GSRTC Buses (City / Express / Gurjarnagari Services)"] if qualified else [],
        legal_citation="GR No. TRN/2021/GSRTC/DivyangPass · RPwD Act 2016, Section 27",
        required_documents=_base_docs() + [
            "Disability Certificate (≥40%) from District Medical Board",
            "Gujarat Domicile Certificate",
            "GSRTC Bus Pass Application Form",
        ],
        notes="Qualified: 100% free lifetime travel on all GSRTC buses." if qualified else "",
        disqualification_reasons=reasons,
    )


def evaluate_niramaya(c: CitizenProfile) -> SchemeResult:
    reasons = []
    citizen_types_lower = {t.lower() for t in c.disability_types}
    has_qualifying_type = bool(citizen_types_lower & NIRAMAYA_QUALIFYING_TYPES)
    if not has_qualifying_type:
        reasons.append(f"Disability types {c.disability_types} do not include Autism, Cerebral Palsy, Intellectual Disability, or Multiple Disabilities.")
    qualified = has_qualifying_type
    return SchemeResult(
        scheme_id="NRMY-GOI-NT-008",
        scheme_name="Niramaya Health Insurance Scheme",
        administering_body="The National Trust & Government of Gujarat",
        qualified=qualified,
        entitlement_type="service",
        service_grants=[
            "₹1,00,000 Annual Cashless Medical Treatment Coverage",
            "Surgical Correction & Therapeutic Interventions",
            "OPD Insurance & Rehabilitation Services",
        ] if qualified else [],
        legal_citation="National Trust Act 1999 · Niramaya Guidelines 2008 (Rev. 2018)",
        required_documents=_base_docs() + [
            "Disability Certificate specifying Autism / Cerebral Palsy / Intellectual Disability / Multiple Disabilities",
            "Registration with National Trust (online at www.thenationaltrust.gov.in)",
            "Niramaya Health Insurance Application Form",
            "Medical Records / Clinical Assessment Report",
        ],
        notes="Qualified: ₹1,00,000/yr cashless medical insurance coverage." if qualified else "",
        disqualification_reasons=reasons,
    )


def evaluate_sadhan_sahay(c: CitizenProfile) -> SchemeResult:
    reasons = []
    age_ok = 16 <= c.age <= 60
    if not age_ok:
        reasons.append(f"Age {c.age} outside 16–60 range.")
    disability_ok = c.disability_percentage >= 40
    if not disability_ok:
        reasons.append(f"Disability {c.disability_percentage}% below 40% threshold.")
    income_ok, income_reason = _check_rural_urban_income(c, 120000, 150000)
    if not income_ok:
        reasons.append(income_reason)
    qualified = age_ok and disability_ok and income_ok
    return SchemeResult(
        scheme_id="DSSY-GJ-ESK-009",
        scheme_name="Divyang Sadhan Sahay Yojana",
        administering_body="e-Samaj Kalyan, Government of Gujarat",
        qualified=qualified,
        entitlement_type="hardware",
        hardware_grants=[
            "Sewing Machine (for self-employment)",
            "Orthotic Calipers (as per clinical need)",
            "Tricycle / Mobility Aid",
        ] if qualified else [],
        legal_citation="GR No. ESK/2020/SadhanSahay/Divyang · RPwD Act 2016, Section 38",
        required_documents=_base_docs() + [
            "Disability Certificate (≥40%) from District Medical Board",
            "Income Certificate (Rural ≤₹1,20,000 / Urban ≤₹1,50,000)",
            "e-Samaj Kalyan Portal Registration (https://esamajkalyan.gujarat.gov.in)",
            "Domicile Certificate (Gujarat)",
            "Self-Employment Plan / Livelihood Proposal (for sewing machine)",
        ],
        notes="Qualified: Free professional equipment kits for livelihood support." if qualified else "",
        disqualification_reasons=reasons,
    )


def evaluate_nfbs(c: CitizenProfile) -> SchemeResult:
    reasons = []
    bpl_ok = c.is_bpl
    if not bpl_ok:
        reasons.append("Household does not hold BPL card.")
    breadwinner_ok = c.is_breadwinner_deceased
    if not breadwinner_ok:
        reasons.append("No primary breadwinner death reported.")
    age_ok = True
    if c.is_breadwinner_deceased and c.deceased_breadwinner_age is not None:
        age_ok = 18 <= c.deceased_breadwinner_age <= 59
        if not age_ok:
            reasons.append(f"Deceased breadwinner age {c.deceased_breadwinner_age} outside 18–59 range.")
    elif c.is_breadwinner_deceased and c.deceased_breadwinner_age is None:
        age_ok = True
    income_ok = c.annual_income <= 47000
    if not income_ok:
        reasons.append(f"Annual income ₹{c.annual_income:,.0f} exceeds ₹47,000 BPL cap.")
    qualified = bpl_ok and breadwinner_ok and age_ok and income_ok
    return SchemeResult(
        scheme_id="NFBS-GOI-MORD-010",
        scheme_name="National Family Benefit Scheme (NFBS)",
        administering_body="Ministry of Rural Development, Government of India",
        qualified=qualified,
        entitlement_type="one_time_cash",
        one_time_cash_value=20000.0 if qualified else 0.0,
        legal_citation="NSAP/NFBS/1998/MoRD (Rev. 2013) · NSAP Guidelines",
        required_documents=_base_docs() + [
            "BPL Card (verified by Block/District authority)",
            "Death Certificate of Primary Breadwinner",
            "FIR / Hospital Records (if accidental death)",
            "Income Certificate (≤₹47,000/yr)",
            "Family Declaration / Ration Card showing household composition",
        ],
        notes="Qualified: ₹20,000 one-time emergency lump-sum relief via DBT." if qualified else "",
        disqualification_reasons=reasons,
    )


def evaluate_saraswati_sadhana(c: CitizenProfile) -> SchemeResult:
    reasons = []
    gender_ok = c.gender == "female"
    if not gender_ok:
        reasons.append("Applicant is not female.")
    student_ok = c.is_student
    if not student_ok:
        reasons.append("Not currently enrolled as a student.")
    std_ok = c.education_standard is not None and c.education_standard >= 9
    if not std_ok:
        reasons.append(f"Education standard {c.education_standard or 'N/A'} — must be Std 9 or above.")
    caste_ok = c.caste_category is not None and c.caste_category.upper() in ("SC", "OBC")
    if not caste_ok:
        reasons.append(f"Caste category '{c.caste_category or 'N/A'}' — must be SC or low-income OBC.")
    income_ok, income_reason = _check_rural_urban_income(c, 120000, 150000)
    if not income_ok:
        reasons.append(income_reason)
    qualified = gender_ok and student_ok and std_ok and caste_ok and income_ok
    return SchemeResult(
        scheme_id="SSdY-GJ-SJE-011",
        scheme_name="Saraswati Sadhana Yojana",
        administering_body="Social Justice & Empowerment Department, Government of Gujarat",
        qualified=qualified,
        entitlement_type="hardware",
        hardware_grants=["Commuter Bicycle (100% free — institutional education retention)"] if qualified else [],
        legal_citation="GR No. SJE/2019/SSdY/SC-OBC-Education · RTE Act 2009 · Gujarat SC/ST Welfare Policy",
        required_documents=_base_docs() + [
            "School Enrollment Certificate (Std 9 or above)",
            "Caste Certificate (SC or OBC) from Competent Authority",
            "Income Certificate (Rural ≤₹1,20,000 / Urban ≤₹1,50,000)",
            "Student ID Card",
            "Domicile Certificate (Gujarat)",
        ],
        notes="Qualified: 100% free commuter bicycle for education retention." if qualified else "",
        disqualification_reasons=reasons,
    )


def evaluate_divyang_shadi_sahay(c: CitizenProfile) -> SchemeResult:
    reasons = []
    marriage_ok = c.is_marriage_registered and c.marital_status == "married"
    if not marriage_ok:
        reasons.append("Marriage not legally registered or marital status not 'married'.")
    disability_ok = c.disability_percentage >= 40 or c.spouse_disability_percentage >= 40
    if not disability_ok:
        reasons.append(f"Neither applicant ({c.disability_percentage}%) nor spouse ({c.spouse_disability_percentage}%) has disability ≥40%.")
    age_ok = True
    if c.gender == "female" and c.age < 18:
        age_ok = False
        reasons.append(f"Female applicant age {c.age} below minimum 18.")
    elif c.gender == "male" and c.age < 21:
        age_ok = False
        reasons.append(f"Male applicant age {c.age} below minimum 21.")
    if c.spouse_age is not None and c.spouse_gender is not None:
        if c.spouse_gender == "female" and c.spouse_age < 18:
            age_ok = False
            reasons.append(f"Female spouse age {c.spouse_age} below minimum 18.")
        elif c.spouse_gender == "male" and c.spouse_age < 21:
            age_ok = False
            reasons.append(f"Male spouse age {c.spouse_age} below minimum 21.")
    qualified = marriage_ok and disability_ok and age_ok
    return SchemeResult(
        scheme_id="DSS-GJ-DSD-012",
        scheme_name="Divyang Shadi Sahay (Marriage Incentive) Yojana",
        administering_body="Directorate of Social Defence, Government of Gujarat",
        qualified=qualified,
        entitlement_type="one_time_cash",
        one_time_cash_value=50000.0 if qualified else 0.0,
        legal_citation="GR No. DSD/2021/DSS/MarriageIncentive · RPwD Act 2016, Section 24",
        required_documents=_base_docs() + [
            "Marriage Registration Certificate",
            "Disability Certificate (≥40%) of bride or groom from District Medical Board",
            "Age Proof of both bride and groom",
            "Joint Photograph of married couple",
            "Domicile Certificate (Gujarat)",
        ],
        notes="Qualified: ₹50,000 one-time rehabilitation grant via DBT." if qualified else "",
        disqualification_reasons=reasons,
    )


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5: MASTER EVALUATION ORCHESTRATOR
# ══════════════════════════════════════════════════════════════════════════════

def evaluate_all_schemes(citizen: CitizenProfile, session_id: str) -> EvaluationResult:
    schemes = [
        evaluate_sant_surdas(citizen),
        evaluate_adip(citizen),
        evaluate_ganga_swarupa(citizen),
        evaluate_palak_mata_pita(citizen),
        evaluate_igndps(citizen),
        evaluate_destitute_elderly_disabled(citizen),
        evaluate_divyang_transit_pass(citizen),
        evaluate_niramaya(citizen),
        evaluate_sadhan_sahay(citizen),
        evaluate_nfbs(citizen),
        evaluate_saraswati_sadhana(citizen),
        evaluate_divyang_shadi_sahay(citizen),
    ]
    total_annual = sum(s.annual_cash_value for s in schemes if s.qualified)
    total_one_time = sum(s.one_time_cash_value for s in schemes if s.qualified)
    total_qualified = sum(1 for s in schemes if s.qualified)
    total_hw = sum(len(s.hardware_grants) for s in schemes if s.qualified)
    total_svc = sum(len(s.service_grants) for s in schemes if s.qualified)
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
    ts = now.strftime("%Y-%m-%dT%H:%M:%S IST")
    hash_input = json.dumps(citizen.model_dump(), sort_keys=True, default=str) + ts + session_id
    exec_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:32].upper()
    return EvaluationResult(
        citizen=citizen,
        schemes=schemes,
        total_annual_cash=total_annual,
        total_one_time_cash=total_one_time,
        total_schemes_qualified=total_qualified,
        total_hardware_items=total_hw,
        total_service_items=total_svc,
        execution_hash=exec_hash,
        timestamp=ts,
        session_id=session_id,
    )


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6: GEMINI NEURAL PARSING PIPELINE
# ══════════════════════════════════════════════════════════════════════════════

GEMINI_SYSTEM_PROMPT = """You are a strict linguistic-to-structured-data parser for the HAQX Indian Government Welfare Eligibility Engine. Your ONLY function is to extract factual demographic and socioeconomic information from a citizen's natural language statement (which may be in Gujarati, Hindi, rural dialect, or broken English) and output a single valid JSON object.

CRITICAL RULES:
1. You must NEVER determine welfare eligibility. You are purely an acoustic/linguistic semantic parser.
2. Output ONLY a raw JSON object. No markdown code fences, no explanation, no conversation, no preamble.
3. Extract ONLY information explicitly stated or directly implied by the citizen's words.
4. For any field not mentioned, use the specified default value.
5. Convert all monetary amounts to annual INR. If someone says "monthly income 5000 rupees", output annual_income as 60000.
6. Interpret Indian number formats: "1.2 lakh" = 120000, "20 lakh" = 2000000.
7. If the citizen mentions a percentage for disability, extract it. If they say "blind" or "cannot walk" without a percentage, estimate based on common Indian UDID certification levels (locomotor disability with immobility = 75-80%, total blindness = 100%, partial hearing loss = 40-60%).

OUTPUT THIS EXACT JSON SCHEMA:
{
    "full_name": "string, default 'Anonymous Citizen'",
    "age": "integer 0-120, default 0",
    "gender": "male | female | other, default 'male'",
    "marital_status": "unmarried | married | widowed | divorced, default 'unmarried'",
    "is_orphan": "boolean, default false",
    "disability_percentage": "integer 0-100, default 0",
    "disability_types": "array of strings from: Locomotor, Visual, Hearing, Speech & Language, Intellectual, Autism Spectrum, Cerebral Palsy, Multiple Disabilities, Mental Illness, Chronic Neurological, Blood Disorder, Acid Attack Survivor. Default empty array []",
    "annual_income": "float >= 0, in INR per year, default 0",
    "monthly_household_income": "float >= 0, in INR per month, default 0",
    "area": "rural | urban, default 'rural'",
    "state": "string, default 'Gujarat'",
    "is_bpl": "boolean, default false",
    "bpl_score": "integer 0-100 or null, default null",
    "has_adult_son_over_21": "boolean, default false",
    "is_student": "boolean, default false",
    "education_standard": "integer 1-12 or null, default null",
    "caste_category": "SC | ST | OBC | General or null, default null",
    "is_breadwinner_deceased": "boolean, default false",
    "deceased_breadwinner_age": "integer or null, default null",
    "is_marriage_registered": "boolean, default false",
    "spouse_disability_percentage": "integer 0-100, default 0",
    "spouse_age": "integer or null, default null",
    "spouse_gender": "male | female | other or null, default null",
    "is_gujarat_domicile": "boolean, default true",
    "has_foster_guardian": "boolean, default false",
    "guardian_annual_income": "float or null, default null"
}"""


def call_gemini_api(text: str, api_key: str) -> Tuple[Optional[Dict], str, str]:
    if not api_key or not api_key.strip():
        return None, "", "No API key provided."
    for model_name in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key.strip()}"
        payload = {
            "systemInstruction": {
                "parts": [{"text": GEMINI_SYSTEM_PROMPT}]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": text}]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.1,
            },
        }
        try:
            resp = requests.post(url, json=payload, timeout=45)
            if resp.status_code == 200:
                body = resp.json()
                candidates = body.get("candidates", [])
                if candidates:
                    content = candidates[0].get("content", {})
                    parts = content.get("parts", [])
                    if parts:
                        raw_text = parts[0].get("text", "")
                        cleaned = raw_text.strip()
                        if cleaned.startswith("```"):
                            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
                            cleaned = re.sub(r"\s*```$", "", cleaned)
                        parsed = json.loads(cleaned)
                        return parsed, model_name, ""
            else:
                error_body = resp.text[:300]
                continue
        except requests.exceptions.Timeout:
            continue
        except json.JSONDecodeError as e:
            continue
        except Exception as e:
            continue
    return None, "", "All Gemini model endpoints exhausted. Please use the manual Symbolic Form Entry."


def parse_citizen_from_gemini(raw_dict: Dict) -> CitizenProfile:
    sanitized = {}
    for field_name in CitizenProfile.model_fields:
        if field_name in raw_dict:
            sanitized[field_name] = raw_dict[field_name]
    return CitizenProfile(**sanitized)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7: REPORTLAB SOVEREIGN DOSSIER SYNTHESIS
# ══════════════════════════════════════════════════════════════════════════════

PDF_OBSIDIAN = HexColor("#0F172A")
PDF_DARK_BLUE = HexColor("#1E293B")
PDF_EMERALD = HexColor("#10B981")
PDF_BLUE = HexColor("#2563EB")
PDF_AMBER = HexColor("#F59E0B")
PDF_WHITE = HexColor("#F8FAFC")
PDF_LIGHT_GRAY = HexColor("#E2E8F0")
PDF_MID_GRAY = HexColor("#94A3B8")


def generate_pdf_dossier(result: EvaluationResult) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        title="HAQX SOVEREIGN STATUTORY CLAIM AUDIT",
        author="HAQX Core v2.0-Sovereign",
    )

    styles = getSampleStyleSheet()

    s_title = ParagraphStyle(
        "HaqxTitle", parent=styles["Title"],
        fontName="Helvetica-Bold", fontSize=18, leading=22,
        textColor=PDF_OBSIDIAN, alignment=TA_CENTER,
        spaceAfter=2 * mm,
    )
    s_subtitle = ParagraphStyle(
        "HaqxSubtitle", parent=styles["Normal"],
        fontName="Helvetica", fontSize=8, leading=10,
        textColor=PDF_MID_GRAY, alignment=TA_CENTER,
        spaceAfter=4 * mm,
    )
    s_section = ParagraphStyle(
        "HaqxSection", parent=styles["Heading2"],
        fontName="Helvetica-Bold", fontSize=11, leading=14,
        textColor=PDF_OBSIDIAN, spaceBefore=6 * mm, spaceAfter=3 * mm,
        borderPadding=(0, 0, 2, 0),
    )
    s_body = ParagraphStyle(
        "HaqxBody", parent=styles["Normal"],
        fontName="Helvetica", fontSize=9, leading=12,
        textColor=black,
    )
    s_mono = ParagraphStyle(
        "HaqxMono", parent=styles["Normal"],
        fontName="Courier", fontSize=7.5, leading=10,
        textColor=PDF_MID_GRAY, alignment=TA_CENTER,
    )
    s_callout = ParagraphStyle(
        "HaqxCallout", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=12, leading=16,
        textColor=PDF_OBSIDIAN, alignment=TA_CENTER,
        spaceBefore=4 * mm, spaceAfter=4 * mm,
    )
    s_small = ParagraphStyle(
        "HaqxSmall", parent=styles["Normal"],
        fontName="Helvetica", fontSize=7.5, leading=10,
        textColor=PDF_MID_GRAY,
    )
    s_check_header = ParagraphStyle(
        "HaqxCheckHeader", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=9.5, leading=12,
        textColor=PDF_OBSIDIAN, spaceBefore=3 * mm, spaceAfter=1.5 * mm,
    )
    s_check_item = ParagraphStyle(
        "HaqxCheckItem", parent=styles["Normal"],
        fontName="Helvetica", fontSize=8.5, leading=11,
        textColor=black, leftIndent=8 * mm,
    )

    flowables = []

    flowables.append(Paragraph("HAQX SOVEREIGN STATUTORY CLAIM AUDIT", s_title))
    flowables.append(Paragraph(
        f"HAQX Core {VERSION} &nbsp;·&nbsp; Deterministic Neuro-Symbolic Engine &nbsp;·&nbsp; "
        f"{SDG_BADGE} &nbsp;·&nbsp; {PRIVACY_STATUS}",
        s_subtitle
    ))

    hash_line = (
        f"EXECUTION HASH: {result.execution_hash} &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"SESSION: {result.session_id} &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"TIMESTAMP: {result.timestamp}"
    )
    flowables.append(Paragraph(hash_line, s_mono))
    flowables.append(Spacer(1, 3 * mm))
    flowables.append(HRFlowable(width="100%", thickness=0.5, color=PDF_LIGHT_GRAY))
    flowables.append(Spacer(1, 4 * mm))

    flowables.append(Paragraph("I. CITIZEN METADATA", s_section))
    c = result.citizen
    meta_data = [
        ["FIELD", "VALUE"],
        ["Full Name / Identifier", c.full_name],
        ["Age", str(c.age)],
        ["Gender", c.gender.capitalize()],
        ["Marital Status", c.marital_status.capitalize()],
        ["Disability Certification", f"{c.disability_percentage}%"],
        ["Disability Types", ", ".join(c.disability_types) if c.disability_types else "None declared"],
        ["Declared Annual Income", f"INR {c.annual_income:,.0f}"],
        ["Monthly Household Income", f"INR {c.monthly_household_income:,.0f}"],
        ["Jurisdiction", f"{c.state} — {c.area.capitalize()} Area"],
        ["BPL Status", f"{'Yes' if c.is_bpl else 'No'}" + (f" (Score: {c.bpl_score})" if c.bpl_score is not None else "")],
        ["Gujarat Domicile", "Yes" if c.is_gujarat_domicile else "No"],
    ]
    meta_table = Table(meta_data, colWidths=[55 * mm, 115 * mm])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PDF_OBSIDIAN),
        ("TEXTCOLOR", (0, 0), (-1, 0), PDF_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("LEADING", (0, 0), (-1, -1), 11),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, PDF_LIGHT_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PDF_WHITE, HexColor("#F1F5F9")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    flowables.append(meta_table)
    flowables.append(Spacer(1, 5 * mm))

    flowables.append(Paragraph("II. STATUTORY ENTITLEMENT AUDIT LEDGER", s_section))
    qualified_schemes = [s for s in result.schemes if s.qualified]
    disqualified_schemes = [s for s in result.schemes if not s.qualified]

    if qualified_schemes:
        ledger_header = ["SCHEME ID", "SCHEME NAME", "ADMINISTERING DIRECTORATE", "ENTITLEMENT"]
        ledger_rows = [ledger_header]
        for s in qualified_schemes:
            entitlement_str = ""
            if s.annual_cash_value > 0:
                entitlement_str = f"INR {s.annual_cash_value:,.0f}/yr (INR {s.monthly_cash_value:,.0f}/mo)"
            elif s.one_time_cash_value > 0:
                entitlement_str = f"INR {s.one_time_cash_value:,.0f} (one-time)"
            if s.hardware_grants:
                hw_str = "; ".join(s.hardware_grants)
                entitlement_str = (entitlement_str + " + " + hw_str) if entitlement_str else hw_str
            if s.service_grants:
                svc_str = "; ".join(s.service_grants[:2])
                entitlement_str = (entitlement_str + " + " + svc_str) if entitlement_str else svc_str
            if not entitlement_str:
                entitlement_str = "See details"
            ledger_rows.append([s.scheme_id, s.scheme_name, s.administering_body, entitlement_str])

        col_w = [30 * mm, 40 * mm, 45 * mm, 55 * mm]
        ledger_table = Table(ledger_rows, colWidths=col_w, repeatRows=1)
        ledger_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PDF_OBSIDIAN),
            ("TEXTCOLOR", (0, 0), (-1, 0), PDF_WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 7),
            ("FONTSIZE", (0, 1), (-1, -1), 7),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("LEADING", (0, 0), (-1, -1), 9.5),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.3, PDF_LIGHT_GRAY),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PDF_WHITE, HexColor("#F1F5F9")]),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ]))
        flowables.append(ledger_table)
    else:
        flowables.append(Paragraph(
            "No statutory entitlements qualified under current citizen profile. "
            "Review input data for accuracy or consult the Gazette Knowledge Base.",
            s_body
        ))

    flowables.append(Spacer(1, 6 * mm))

    callout_data = [
        [Paragraph(
            f"AGGREGATE DIRECT ANNUAL CASH TRANSFER UNLOCKED: INR {result.total_annual_cash:,.0f}/yr"
            + (f" &nbsp;+&nbsp; INR {result.total_one_time_cash:,.0f} ONE-TIME" if result.total_one_time_cash > 0 else ""),
            s_callout
        )],
        [Paragraph(
            f"Total Schemes Qualified: {result.total_schemes_qualified} of 12 &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"Hardware Allocations: {result.total_hardware_items} &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"Service Grants: {result.total_service_items}",
            ParagraphStyle("CalloutSub", parent=s_body, fontSize=9, alignment=TA_CENTER, textColor=PDF_MID_GRAY)
        )]
    ]
    callout_table = Table(callout_data, colWidths=[170 * mm])
    callout_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#ECFDF5")),
        ("BOX", (0, 0), (-1, -1), 1, PDF_EMERALD),
        ("TOPPADDING", (0, 0), (-1, -1), 4 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4 * mm),
        ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
    ]))
    flowables.append(callout_table)
    flowables.append(Spacer(1, 6 * mm))

    if qualified_schemes:
        flowables.append(Paragraph("III. STATUTORY VERIFICATION & NEXT STEPS CHECKLIST", s_section))
        flowables.append(Paragraph(
            "Present this dossier and the following documents to the Taluka Mamlatdar, "
            "District Social Defence Officer, or Taluka Development Officer (TDO) for claim processing.",
            s_body
        ))
        flowables.append(Spacer(1, 3 * mm))

        for s in qualified_schemes:
            flowables.append(Paragraph(
                f"{s.scheme_id} — {s.scheme_name}",
                s_check_header
            ))
            flowables.append(Paragraph(
                f"<i>Authority: {s.administering_body}</i> &nbsp;|&nbsp; <i>Citation: {s.legal_citation}</i>",
                ParagraphStyle("CitationLine", parent=s_small, leftIndent=4 * mm)
            ))
            for req_doc in s.required_documents:
                flowables.append(Paragraph(f"☐ &nbsp;{req_doc}", s_check_item))
            flowables.append(Spacer(1, 2.5 * mm))

    if disqualified_schemes:
        flowables.append(Spacer(1, 3 * mm))
        flowables.append(Paragraph("IV. SCHEMES NOT QUALIFIED (TRANSPARENCY AUDIT)", s_section))
        for s in disqualified_schemes:
            reason_text = "; ".join(s.disqualification_reasons) if s.disqualification_reasons else "Criteria not met."
            flowables.append(Paragraph(
                f"<b>{s.scheme_id} — {s.scheme_name}:</b> {reason_text}",
                ParagraphStyle("DisqualNote", parent=s_body, fontSize=7.5, leading=10, textColor=PDF_MID_GRAY, spaceAfter=1.5 * mm)
            ))

    flowables.append(Spacer(1, 10 * mm))
    flowables.append(HRFlowable(width="100%", thickness=0.3, color=PDF_LIGHT_GRAY))
    flowables.append(Spacer(1, 2 * mm))
    flowables.append(Paragraph(
        f"Generated by HAQX Core {VERSION} — Neuro-Symbolic Civic Execution Engine — "
        f"{SDG_BADGE} — {PRIVACY_STATUS} — "
        f"This document is machine-generated for statutory claim initiation purposes. "
        f"All entitlements are deterministic evaluations of gazetted rules and do not constitute legal advice.",
        ParagraphStyle("Footer", parent=s_small, alignment=TA_CENTER)
    ))

    doc.build(flowables)
    return buf.getvalue()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8: STREAMLIT CUSTOM CSS INJECTION
# ══════════════════════════════════════════════════════════════════════════════

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    :root {
        --obsidian: #06080F;
        --carbon: #0F172A;
        --gunmetal: #1E293B;
        --slate700: #334155;
        --emerald: #10B981;
        --emerald-dim: #065F46;
        --blue: #2563EB;
        --blue-dim: #1E3A5F;
        --amber: #F59E0B;
        --amber-dim: #78350F;
        --white-primary: #F8FAFC;
        --white-secondary: #E2E8F0;
        --muted: #94A3B8;
        --red: #EF4444;
    }

    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background-color: var(--obsidian) !important;
        color: var(--white-primary) !important;
        font-family: 'Inter', 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }

    [data-testid="stHeader"] { background-color: transparent !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stDecoration"] { display: none; }

    [data-testid="stSidebar"] {
        background-color: var(--carbon) !important;
        border-right: 1px solid var(--gunmetal) !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--white-primary) !important;
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
    }

    p, span, div, label {
        color: var(--white-secondary) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--carbon) !important;
        border-radius: 8px !important;
        padding: 4px !important;
        gap: 4px !important;
        border: 1px solid var(--gunmetal) !important;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: var(--muted) !important;
        border-radius: 6px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
        border: none !important;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--gunmetal) !important;
        color: var(--white-primary) !important;
        border: 1px solid var(--slate700) !important;
    }

    .stTabs [data-baseweb="tab-highlight"] { display: none !important; }
    .stTabs [data-baseweb="tab-border"] { display: none !important; }

    [data-testid="stTextInput"] > div > div > input,
    [data-testid="stNumberInput"] > div > div > input,
    .stTextArea textarea,
    .stSelectbox > div > div {
        background-color: var(--carbon) !important;
        color: var(--white-primary) !important;
        border: 1px solid var(--gunmetal) !important;
        border-radius: 6px !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stTextArea textarea:focus,
    [data-testid="stTextInput"] > div > div > input:focus {
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--blue), #1D4ED8) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 10px 24px !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.02em !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8, #1E40AF) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.3) !important;
    }

    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--emerald), var(--emerald-dim)) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
    }

    [data-testid="stExpander"] {
        background-color: var(--carbon) !important;
        border: 1px solid var(--gunmetal) !important;
        border-radius: 8px !important;
    }

    [data-testid="stExpander"] summary {
        color: var(--white-primary) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
    }

    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        border-top: 1px solid var(--gunmetal) !important;
    }

    [data-testid="stMetric"] {
        background-color: var(--carbon) !important;
        border: 1px solid var(--gunmetal) !important;
        border-radius: 10px !important;
        padding: 16px 20px !important;
    }

    [data-testid="stMetric"] label {
        color: var(--muted) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }

    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--emerald) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
    }

    [data-testid="stForm"] {
        background-color: var(--carbon) !important;
        border: 1px solid var(--gunmetal) !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }

    .stRadio > div { flex-direction: row !important; gap: 16px !important; }
    .stRadio label { color: var(--white-secondary) !important; }

    .stCheckbox label span { color: var(--white-secondary) !important; }

    div[data-testid="stJson"] {
        background-color: var(--carbon) !important;
        border: 1px solid var(--gunmetal) !important;
        border-radius: 8px !important;
    }

    hr { border-color: var(--gunmetal) !important; }

    .stSelectbox [data-baseweb="select"] > div {
        background-color: var(--carbon) !important;
        border-color: var(--gunmetal) !important;
    }

    [data-baseweb="popover"] > div {
        background-color: var(--carbon) !important;
        border: 1px solid var(--gunmetal) !important;
    }

    [data-baseweb="menu"] {
        background-color: var(--carbon) !important;
    }

    [data-baseweb="menu"] li {
        color: var(--white-secondary) !important;
    }

    [data-baseweb="menu"] li:hover {
        background-color: var(--gunmetal) !important;
    }

    .stMultiSelect [data-baseweb="tag"] {
        background-color: var(--gunmetal) !important;
        color: var(--white-primary) !important;
    }

    .stAlert { border-radius: 8px !important; }

    code, pre, .stCode {
        font-family: 'JetBrains Mono', monospace !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 9: HUD TELEMETRY BAR
# ══════════════════════════════════════════════════════════════════════════════

def render_hud_bar(session_id: str):
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
    ts = now.strftime("%Y-%m-%d %H:%M IST")
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 10px 24px;
        margin-bottom: 20px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
    ">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.95rem;
                font-weight: 700;
                color: #F8FAFC;
                letter-spacing: 0.05em;
            ">HAQX CORE</span>
            <span style="
                background-color: #065F46;
                color: #10B981;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.6rem;
                font-weight: 600;
                padding: 3px 8px;
                border-radius: 4px;
                letter-spacing: 0.05em;
            ">{VERSION}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
            <span style="
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.6rem;
                color: #10B981;
                display: flex;
                align-items: center;
                gap: 5px;
            ">
                <span style="width:6px;height:6px;border-radius:50%;background:#10B981;display:inline-block;"></span>
                {ENGINE_STATUS}
            </span>
            <span style="
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.6rem;
                color: #94A3B8;
            ">SESSION: {session_id}</span>
            <span style="
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.6rem;
                color: #94A3B8;
            ">{ts}</span>
            <span style="
                background-color: #78350F;
                color: #F59E0B;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.55rem;
                font-weight: 600;
                padding: 2px 7px;
                border-radius: 3px;
            ">ZERO-PII</span>
            <span style="
                background-color: #1E3A5F;
                color: #2563EB;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.55rem;
                font-weight: 600;
                padding: 2px 7px;
                border-radius: 3px;
            ">SDG 1.3</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 10: METRIC CARDS DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

def render_metric_cards(result: EvaluationResult):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(
            label="DIRECT ANNUAL CASH TRANSFER",
            value=f"₹{result.total_annual_cash:,.0f}/yr",
        )
    with c2:
        st.metric(
            label="STATUTORY SCHEMES QUALIFIED",
            value=f"{result.total_schemes_qualified} / 12",
        )
    with c3:
        st.metric(
            label="ASSISTIVE HARDWARE ALLOCATIONS",
            value=str(result.total_hardware_items),
        )
    with c4:
        combined = result.total_service_items
        one_time_label = ""
        if result.total_one_time_cash > 0:
            one_time_label = f" + ₹{result.total_one_time_cash:,.0f} lump"
        st.metric(
            label="MOBILITY / SERVICE GRANTS",
            value=f"{combined} grants{one_time_label}",
        )
    st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 11: TAB 1 — TERMINAL INGESTION
# ══════════════════════════════════════════════════════════════════════════════

def render_ingestion_tab():
    st.markdown("### ⌨ Terminal Ingestion")
    st.markdown(
        "<span style='color:#94A3B8;font-size:0.85rem;'>"
        "Dual-mode citizen data intake. Use Natural Dialect Ingestion for conversational input "
        "via Gemini neural parser, or Fine-Grained Symbolic Form for direct deterministic entry."
        "</span>",
        unsafe_allow_html=True,
    )

    mode = st.radio(
        "Intake Mode",
        ["🧠 Natural Dialect Ingestion (Gemini AI)", "📝 Fine-Grained Symbolic Form Entry"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if mode.startswith("🧠"):
        render_nl_ingestion()
    else:
        render_symbolic_form()


def render_nl_ingestion():
    st.markdown(
        "<div style='background:#0F172A;border:1px solid #1E293B;border-radius:8px;padding:16px;margin:12px 0;'>"
        "<span style='font-family:JetBrains Mono,monospace;font-size:0.75rem;color:#F59E0B;'>"
        "⚡ NEURAL PARSING MODE</span>"
        "<br/><span style='font-size:0.8rem;color:#94A3B8;'>"
        "Speak naturally in any language — Gujarati, Hindi, or English. "
        "The Gemini parser will extract structured citizen data. "
        "The AI does NOT determine eligibility; it only translates language to data.</span></div>",
        unsafe_allow_html=True,
    )

    api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        placeholder="Enter your Gemini API key…",
        help="Get a free key at https://aistudio.google.com/apikey",
    )

    transcript = st.text_area(
        "Citizen Statement / Transcript",
        height=180,
        placeholder=(
            "Example: Maru naam Ramesh che. Hoon 45 varsh no chhu. "
            "Mane 80% locomotor disability che. Maru gaon ma rahe chhe. "
            "Mahine 3000 rupiya kamauu chhu. BPL card che.\n\n"
            "Or in Hindi: Mera naam Sunita hai, umr 62 saal. "
            "Main vidhwa hoon. Gaon mein rehti hoon. Saal ka 90,000 kamaati hoon."
        ),
    )

    if st.button("🔬 Parse with Gemini Neural Engine", use_container_width=True):
        if not transcript.strip():
            st.error("Please enter a citizen statement or transcript.")
            return
        if not api_key.strip():
            st.error("Please provide a Gemini API key, or use the Symbolic Form Entry mode.")
            return

        with st.spinner("Engaging neural parsing pipeline…"):
            raw_dict, model_used, error = call_gemini_api(transcript.strip(), api_key.strip())

        if error:
            st.error(f"Neural parsing failed: {error}")
            return
        if raw_dict is None:
            st.error("Failed to extract structured data from the provided transcript.")
            return

        st.success(f"Parsed successfully via `{model_used}`")

        with st.expander("📦 Raw Gemini Extraction (Intermediate JSON)", expanded=False):
            st.json(raw_dict)

        try:
            citizen = parse_citizen_from_gemini(raw_dict)
        except Exception as e:
            st.error(f"Pydantic validation failed: {e}")
            return

        result = evaluate_all_schemes(citizen, st.session_state.session_id)
        st.session_state.evaluation = result
        st.rerun()


def render_symbolic_form():
    st.markdown(
        "<div style='background:#0F172A;border:1px solid #1E293B;border-radius:8px;padding:16px;margin:12px 0;'>"
        "<span style='font-family:JetBrains Mono,monospace;font-size:0.75rem;color:#2563EB;'>"
        "📋 SYMBOLIC FORM MODE</span>"
        "<br/><span style='font-size:0.8rem;color:#94A3B8;'>"
        "Direct deterministic data entry. No API key required. "
        "Every field maps to a gazetted statutory threshold.</span></div>",
        unsafe_allow_html=True,
    )

    with st.form("symbolic_form", clear_on_submit=False):
        st.markdown("**§ Personal Identity**")
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            full_name = st.text_input("Full Name", value="Anonymous Citizen")
        with fc2:
            age = st.number_input("Age (years)", min_value=0, max_value=120, value=0, step=1)
        with fc3:
            gender = st.selectbox("Gender", ["male", "female", "other"])

        fc4, fc5 = st.columns(2)
        with fc4:
            marital_status = st.selectbox("Marital Status", ["unmarried", "married", "widowed", "divorced"])
        with fc5:
            is_orphan = st.checkbox("Minor Orphan (both parents deceased)")

        st.markdown("---")
        st.markdown("**§ Disability Profile**")
        dc1, dc2 = st.columns(2)
        with dc1:
            disability_percentage = st.slider("Disability Certification (%)", 0, 100, 0)
        with dc2:
            disability_types = st.multiselect("Disability Types (select all that apply)", DISABILITY_TYPE_OPTIONS)

        st.markdown("---")
        st.markdown("**§ Economic Profile**")
        ec1, ec2, ec3 = st.columns(3)
        with ec1:
            annual_income = st.number_input("Annual Income (₹/yr)", min_value=0.0, value=0.0, step=1000.0)
        with ec2:
            monthly_household_income = st.number_input("Monthly Household Income (₹/mo)", min_value=0.0, value=0.0, step=500.0)
        with ec3:
            area = st.selectbox("Area Classification", ["rural", "urban"])

        ec4, ec5, ec6 = st.columns(3)
        with ec4:
            is_bpl = st.checkbox("Below Poverty Line (BPL) Card Holder")
        with ec5:
            bpl_score = st.number_input("BPL Score (0–100, if applicable)", min_value=0, max_value=100, value=0, step=1)
        with ec6:
            caste_category = st.selectbox("Caste Category", [None, "SC", "ST", "OBC", "General"])

        st.markdown("---")
        st.markdown("**§ Domicile & Family**")
        ff1, ff2, ff3 = st.columns(3)
        with ff1:
            state = st.text_input("State", value="Gujarat")
        with ff2:
            is_gujarat_domicile = st.checkbox("Gujarat Domicile Certificate", value=True)
        with ff3:
            has_adult_son_over_21 = st.checkbox("Has Adult Son ≥ 21 years")

        st.markdown("---")
        st.markdown("**§ Education (for Saraswati Sadhana Yojana)**")
        ed1, ed2 = st.columns(2)
        with ed1:
            is_student = st.checkbox("Currently Enrolled Student")
        with ed2:
            education_standard = st.number_input("Education Standard (class)", min_value=0, max_value=12, value=0, step=1)

        st.markdown("---")
        st.markdown("**§ Foster / Guardian (for Palak Mata Pita Yojana)**")
        fg1, fg2 = st.columns(2)
        with fg1:
            has_foster_guardian = st.checkbox("Has Foster Guardian / Caretaker")
        with fg2:
            guardian_annual_income = st.number_input("Guardian Annual Income (₹/yr)", min_value=0.0, value=0.0, step=10000.0)

        st.markdown("---")
        st.markdown("**§ Bereavement (for NFBS)**")
        bv1, bv2 = st.columns(2)
        with bv1:
            is_breadwinner_deceased = st.checkbox("Primary Household Breadwinner Deceased")
        with bv2:
            deceased_breadwinner_age = st.number_input("Deceased Breadwinner Age at Death", min_value=0, max_value=120, value=0, step=1)

        st.markdown("---")
        st.markdown("**§ Marriage (for Divyang Shadi Sahay)**")
        mg1, mg2, mg3 = st.columns(3)
        with mg1:
            is_marriage_registered = st.checkbox("Marriage Legally Registered")
        with mg2:
            spouse_disability_percentage = st.slider("Spouse Disability (%)", 0, 100, 0)
        with mg3:
            spouse_age = st.number_input("Spouse Age", min_value=0, max_value=120, value=0, step=1)

        spouse_gender = st.selectbox("Spouse Gender", [None, "male", "female", "other"])

        submitted = st.form_submit_button(
            "⚡ EXECUTE DETERMINISTIC STATUTORY ENGINE",
            use_container_width=True,
        )

        if submitted:
            citizen = CitizenProfile(
                full_name=full_name,
                age=age,
                gender=gender,
                marital_status=marital_status,
                is_orphan=is_orphan,
                disability_percentage=disability_percentage,
                disability_types=disability_types,
                annual_income=annual_income,
                monthly_household_income=monthly_household_income,
                area=area,
                state=state,
                is_bpl=is_bpl,
                bpl_score=bpl_score if bpl_score > 0 else None,
                has_adult_son_over_21=has_adult_son_over_21,
                is_student=is_student,
                education_standard=education_standard if education_standard > 0 else None,
                caste_category=caste_category,
                is_breadwinner_deceased=is_breadwinner_deceased,
                deceased_breadwinner_age=deceased_breadwinner_age if deceased_breadwinner_age > 0 else None,
                is_marriage_registered=is_marriage_registered,
                spouse_disability_percentage=spouse_disability_percentage,
                spouse_age=spouse_age if spouse_age > 0 else None,
                spouse_gender=spouse_gender,
                is_gujarat_domicile=is_gujarat_domicile,
                has_foster_guardian=has_foster_guardian,
                guardian_annual_income=guardian_annual_income if guardian_annual_income > 0 else None,
            )

            result = evaluate_all_schemes(citizen, st.session_state.session_id)
            st.session_state.evaluation = result
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 12: TAB 2 — STATUTORY ENTITLEMENT LEDGER
# ══════════════════════════════════════════════════════════════════════════════

def render_ledger_tab():
    st.markdown("### 📋 Statutory Entitlement Ledger")

    result: Optional[EvaluationResult] = st.session_state.get("evaluation")
    if result is None:
        st.info("No evaluation executed yet. Use the **Terminal Ingestion** tab to submit citizen data.")
        return

    qualified = [s for s in result.schemes if s.qualified]
    disqualified = [s for s in result.schemes if not s.qualified]

    if qualified:
        st.markdown(
            f"<div style='background:#065F46;border:1px solid #10B981;border-radius:8px;padding:12px 16px;margin-bottom:16px;'>"
            f"<span style='font-family:JetBrains Mono,monospace;color:#10B981;font-size:0.85rem;font-weight:600;'>"
            f"✓ {len(qualified)} SCHEME(S) QUALIFIED</span>"
            f"<span style='float:right;font-family:JetBrains Mono,monospace;color:#10B981;font-size:0.85rem;'>"
            f"ANNUAL DBT: ₹{result.total_annual_cash:,.0f}/yr"
            + (f" + ₹{result.total_one_time_cash:,.0f} lump-sum" if result.total_one_time_cash > 0 else "")
            + f"</span></div>",
            unsafe_allow_html=True,
        )

        for s in qualified:
            badge_color = EMERALD if s.entitlement_type == "cash" else (SOVEREIGN_BLUE if s.entitlement_type in ("hardware", "service") else AMBER)
            with st.expander(f"✅ {s.scheme_id} — {s.scheme_name}", expanded=True):
                ic1, ic2 = st.columns([2, 1])
                with ic1:
                    st.markdown(f"**Administering Body:** {s.administering_body}")
                    st.markdown(f"**Legal Citation:** `{s.legal_citation}`")
                    st.markdown(f"**Entitlement Type:** `{s.entitlement_type.upper()}`")
                with ic2:
                    if s.annual_cash_value > 0:
                        st.markdown(
                            f"<div style='background:#065F46;border-radius:8px;padding:12px;text-align:center;'>"
                            f"<div style='font-family:JetBrains Mono,monospace;color:#10B981;font-size:1.4rem;font-weight:700;'>"
                            f"₹{s.annual_cash_value:,.0f}/yr</div>"
                            f"<div style='font-family:JetBrains Mono,monospace;color:#94A3B8;font-size:0.7rem;'>"
                            f"₹{s.monthly_cash_value:,.0f}/month via DBT</div></div>",
                            unsafe_allow_html=True,
                        )
                    elif s.one_time_cash_value > 0:
                        st.markdown(
                            f"<div style='background:#78350F;border-radius:8px;padding:12px;text-align:center;'>"
                            f"<div style='font-family:JetBrains Mono,monospace;color:#F59E0B;font-size:1.4rem;font-weight:700;'>"
                            f"₹{s.one_time_cash_value:,.0f}</div>"
                            f"<div style='font-family:JetBrains Mono,monospace;color:#94A3B8;font-size:0.7rem;'>"
                            f"ONE-TIME RELIEF</div></div>",
                            unsafe_allow_html=True,
                        )

                if s.hardware_grants:
                    st.markdown("**Hardware Grants:**")
                    for hw in s.hardware_grants:
                        st.markdown(f"- 🔧 {hw}")
                if s.service_grants:
                    st.markdown("**Service Grants:**")
                    for svc in s.service_grants:
                        st.markdown(f"- 🎫 {svc}")
                if s.notes:
                    st.markdown(f"**Notes:** {s.notes}")

                st.markdown("**Required Documents:**")
                for doc in s.required_documents:
                    st.markdown(f"- ☐ {doc}")
    else:
        st.warning("No statutory entitlements qualified under the current citizen profile. Please review the input data.")

    if disqualified:
        st.markdown("---")
        st.markdown(
            f"<span style='font-family:JetBrains Mono,monospace;color:#94A3B8;font-size:0.8rem;'>"
            f"▼ {len(disqualified)} SCHEME(S) NOT QUALIFIED — TRANSPARENCY AUDIT</span>",
            unsafe_allow_html=True,
        )
        for s in disqualified:
            with st.expander(f"❌ {s.scheme_id} — {s.scheme_name}", expanded=False):
                st.markdown(f"**Administering Body:** {s.administering_body}")
                if s.disqualification_reasons:
                    st.markdown("**Disqualification Reasons:**")
                    for reason in s.disqualification_reasons:
                        st.markdown(f"- ⚠️ {reason}")
                else:
                    st.markdown("*Criteria not met — review statutory thresholds in Gazette Knowledge Base.*")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 13: TAB 3 — GAZETTE KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════════════════════

def render_gazette_tab():
    st.markdown("### 📚 Gazette Knowledge Base")
    st.markdown(
        "<span style='color:#94A3B8;font-size:0.85rem;'>"
        "Searchable directory of gazetted statutory rules, GR numbers, income caps, "
        "and welfare entitlements across Gujarat State and Central Government schemes.</span>",
        unsafe_allow_html=True,
    )

    search_query = st.text_input(
        "🔍 Search schemes, GR numbers, categories…",
        placeholder="e.g., disability pension, widow, ADIP, ₹1,20,000…",
    )

    filtered = GAZETTE_ENTRIES
    if search_query.strip():
        q = search_query.strip().lower()
        filtered = []
        for entry in GAZETTE_ENTRIES:
            searchable = " ".join([
                entry["scheme_id"], entry["name"], entry["administering_body"],
                entry["gr_number"], entry["category"], entry["target_group"],
                entry["income_cap"], entry["entitlement"], entry["legal_basis"],
                " ".join(entry["criteria"]),
            ]).lower()
            if q in searchable:
                filtered.append(entry)

    if not filtered:
        st.warning("No schemes match your search query.")
        return

    st.markdown(
        f"<span style='font-family:JetBrains Mono,monospace;color:#94A3B8;font-size:0.7rem;'>"
        f"Displaying {len(filtered)} of {len(GAZETTE_ENTRIES)} gazetted schemes</span>",
        unsafe_allow_html=True,
    )

    for entry in filtered:
        with st.expander(f"📜 {entry['scheme_id']} — {entry['name']}", expanded=False):
            gc1, gc2 = st.columns([3, 2])
            with gc1:
                st.markdown(f"**Administering Body:** {entry['administering_body']}")
                st.markdown(f"**GR Number:** `{entry['gr_number']}`")
                st.markdown(f"**Category:** {entry['category']}")
                st.markdown(f"**Target Group:** {entry['target_group']}")
                st.markdown(f"**Legal Basis:** {entry['legal_basis']}")
            with gc2:
                st.markdown(
                    f"<div style='background:#0F172A;border:1px solid #1E293B;border-radius:8px;padding:12px;'>"
                    f"<div style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#94A3B8;text-transform:uppercase;letter-spacing:0.05em;'>Income Cap</div>"
                    f"<div style='font-family:JetBrains Mono,monospace;font-size:0.85rem;color:#F59E0B;margin:4px 0;'>{entry['income_cap']}</div>"
                    f"<div style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#94A3B8;text-transform:uppercase;letter-spacing:0.05em;margin-top:8px;'>Entitlement</div>"
                    f"<div style='font-family:JetBrains Mono,monospace;font-size:0.85rem;color:#10B981;margin:4px 0;'>{entry['entitlement']}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            st.markdown("**Statutory Criteria:**")
            for criterion in entry["criteria"]:
                st.markdown(f"- {criterion}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 14: TAB 4 — AUDIT & EXPORT
# ══════════════════════════════════════════════════════════════════════════════

def render_audit_tab():
    st.markdown("### 🔒 Audit & Export")

    result: Optional[EvaluationResult] = st.session_state.get("evaluation")
    if result is None:
        st.info("No evaluation executed yet. Use the **Terminal Ingestion** tab to submit citizen data.")
        return

    st.markdown(
        f"<div style='background:#0F172A;border:1px solid #1E293B;border-radius:8px;padding:16px;margin-bottom:16px;'>"
        f"<div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;'>"
        f"<div>"
        f"<span style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#94A3B8;'>EXECUTION HASH</span><br/>"
        f"<span style='font-family:JetBrains Mono,monospace;font-size:0.95rem;color:#10B981;font-weight:600;'>{result.execution_hash}</span>"
        f"</div>"
        f"<div>"
        f"<span style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#94A3B8;'>SESSION</span><br/>"
        f"<span style='font-family:JetBrains Mono,monospace;font-size:0.95rem;color:#F8FAFC;'>{result.session_id}</span>"
        f"</div>"
        f"<div>"
        f"<span style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#94A3B8;'>TIMESTAMP</span><br/>"
        f"<span style='font-family:JetBrains Mono,monospace;font-size:0.95rem;color:#F8FAFC;'>{result.timestamp}</span>"
        f"</div>"
        f"</div></div>",
        unsafe_allow_html=True,
    )

    ac1, ac2 = st.columns(2)
    with ac1:
        st.markdown("#### Intermediate JSON Representation")
        export_data = result.model_dump()
        export_data["citizen"] = result.citizen.model_dump()
        export_data["schemes"] = [s.model_dump() for s in result.schemes]
        st.json(export_data)

    with ac2:
        st.markdown("#### Sovereign PDF Dossier")
        st.markdown(
            "<span style='color:#94A3B8;font-size:0.85rem;'>"
            "Generate a court-admissible Statutory Claim Audit Dossier in PDF format. "
            "Includes verification hashes, legal citations, and Mamlatdar/TDO submission checklists."
            "</span>",
            unsafe_allow_html=True,
        )

        pdf_bytes = generate_pdf_dossier(result)
        now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"HAQX_Dossier_{result.session_id}_{now_str}.pdf"

        st.download_button(
            label="📥 DOWNLOAD SOVEREIGN AUDIT DOSSIER (PDF)",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True,
        )

        st.markdown(
            f"<div style='margin-top:12px;background:#0F172A;border:1px solid #1E293B;border-radius:8px;padding:12px;'>"
            f"<span style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#94A3B8;'>"
            f"PDF Size: {len(pdf_bytes):,} bytes &nbsp;|&nbsp; "
            f"Schemes Audited: 12 &nbsp;|&nbsp; "
            f"Qualified: {result.total_schemes_qualified} &nbsp;|&nbsp; "
            f"Format: A4 Portrait"
            f"</span></div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;padding:16px;'>"
        "<span style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#94A3B8;'>"
        f"HAQX Core {VERSION} · Neuro-Symbolic Civic Execution Engine · "
        f"{SDG_BADGE} · {PRIVACY_STATUS} · "
        "All statutory evaluations are deterministic computations of gazetted rules. "
        "This system does not constitute legal advice.</span></div>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 15: APPLICATION ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    st.set_page_config(
        page_title="HAQX Core v2.0-Sovereign",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    inject_css()

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:12].upper()
    if "evaluation" not in st.session_state:
        st.session_state.evaluation = None

    render_hud_bar(st.session_state.session_id)

    if st.session_state.evaluation is not None:
        render_metric_cards(st.session_state.evaluation)

    tab1, tab2, tab3, tab4 = st.tabs([
        "⌨ Terminal Ingestion",
        "📋 Statutory Entitlement Ledger",
        "📚 Gazette Knowledge Base",
        "🔒 Audit & Export",
    ])

    with tab1:
        render_ingestion_tab()
    with tab2:
        render_ledger_tab()
    with tab3:
        render_gazette_tab()
    with tab4:
        render_audit_tab()


if __name__ == "__main__":
    main()
