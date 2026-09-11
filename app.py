import streamlit as st

# Page setup
st.set_page_config(page_title="HAQ - Sovereign Welfare Engine", page_icon="⚖️", layout="centered")

st.title("⚖️ HAQ: Sovereign Welfare Execution Engine")
st.markdown("### Claim what the state legally owes you. Built for UN SDG 1.3.")

st.info("Enter citizen details below. The deterministic engine matches statutory government gazettes with zero hallucinations.")

# Input fields
st.subheader("1. Citizen Demographics")
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=0, max_value=110, value=35)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    is_widow = st.checkbox("Is the applicant a widow?") if gender == "Female" else False

with col2:
    state = st.selectbox("State", ["Gujarat", "Other"])
    area_type = st.selectbox("Living Area", ["Rural", "Urban"])
    annual_income = st.number_input("Total Annual Household Income (₹)", min_value=0, max_value=1000000, value=36000, step=5000)

st.subheader("2. Disability & Vulnerability Details")
col3, col4 = st.columns(2)

with col3:
    has_disability = st.checkbox("Has physical or intellectual disability?")
    disability_pct = 0
    disability_type = "None"
    if has_disability:
        disability_pct = st.slider("Disability Percentage (as per UDID/Medical certificate)", 0, 100, 75)
        disability_type = st.selectbox("Disability Type", ["Locomotor/Orthopedic", "Visual", "Hearing", "Intellectual/Cerebral Palsy", "Multiple"])

with col4:
    has_bpl = st.checkbox("Holds BPL (Below Poverty Line) Card?")

# Evaluation Button
st.markdown("---")
if st.button("Run Statutory Entitlement Diagnosis 🚀", type="primary"):
    eligible_schemes = []
    total_annual_cash = 0
    assistive_aids = []

    # Scheme 1: Sant Surdas Yojana (Gujarat)
    if state == "Gujarat" and has_disability and disability_pct >= 75:
        income_limit = 47000 if area_type == "Rural" else 68000
        if annual_income <= income_limit or has_bpl:
            eligible_schemes.append({
                "name": "Sant Surdas Yojana (Gujarat)",
                "benefit": "₹1,000 per month (₹12,000/year) direct cash transfer to bank",
                "authority": "Social Justice & Empowerment Dept, Govt of Gujarat",
                "docs": ["Disability Certificate (75%+)", "Income Certificate or BPL Card", "Aadhaar Card", "Bank Passbook"]
            })
            total_annual_cash += 12000

    # Scheme 2: Central ADIP Scheme (Assistive Devices)
    monthly_income = annual_income / 12
    if has_disability and disability_pct >= 40 and monthly_income <= 30000:
        coverage = "100% Free Aid" if monthly_income <= 22500 else "50% Subsidized Aid"
        aid_item = "Motorized Tricycle / Wheelchair" if disability_pct >= 80 else "Tricycle / Hearing Aid / Crutches"
        eligible_schemes.append({
            "name": f"ADIP Scheme (Central Government - {coverage})",
            "benefit": f"Free assistive device allocation: {aid_item}",
            "authority": "Ministry of Social Justice and Empowerment, Govt of India",
            "docs": ["Disability Certificate (40%+)", "Income Certificate", "Identity Proof", "Passport Photo"]
        })
        assistive_aids.append(aid_item)

    # Scheme 3: Indira Gandhi National Disability Pension (IGNDPS)
    if has_disability and disability_pct >= 80 and 18 <= age <= 79 and has_bpl:
        eligible_schemes.append({
            "name": "Indira Gandhi National Disability Pension Scheme (Central)",
            "benefit": "₹500 - ₹1,000 per month statutory disability pension",
            "authority": "Ministry of Rural Development, Govt of India",
            "docs": ["BPL Card", "80%+ Severe Disability Proof", "Aadhaar", "Bank Account"]
        })
        total_annual_cash += 6000

    # Scheme 4: Ganga Swarupa Yojana (Gujarat Widow Pension)
    if state == "Gujarat" and is_widow and age >= 18:
        widow_limit = 120000 if area_type == "Rural" else 150000
        if annual_income <= widow_limit:
            eligible_schemes.append({
                "name": "Ganga Swarupa Yojana (Gujarat Widow Assistance)",
                "benefit": "₹1,250 per month (₹15,000/year) direct bank transfer",
                "authority": "Women & Child Development Department, Gujarat",
                "docs": ["Husband's Death Certificate", "Income Certificate", "Age Proof", "Affidavit"]
            })
            total_annual_cash += 15000

    # DISPLAY RESULTS
    st.success(f"Diagnosis Complete: Found {len(eligible_schemes)} statutory entitlements!")

    st.metric(label="Total Annual Cash Entitlements Unlocked", value=f"₹{total_annual_cash:,}")

    for idx, s in enumerate(eligible_schemes, 1):
        with st.expander(f"{idx}. {s['name']}", expanded=True):
            st.write(f"**Benefit:** {s['benefit']}")
            st.write(f"**Department:** {s['authority']}")
            st.write("**Mandatory Documents Needed:**")
            for d in s['docs']:
                st.write(f"- {d}")

    # Generate Summary text
    report = f"HAQ DIAGNOSIS REPORT\nBeneficiary Age: {age}, Annual Income: Rs {annual_income}\nTotal Annual Entitlement: Rs {total_annual_cash}\n\nEligible Schemes:\n"
    for s in eligible_schemes:
        report += f"- {s['name']}: {s['benefit']}\n"

    st.download_button("Download Official Claim Summary (TXT)", data=report, file_name=f"HAQ_Claim_Profile_{age}.txt")
