import streamlit as st
import json

# Set wide layout and page metadata
st.set_page_config(
    page_title="HAQ | Sovereign Civic Execution Engine",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom High-End Minimalist CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Global Background & Cards */
    .stApp {
        background-color: #0A0D14;
        color: #F3F4F6;
    }
    
    /* Header Container */
    .hero-container {
        border-bottom: 1px solid #1F2937;
        padding-bottom: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .badge-dpg {
        background-color: #1E293B;
        color: #38BDF8;
        border: 1px solid #0284C7;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 0.75rem;
    }
    
    /* Stat Cards */
    .metric-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: left;
    }
    
    .metric-val {
        font-size: 1.875rem;
        font-weight: 700;
        color: #10B981;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.825rem;
        color: #9CA3AF;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Result Scheme Cards */
    .scheme-card {
        background: #111827;
        border-left: 4px solid #3B82F6;
        border-top: 1px solid #1F2937;
        border-right: 1px solid #1F2937;
        border-bottom: 1px solid #1F2937;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    
    .scheme-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #F9FAFB;
        margin-bottom: 0.35rem;
    }
    
    .scheme-benefit {
        color: #34D399;
        font-weight: 500;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    
    .scheme-dept {
        color: #9CA3AF;
        font-size: 0.8rem;
    }
    
    /* Streamlit widget tweaks */
    div[data-testid="stExpander"] {
        background-color: #111827;
        border: 1px solid #1F2937;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-container">
    <span class="badge-dpg">UN SDG 1.3 • Sovereign Digital Public Infrastructure</span>
    <h1 style='margin: 0; font-size: 2.25rem; font-weight: 700; color: #FFFFFF;'>HAQ <span style='color: #3B82F6;'>Core</span></h1>
    <p style='color: #9CA3AF; font-size: 1.05rem; margin-top: 0.4rem;'>
        Deterministic neuro-symbolic civic execution engine. Translating citizen reality into legally binding statutory entitlements.
    </p>
</div>
""", unsafe_allow_html=True)

tab_diagnose, tab_voice, tab_library = st.tabs(["⚡ Entitlement Diagnostic", "🎙️ Natural Voice Parsing", "📚 Statutory Library (10 Schemes)"])

# TAB 1: DIAGNOSTIC ENGINE
with tab_diagnose:
    st.markdown("#### Citizen Diagnostic Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input("Age", min_value=0, max_value=115, value=42)
        gender = st.selectbox("Gender", ["Male", "Female", "Transgender / Other"])
        is_widow = False
        if gender == "Female":
            is_widow = st.checkbox("Applicant is a widow?")
            
    with col2:
        state = st.selectbox("State Jurisdiction", ["Gujarat", "Other State"])
        living_area = st.selectbox("Living Environment", ["Rural", "Urban"])
        annual_income = st.number_input("Annual Household Income (₹)", min_value=0, max_value=2000000, value=42000, step=5000)
        
    with col3:
        has_bpl = st.checkbox("Holds BPL Card / Score ≤ 20")
        has_adult_son = st.checkbox("Has a living son aged ≥ 21?", value=False)
        is_orphan = st.checkbox("Orphan child living with foster guardians?", value=False)
    
    st.markdown("---")
    st.markdown("#### Disability & Medical Classifications")
    
    col4, col5 = st.columns(2)
    with col4:
        has_disability = st.checkbox("Diagnosed with physical / intellectual disability")
        disability_pct = 0
        disability_type = "None"
        if has_disability:
            disability_pct = st.slider("Certified Disability Percentage (UDID / Medical Board)", 0, 100, 75)
            disability_type = st.selectbox("Clinical Classification", [
                "Locomotor / Orthopedic", 
                "Visual Impairment / Blindness", 
                "Hearing / Speech Impairment", 
                "Intellectual Disability / Cerebral Palsy / Autism", 
                "Multiple Disabilities"
            ])
            
    with col5:
        needs_assistive_devices = st.checkbox("Requires physical mobility or hearing assistive aid", value=True if has_disability else False)
        free_bus_travel_needed = st.checkbox("Requires public transport commute assistance", value=True if has_disability else False)

    # EVALUATION TRIGGER
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("RUN STATUTORY DETERMINISTIC AUDIT", use_container_width=True, type="primary"):
        eligible_schemes = []
        total_cash = 0
        in_kind_services = []

        # 1. Sant Surdas Yojana (Gujarat)
        if state == "Gujarat" and has_disability and disability_pct >= 60:
            income_cap = 47000 if living_area == "Rural" else 68000
            if annual_income <= income_cap or has_bpl:
                eligible_schemes.append({
                    "id": "GJ-SJE-01",
                    "name": "Sant Surdas Yojana (સંત સુરદાસ યોજના)",
                    "category": "Direct Income Support",
                    "benefit": "₹1,000 / month (₹12,000 annually) via DBT",
                    "dept": "Directorate of Social Defence, Govt of Gujarat",
                    "docs": ["Disability Certificate (≥60%)", "Income Certificate / BPL Score", "Aadhaar Card", "Bank Passbook"]
                })
                total_cash += 12000

        # 2. ADIP Scheme (Central Govt)
        monthly_inc = annual_income / 12
        if has_disability and disability_pct >= 40 and monthly_inc <= 30000:
            status = "100% Free Allocation" if monthly_inc <= 22500 else "50% Subsidized Allocation"
            item = "Motorized Tricycle / Electric Wheelchair" if (disability_pct >= 80 and age >= 16) else "Tricycle / Wheelchair / Digital Hearing Aid"
            eligible_schemes.append({
                "id": "IN-MSJE-01",
                "name": f"ADIP Scheme ({status})",
                "category": "Assistive Hardware",
                "benefit": f"Free statutory grant for: {item} (Valued at ₹10,000 to ₹40,000)",
                "dept": "Ministry of Social Justice and Empowerment, Govt of India",
                "docs": ["UDID / Disability Certificate (≥40%)", "Income Certificate", "Identity Proof", "Recent Photo"]
            })
            in_kind_services.append(f"ADIP: {item}")

        # 3. Indira Gandhi National Disability Pension Scheme (IGNDPS)
        if has_disability and disability_pct >= 80 and (18 <= age <= 79) and has_bpl:
            eligible_schemes.append({
                "id": "IN-MORD-01",
                "name": "Indira Gandhi National Disability Pension Scheme (IGNDPS)",
                "category": "Central Pension",
                "benefit": "₹500 / month (₹6,000 annually) direct central assistance",
                "dept": "Ministry of Rural Development, Govt of India",
                "docs": ["National BPL Card", "Severe Disability Certificate (≥80%)", "Aadhaar", "Bank Account"]
            })
            total_cash += 6000

        # 4. Ganga Swarupa Yojana (Gujarat Widow Pension)
        if state == "Gujarat" and is_widow and age >= 18:
            widow_cap = 120000 if living_area == "Rural" else 150000
            if annual_income <= widow_cap:
                eligible_schemes.append({
                    "id": "GJ-WCD-01",
                    "name": "Ganga Swarupa Yojana (ગંગા સ્વરૂપા સહાય યોજના)",
                    "category": "Direct Income Support",
                    "benefit": "₹1,250 / month (₹15,000 annually) direct bank transfer",
                    "dept": "Women & Child Development Department, Govt of Gujarat",
                    "docs": ["Husband's Death Certificate", "Local Authority Income Certificate", "Affidavit", "Aadhaar"]
                })
                total_cash += 15000

        # 5. Palak Mata Pita Yojana (Foster Child Support)
        if state == "Gujarat" and is_orphan and age < 18 and annual_income <= 2000000:
            eligible_schemes.append({
                "id": "GJ-SJE-02",
                "name": "Palak Mata Pita Yojana (પાલક માતા-પિતા યોજના)",
                "category": "Child Protection Support",
                "benefit": "₹4,000 / month (₹48,000 annually) for school and livelihood maintenance",
                "dept": "Social Justice & Empowerment Department, Gujarat",
                "docs": ["Parents' Death Certificates", "Foster Guardian Affidavit", "Child Age Proof / School Bonafide"]
            })
            total_cash += 48000

        # 6. Destitute Elderly & Disabled Pension (Vrudh Sahay)
        destitute_cap = 120000 if living_area == "Rural" else 150000
        if state == "Gujarat" and annual_income <= destitute_cap:
            if (age >= 60 and not has_adult_son) or (age >= 45 and has_disability and disability_pct >= 75):
                pension_rate = 1250 if age >= 80 else 1000
                eligible_schemes.append({
                    "id": "GJ-SJE-03",
                    "name": "Financial Aid to Destitute Elderly & Disabled Persons",
                    "category": "State Destitution Floor",
                    "benefit": f"₹{pension_rate} / month (₹{pension_rate * 12} annually) direct cash assistance",
                    "dept": "Directorate of Social Defence, Gujarat",
                    "docs": ["Age Certificate / Electoral ID", "Proof of No Adult Son", "Income Certificate", "Aadhaar"]
                })
                total_cash += (pension_rate * 12)

        # 7. Divyang ST Bus Free Travel Pass
        if state == "Gujarat" and has_disability and disability_pct >= 40:
            eligible_schemes.append({
                "id": "GJ-GSRTC-01",
                "name": "Divyang Free Bus Travel Pass (એસ.ટી. બસ મફત મુસાફરી)",
                "category": "Universal Mobility Rights",
                "benefit": "100% Free Lifetime Commuter Pass across all Gujarat State Transport (GSRTC) buses",
                "dept": "GSRTC & Directorate of Social Defence, Gujarat",
                "docs": ["Civil Surgeon Disability Certificate (≥40%)", "Gujarat Domicile Proof", "Passport Photos"]
            })
            in_kind_services.append("GSRTC Free Travel Pass")

        # 8. Niramaya Health Insurance Scheme
        if state == "Gujarat" and has_disability and disability_type in ["Intellectual Disability / Cerebral Palsy / Autism", "Multiple Disabilities"]:
            eligible_schemes.append({
                "id": "IN-NAT-01",
                "name": "Niramaya Health Insurance Scheme (નિરામયા યોજના)",
                "category": "Critical Healthcare Floor",
                "benefit": "₹1,00,000 annual cashless coverage for corrective surgeries, OPD, and therapy",
                "dept": "The National Trust & Directorate of Social Defence, Gujarat",
                "docs": ["Disability Certificate (Autism/CP/ID/Multiple)", "Ration Card", "Bank Account"]
            })
            in_kind_services.append("Niramaya Health Insurance (₹1L)")

        # 9. Divyang Sadhan Sahay Yojana (Equipment Grant)
        sadhan_cap = 120000 if living_area == "Rural" else 150000
        if state == "Gujarat" and has_disability and disability_pct >= 40 and 16 <= age <= 60 and annual_income <= sadhan_cap:
            eligible_schemes.append({
                "id": "GJ-SJE-04",
                "name": "Divyang Sadhan Sahay Yojana (સાધન સહાય યોજના)",
                "category": "Livelihood & Assistive Aid",
                "benefit": "Direct in-kind distribution of Sewing Machines, Calipers, Crutches, or Wheelchairs",
                "dept": "e-Samaj Kalyan, Govt of Gujarat",
                "docs": ["UDID Card", "Income Certificate from Mamlatdar/TDO", "Ration Card", "Passport Photo"]
            })
            in_kind_services.append("Sadhan Sahay Equipment")

        # 10. National Family Benefit Scheme (NFBS)
        if has_bpl and 18 <= age <= 59 and annual_income <= 47000:
            eligible_schemes.append({
                "id": "IN-MORD-02",
                "name": "National Family Benefit Scheme (NFBS - રાષ્ટ્રીય કુટુંબ સહાય યોજના)",
                "category": "Emergency Crisis Capital",
                "benefit": "₹20,000 one-time direct cash transfer upon death of household primary breadwinner",
                "dept": "Ministry of Rural Development / Revenue Dept, Gujarat",
                "docs": ["BPL List Inclusion", "Breadwinner Death Certificate", "Age Proof (18-59)", "Bank Account"]
            })

        # RESULTS INTERFACE
        st.markdown("---")
        st.markdown("### 📊 Statutory Entitlement Assessment Report")
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val">₹{total_cash:,}</div>
                <div class="metric-label">Direct Annual Cash Entitlements</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: #38BDF8;">{len(eligible_schemes)}</div>
                <div class="metric-label">Statutory Schemes Qualified</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: #F59E0B;">{len(in_kind_services)}</div>
                <div class="metric-label">In-Kind Statutory Grants</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        if eligible_schemes:
            for s in eligible_schemes:
                st.markdown(f"""
                <div class="scheme-card">
                    <div style="font-size: 0.75rem; color: #60A5FA; font-weight: 600; text-transform: uppercase;">{s['id']} • {s['category']}</div>
                    <div class="scheme-title">{s['name']}</div>
                    <div class="scheme-benefit">{s['benefit']}</div>
                    <div class="scheme-dept">Authority: {s['dept']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander(f"Required Statutory Documentation Checklist ({s['name']})"):
                    for d in s['docs']:
                        st.markdown(f"- [ ] **{d}**")
                        
            # Downloadable Summary Dossier
            dossier_text = f"HAQ STATUTORY CLAIM AUDIT REPORT\n"
            dossier_text += f"Citizen Profile: Age {age} | Gender: {gender} | Area: {living_area} | Reported Income: Rs {annual_income}\n"
            dossier_text += f"Total Direct Annual Cash Unlocked: Rs {total_cash:,}\n"
            dossier_text += f"Schemes Identified ({len(eligible_schemes)}):\n"
            for s in eligible_schemes:
                dossier_text += f"\n- {s['name']} [{s['id']}]\n  Benefit: {s['benefit']}\n  Filing Authority: {s['dept']}\n"
            
            st.download_button(
                "📥 Download Official Citizen Claim Audit (Plaintext)",
                data=dossier_text,
                file_name=f"HAQ_Claim_Audit_Age_{age}.txt",
                use_container_width=True
            )
        else:
            st.warning("No statutory matches found under current threshold limits. Verify annual income certificate or medical board documentation.")

# TAB 2: VOICE TO SCHEMA PIPELINE
with tab_voice:
    st.markdown("#### 🎙️ Voice & Spoken Dialect Parsing Pipeline")
    st.write("This sandbox illustrates how raw, unstructured conversational speech in Gujarati, Hindi, or vernacular English is parsed into validated demographic variables.")
    
    sample_text = st.text_area(
        "Paste or simulate native speech transcript:",
        value="હું સુરત પાસે રહું છું. મારો પગ એક અકસ્માતમાં કપાઈ ગયો છે અને 80% ખોડખાંપણ છે. મારી પાસે કોઈ કમાણી નથી અને ઘરમાં કોઈ મોટો દીકરો નથી. મહિને માંડ ત્રણ હજાર રૂપિયા થાય છે."
    )
    
    st.markdown("""
    ```json
    // Neuro-Symbolic Boundary: AI Studio Extraction (Example Target)
    {
      "jurisdiction": "Gujarat",
      "disability_diagnosed": true,
      "disability_percentage": 80,
      "disability_type": "Locomotor / Orthopedic",
      "annual_household_income": 36000,
      "has_adult_son_over_21": false,
      "living_area": "Rural"
    }
    ```
    """)
    st.info("The neural model extracts only verifiable facts into this structured JSON schema. The deterministic rule engine takes that JSON and runs the statutory eligibility math without risk of hallucination.")

# TAB 3: STATUTORY SCHEME DIRECTORY
with tab_library:
    st.markdown("#### 📚 Gujarat & Central Statutory Scheme Directory")
    st.write("Current statutory logic rules encoded inside the HAQ engine:")
    
    schemes_data = [
        ("Sant Surdas Yojana", "Directorate of Social Defence, Gujarat", "≥60% Disability, Low Income/BPL", "₹1,000 / month direct pension"),
        ("ADIP Scheme", "Ministry of Social Justice & Empowerment, GoI", "≥40% Disability, Income ≤ ₹30k/mo", "Free motorized tricycles, wheelchairs, hearing aids"),
        ("Indira Gandhi Disability Pension (IGNDPS)", "Ministry of Rural Development, GoI", "18-79 yrs, ≥80% Disability, BPL Card", "₹500 - ₹1,000 / month central pension"),
        ("Ganga Swarupa Yojana", "Women & Child Development, Gujarat", "Widowed, Income ≤ ₹1.2L (R) / ₹1.5L (U)", "₹1,250 / month direct income transfer"),
        ("Palak Mata Pita Yojana", "Social Justice & Empowerment, Gujarat", "Orphaned children, Guardian income ≤ ₹20L", "₹4,000 / month educational assistance"),
        ("Destitute Elderly & Disabled Assistance", "Directorate of Social Defence, Gujarat", "Age ≥60 (no adult son) OR Age ≥45 (≥75% dis.)", "₹1,000 - ₹1,250 / month destitution support"),
        ("GSRTC Divyang Free Travel Pass", "GSRTC & Govt of Gujarat", "≥40% Certified Disability", "100% Free lifetime bus transportation"),
        ("Niramaya Health Insurance", "The National Trust & Govt of Gujarat", "Intellectual / Autism / Cerebral Palsy / Multiple", "₹1,00,000 annual cashless medical treatment"),
        ("Divyang Sadhan Sahay Yojana", "e-Samaj Kalyan, Gujarat", "16-60 yrs, ≥40% Disability, Income criteria", "Free sewing machines, calipers, tricycles"),
        ("National Family Benefit Scheme (NFBS)", "Ministry of Rural Development, GoI", "18-59 yrs, BPL, Death of primary breadwinner", "₹20,000 one-time emergency capital")
    ]
    
    for title, dept, crit, ben in schemes_data:
        with st.expander(title):
            st.markdown(f"**Authority:** {dept}")
            st.markdown(f"**Statutory Thresholds:** {crit}")
            st.markdown(f"**Legally Guaranteed Benefit:** {ben}")
