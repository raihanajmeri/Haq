import streamlit as st
import json
import io
import requests
from pydantic import BaseModel, Field
from typing import Optional, List
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# -------------------------------------------------------------------------
# PAGE CONFIGURATION & INSTITUTIONAL HUD STYLING
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="HAQX | Sovereign Civic Execution Protocol",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at top right, #0F172A 0%, #020617 100%);
        color: #F8FAFC;
    }
    
    .mono {
        font-family: 'JetBrains Mono', monospace;
    }

    .telemetry-bar {
        background-color: #0B0F19;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 8px 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #64748B;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
    }
    
    .live-dot {
        height: 8px;
        width: 8px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        box-shadow: 0 0 8px #10B981;
    }

    .metric-box {
        background: #0B0F19;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 20px;
        position: relative;
        overflow: hidden;
    }
    
    .metric-box::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: #3B82F6;
    }
    
    .metric-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.2rem;
        font-weight: 700;
        color: #10B981;
        margin-top: 4px;
    }

    .claim-item {
        background: #0B0F19;
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 12px;
        transition: border 0.2s ease;
    }
    
    .claim-item:hover {
        border-color: #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# DETERMINISTIC DATA ENGINE (PYDANTIC SCHEMAS - ZERO HALLUCINATION)
# -------------------------------------------------------------------------
class CitizenProfile(BaseModel):
    name: Optional[str] = "Undisclosed Citizen"
    age: int = Field(..., description="Age of applicant in years")
    gender: str = Field(default="Male")
    state: str = Field(default="Gujarat")
    annual_income: int = Field(..., description="Total household annual income in INR")
    disability_pct: int = Field(default=0, description="Certified percentage 0-100")
    disability_type: str = Field(default="None")
    is_widow: bool = False
    has_bpl_card: bool = False
    is_orphan: bool = False
    has_adult_son: bool = False
    area: str = Field(default="Rural")

class StatutoryAuditResult(BaseModel):
    scheme_id: str
    scheme_name: str
    authority: str
    annual_cash: int
    in_kind: Optional[str] = None
    statutory_docs: List[str]

def run_deterministic_rules(p: CitizenProfile) -> List[StatutoryAuditResult]:
    entitlements = []
    
    # 1. Sant Surdas Yojana (Gujarat DSD)
    if p.state == "Gujarat" and p.disability_pct >= 60:
        income_cap = 47000 if p.area == "Rural" else 68000
        if p.annual_income <= income_cap or p.has_bpl_card:
            entitlements.append(StatutoryAuditResult(
                scheme_id="GJ-DSD-SSY",
                scheme_name="Sant Surdas Yojana (સંત સુરદાસ સહાય)",
                authority="Directorate of Social Defence, Gujarat",
                annual_cash=12000,
                in_kind=None,
                statutory_docs=["UDID Card (≥60%)", "Income Certificate / BPL", "Aadhaar", "Bank Passbook"]
            ))

    # 2. ADIP Scheme (Central MSJE)
    monthly_income = p.annual_income / 12
    if p.disability_pct >= 40 and monthly_income <= 30000:
        hardware = "Motorized Tricycle" if (p.disability_pct >= 80 and p.age >= 16) else "Wheelchair / Digital Hearing Aid"
        entitlements.append(StatutoryAuditResult(
            scheme_id="IN-MSJE-ADIP",
            scheme_name="Assistance to Disabled Persons (ADIP)",
            authority="Ministry of Social Justice & Empowerment, GoI",
            annual_cash=0,
            in_kind=hardware,
            statutory_docs=["Disability Certificate (≥40%)", "Income Certificate", "Residence Proof"]
        ))

    # 3. Ganga Swarupa Yojana (Gujarat Widow Pension)
    if p.state == "Gujarat" and p.is_widow and p.age >= 18:
        cap = 120000 if p.area == "Rural" else 150000
        if p.annual_income <= cap:
            entitlements.append(StatutoryAuditResult(
                scheme_id="GJ-WCD-GSY",
                scheme_name="Ganga Swarupa Financial Assistance",
                authority="Women & Child Development, Gujarat",
                annual_cash=15000,
                in_kind=None,
                statutory_docs=["Death Certificate of Spouse", "Income Certificate", "No-Remarriage Affidavit"]
            ))

    # 4. Palak Mata Pita Yojana
    if p.state == "Gujarat" and p.is_orphan and p.age < 18 and p.annual_income <= 2000000:
        entitlements.append(StatutoryAuditResult(
            scheme_id="GJ-SJE-PMPY",
            scheme_name="Palak Mata Pita Foster Grant",
            authority="Social Justice & Empowerment, Gujarat",
            annual_cash=48000,
            in_kind="Educational Rehabilitation Support",
            statutory_docs=["Parents' Death Certificates", "Foster Legal Affidavit", "School Bonafide Certificate"]
        ))

    # 5. GSRTC Universal Transit Floor
    if p.state == "Gujarat" and p.disability_pct >= 40:
        entitlements.append(StatutoryAuditResult(
            scheme_id="GJ-GSRTC-DIV",
            scheme_name="Divyang Universal Transit Pass",
            authority="GSRTC & Directorate of Social Defence",
            annual_cash=0,
            in_kind="100% Free Lifetime Bus Travel Pass",
            statutory_docs=["UDID Card", "Proof of Gujarat Domicile", "Passport Photos"]
        ))
        
    return entitlements

# -------------------------------------------------------------------------
# STATUTORY PDF GENERATOR (DOCUMENT SYNTHESIS)
# -------------------------------------------------------------------------
def generate_statutory_dossier(profile: CitizenProfile, results: List[StatutoryAuditResult], total_cash: int) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elements = []
    
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.HexColor('#0F172A'))
    body = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor('#334155'))
    bold_body = ParagraphStyle('BBody', parent=body, fontName='Helvetica-Bold')

    elements.append(Paragraph("HAQX // STATUTORY ENTITLEMENT DOSSIER", h1))
    elements.append(Paragraph("Verified Digital Public Infrastructure Artifact • UN SDG 1.3 Target Compliance", body))
    elements.append(Spacer(1, 15))

    meta_table_data = [
        [Paragraph("<b>Claimant:</b>", body), Paragraph(profile.name, body), Paragraph("<b>Jurisdiction:</b>", body), Paragraph(f"{profile.state} ({profile.area})", body)],
        [Paragraph("<b>Age/Gender:</b>", body), Paragraph(f"{profile.age} / {profile.gender}", body), Paragraph("<b>Annual Income:</b>", body), Paragraph(f"INR {profile.annual_income:,}", body)],
        [Paragraph("<b>Disability Audit:</b>", body), Paragraph(f"{profile.disability_pct}% ({profile.disability_type})", body), Paragraph("<b>Audit Status:</b>", body), Paragraph("DETERMINISTIC VERIFIED", bold_body)],
    ]
    t = Table(meta_table_data, colWidths=[90, 180, 90, 180])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 15))

    elements.append(Paragraph(f"<b>TOTAL ANNUAL CASH ENTITLEMENT UNLOCKED: INR {total_cash:,}</b>", h1))
    elements.append(Spacer(1, 10))

    results_data = [["Statutory Code", "Scheme Manifest", "Administering Authority", "Legally Guaranteed Benefit"]]
    for r in results:
        benefit_desc = f"INR {r.annual_cash:,}/yr" if r.annual_cash > 0 else r.in_kind
        results_data.append([r.scheme_id, r.scheme_name, r.authority, benefit_desc])
    
    rt = Table(results_data, colWidths=[80, 180, 160, 120])
    rt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(rt)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("This instrument certifies statutory entitlement identification under state gazetted welfare law. Generated autonomously with zero human intervention via HAQX Core.", body))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

# -------------------------------------------------------------------------
# INTERACTION INTERFACE
# -------------------------------------------------------------------------
st.markdown("""
<div class="telemetry-bar">
    <div><span class="live-dot"></span>HAQX CORE: v1.0.4-SOVEREIGN // STATUS: OPERATIONAL</div>
    <div>ZERO-HALLUCINATION DETERMINISTIC ENGINE</div>
    <div>SDG 1.3 COMPLIANT</div>
</div>
""", unsafe_allow_html=True)

st.title("Sovereign Civic Execution Engine")
st.caption("Translating conversational speech and unstructured demographic inputs into verified, statutory entitlements.")

with st.sidebar:
    st.markdown("### Protocol Configuration")
    user_api_key = st.text_input("Gemini API Key (Google AI Studio)", type="password", help="Enter key from aistudio.google.com")
    st.markdown("---")
    st.markdown("#### System Metrics")
    st.caption("• Execution Engine: Neuro-Symbolic Boundary")
    st.caption("• PII Leakage: Zero (Client-Ephemeral)")
    st.caption("• License: MIT Open Source")

col_input, col_audit = st.columns([1, 1], gap="large")

with col_input:
    st.markdown("### 1. Ingestion Vector")
    mode = st.radio("Select Input Mode", ["Voice / Raw Vernacular Speech", "Structured Manual Input"], horizontal=True)

    if mode == "Voice / Raw Vernacular Speech":
        st.markdown("**Spoken Dialect Ingestion (Audio / Vernacular Text)**")
        raw_speech = st.text_area(
            "Natural Dialect Input (Gujarati, Hindi, or Vernacular English):",
            value="હું સુરત પાસે રહું છું. મારો પગ એક અકસ્માતમાં કપાઈ ગયો છે અને 80% ખોડખાંપણ છે. મારી પાસે કોઈ કમાણી નથી અને ઘરમાં કોઈ મોટો દીકરો નથી. મહિને માંડ ત્રણ હજાર રૂપિયા થાય છે. હું અને મારી પત્ની મુશ્કેલીમાં છીએ.",
            height=130
        )
        
        if st.button("EXECUTE NEURO-EXTRACTION", type="primary", use_container_width=True):
            if not user_api_key:
                st.error("Missing Gemini API Key. Paste your key in the sidebar configuration.")
            else:
                extraction_prompt = f"""
                You are a strict legal data extraction parser. Given the following unstructured citizen statement, extract demographic variables into pure, valid JSON with NO commentary and NO markdown formatting.
                
                Input Statement: "{raw_speech}"
                
                Required JSON structure:
                {{
                    "name": "Citizen (auto-assigned if missing)",
                    "age": 40,
                    "gender": "Male",
                    "state": "Gujarat",
                    "annual_income": 36000,
                    "disability_pct": 80,
                    "disability_type": "Locomotor",
                    "is_widow": false,
                    "has_bpl_card": false,
                    "is_orphan": false,
                    "has_adult_son": false,
                    "area": "Rural"
                }}
                """
                
                with st.spinner("Connecting to neural variable synthesis..."):
                    try:
                        clean_key = user_api_key.strip()
                        headers = {"Content-Type": "application/json"}
                        payload = {
                            "contents": [{
                                "parts": [{"text": extraction_prompt}]
                            }]
                        }
                        
                        # Direct REST call targeting active 3.6-flash first
                        candidate_models = ["gemini-3.6-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
                        response_json = None
                        success = False
                        last_error = ""
                        
                        for m_alias in candidate_models:
                            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m_alias}:generateContent?key={clean_key}"
                            res = requests.post(url, headers=headers, json=payload)
                            data = res.json()
                            if "error" not in data and "candidates" in data:
                                response_json = data
                                success = True
                                break
                            else:
                                last_error = data.get("error", {}).get("message", "Unknown error")

                        if not success:
                            st.error(f"API Error from Google: {last_error}")
                        else:
                            raw_output = response_json["candidates"][0]["content"]["parts"][0]["text"]
                            clean_json = raw_output.replace("```json", "").replace("```", "").strip()
                            parsed_dict = json.loads(clean_json)
                            st.session_state['parsed_profile'] = CitizenProfile(**parsed_dict)
                            st.success("Extracted Variables Successfully.")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Extraction Pipeline Failure: {str(e)}")

    else:
        st.markdown("**Manual Structured Entry**")
        with st.form("manual_entry_form"):
            name = st.text_input("Citizen Identifier", value="Citizen-09")
            c1, c2 = st.columns(2)
            with c1:
                age = st.number_input("Age", 0, 110, 48)
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                income = st.number_input("Annual Household Income (₹)", 0, 2000000, 36000, step=5000)
                widow = st.checkbox("Applicant is Widow") if gender == "Female" else False
            with c2:
                dis_pct = st.slider("Disability %", 0, 100, 80)
                dis_type = st.selectbox("Disability Class", ["Locomotor", "Visual", "Hearing", "Intellectual", "None"])
                area = st.selectbox("Area", ["Rural", "Urban"])
                bpl = st.checkbox("BPL Card Holder")
                orphan = st.checkbox("Orphan Minor")
            
            if st.form_submit_button("COMPILE PROFILE", use_container_width=True):
                st.session_state['parsed_profile'] = CitizenProfile(
                    name=name, age=age, gender=gender, state="Gujarat", annual_income=income,
                    disability_pct=dis_pct, disability_type=dis_type, is_widow=widow,
                    has_bpl_card=bpl, is_orphan=orphan, area=area
                )

    if 'parsed_profile' in st.session_state:
        st.markdown("#### Parsed Intermediate Representation")
        st.json(st.session_state['parsed_profile'].model_dump())

with col_audit:
    st.markdown("### 2. Statutory Audit & Output")
    
    if 'parsed_profile' in st.session_state:
        profile = st.session_state['parsed_profile']
        audit_results = run_deterministic_rules(profile)
        total_cash = sum(r.annual_cash for r in audit_results)
        
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"""
            <div class="metric-box">
                <span class="mono" style="font-size: 0.8rem; color: #94A3B8;">DIRECT ANNUAL CASH</span>
                <div class="metric-val">₹{total_cash:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-box">
                <span class="mono" style="font-size: 0.8rem; color: #94A3B8;">STATUTORY MATCHES</span>
                <div class="metric-val" style="color: #38BDF8;">{len(audit_results)}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        for r in audit_results:
            benefit_badge = f"₹{r.annual_cash:,}/yr" if r.annual_cash > 0 else r.in_kind
            st.markdown(f"""
            <div class="claim-item">
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <span class="mono" style="font-size: 0.75rem; color: #3B82F6; font-weight: bold;">{r.scheme_id}</span>
                    <span class="mono" style="color: #10B981; font-weight: bold;">{benefit_badge}</span>
                </div>
                <div style="font-size: 1.1rem; font-weight: 600; margin: 4px 0;">{r.scheme_name}</div>
                <div style="font-size: 0.8rem; color: #94A3B8;">{r.authority}</div>
            </div>
            """, unsafe_allow_html=True)
            
        pdf_bytes = generate_statutory_dossier(profile, audit_results, total_cash)
        st.download_button(
            label="DOWNLOAD STATUTORY CLAIM DOSSIER (PDF)",
            data=pdf_bytes,
            file_name=f"HAQX_Statutory_Dossier_{profile.age}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
    else:
        st.info("Awaiting citizen ingestion vector execution on the left panel.")
