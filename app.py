import graphviz
import streamlit as st
import json
import re
from datetime import datetime

from core.input_layer import BrandInput
from utils.scraper import WebsiteScraper
from utils.report_storage import ReportStorage

from intelligence.instagram_algorithm_engine import InstagramAlgorithmEngine
from intelligence.brand_intelligence_engine import BrandIntelligenceEngine
from intelligence.scoring_engine import AIIntelligenceScoringEngine
from intelligence.pillar_permutation_engine import PillarPermutationEngine
from intelligence.seo_intelligence_engine import SEOIntelligenceEngine
from intelligence.brand_diagnosis_engine import BrandDiagnosisEngine
from intelligence.lifecycle_engine import LifecycleEngine
from intelligence.client_qualification_engine import ClientQualificationEngine
from intelligence.commercial_objective_engine import CommercialObjectiveEngine

from strategy.strategy_brain import StrategyBrain
from execution.ai_planning_engine import AIPlanningEngine
from x_system_output import render_client_report
from agency_hq_button import render_agency_hq_button


# -------------------------
# PAGE SETUP
# -------------------------

st.set_page_config(page_title="X", layout="wide")
st.title("X — Brand Intelligence System")


# -------------------------
# MODE SELECTOR
# -------------------------

if "mode" not in st.session_state:
    st.session_state["mode"] = "brand"

col1, col2 = st.columns(2)

with col1:
    if st.button("Brand Intelligence"):
        st.session_state["mode"] = "brand"

with col2:
    if st.button("Instagram Algorithm Check"):
        st.session_state["mode"] = "instagram"


# =========================
# INSTAGRAM MODE (ISOLATED)
# =========================

if st.session_state["mode"] == "instagram":

    st.subheader("Instagram Algorithm Check")

    page_link = st.text_input("Social Media Page Link")
    post_content = st.text_area("Post Content")

    if st.button("Analyze Post"):

        if not post_content:
            st.warning("Enter post content.")
            st.stop()

        engine = InstagramAlgorithmEngine()
        raw = engine.rewrite_and_score(post_content, page_link)

        try:
            result = json.loads(raw)
        except:
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                result = json.loads(match.group(0))
            else:
                st.error("AI response error.")
                st.code(raw)
                st.stop()

        st.metric("Algorithm Score", result.get("algorithm_score"))

        st.write("### What Works")
        st.write(result.get("what_is_working"))

        st.write("### Fix Needed")
        st.write(result.get("what_is_wrong"))

        st.subheader("Optimized Version")

        st.write("### Title")
        st.write(result.get("title"))

        st.write("### Hook")
        st.write(result.get("hook"))

        st.write("### Content")
        st.write(result.get("body"))

        st.write("### CTA")
        st.write(result.get("cta"))

        st.write("### Hashtags")
        st.write(", ".join(result.get("hashtags", [])))

        st.write("### Alt Text")
        st.write(result.get("alt_text"))

    st.stop()


# =========================
# BRAND MODE
# =========================

# -------------------------
# SIDEBAR INPUTS
# -------------------------

st.sidebar.header("Brand Inputs")

brand_name = st.sidebar.text_input("Brand Name")
website_url = st.sidebar.text_input("Website URL")
social_url = st.sidebar.text_input("Social Media URL (optional)")
location = st.sidebar.text_input("Location")
product_service = st.sidebar.text_input("Product / Service")

current_problem = st.sidebar.text_area(
    "Current Problem",
    help="One sentence only"
)

primary_keyword = st.sidebar.text_input("Primary SEO Keyword")

client_goal = st.sidebar.selectbox(
    "Client Goal",
    [
        "More Leads", "Sales Growth", "Brand Awareness", "Positioning",
        "Premium Clients", "Authority Building", "Market Expansion",
        "Launch Support", "Demand Generation"
    ]
)

monthly_budget = st.sidebar.number_input("Monthly Budget", value=50000)
urgency_level = st.sidebar.selectbox("Urgency Level", ["Low", "Medium", "High"])


# -------------------------
# LIFECYCLE INPUT
# -------------------------

st.sidebar.subheader("Brand Stage")

brand_stage = st.sidebar.radio(
    "Select Brand Stage",
    ["Foundational (New)", "Active (Running)"]
)

brand_stage_value = "Foundational" if "Foundational" in brand_stage else "Active"

follower_count = st.sidebar.number_input("Follower Count", min_value=0, value=0)
post_count = st.sidebar.number_input("Post Count", min_value=0, value=0)
website_age_days = st.sidebar.number_input("Website Age (days)", min_value=0, value=0)

lifecycle_engine = LifecycleEngine()
lifecycle_result = lifecycle_engine.evaluate(
    brand_stage=brand_stage_value,
    follower_count=follower_count,
    post_count=post_count,
    website_age_days=website_age_days,
)

lifecycle_stage = lifecycle_result.get("lifecycle_stage", "Active")

run = st.button("Analyze Brand")

if run:
    st.session_state["analysis_done"] = True

if st.session_state.get("analysis_done"):

    # =========================
    # MAIN EXECUTION
    # =========================

    if not website_url:
        st.error("Website URL required.")
        st.stop()

    scraper = WebsiteScraper()
    website_text = scraper.fetch_text(website_url)
    social_text = scraper.fetch_text(social_url) if social_url else ""

    # -------------------------
    # BRAND INTELLIGENCE
    # -------------------------

    intelligence_engine = BrandIntelligenceEngine()
    brand_data = json.loads(
        intelligence_engine.analyze(brand_input := BrandInput(
            brand_name=brand_name,
            website_url=website_url,
            location=location,
            product_service=product_service,
            current_problem=current_problem,
            brand_stage=lifecycle_stage,
        ), website_text, social_text)
    )

    # -------------------------
    # SEO
    # -------------------------

    seo_engine = SEOIntelligenceEngine()
    seo_data = json.loads(
        seo_engine.analyze(website_text, primary_keyword, lifecycle_stage)
    )

    # -------------------------
    # SCORING
    # -------------------------

    scoring_engine = AIIntelligenceScoringEngine()
    scores = json.loads(scoring_engine.evaluate(brand_data))

    # -------------------------
    # DIAGNOSIS
    # -------------------------

    diagnosis_engine = BrandDiagnosisEngine()
    diagnosis_result = diagnosis_engine.diagnose(
        brand_intelligence=brand_data,
        seo_intelligence=seo_data,
        scoring_output=scores
    )

    # -------------------------
    # CLIENT QUALIFICATION
    # -------------------------

    qualification_engine = ClientQualificationEngine()
    qualification_result = qualification_engine.evaluate(
        brand_intelligence=brand_data,
        diagnosis=diagnosis_result,
        demand_validation=diagnosis_result.get("demand_validation", {}),
        lifecycle_stage=lifecycle_stage,
        monthly_budget=monthly_budget,
        urgency_level=urgency_level,
    )

    # -------------------------
    # STRATEGY
    # -------------------------

    strategy = StrategyBrain(diagnosis_result, lifecycle_stage=lifecycle_stage)
    arc = strategy.generate_90_day_arc()

    # -------------------------
    # CLIENT REPORT OUTPUT
    # -------------------------

    render_client_report(
        brand_data=brand_data,
        seo_data=seo_data,
        scores=scores,
        diagnosis_result=diagnosis_result,
        arc=arc,
        qualification_result=qualification_result,
        brand_name=brand_name,
        client_goal=client_goal,
        lifecycle_stage=lifecycle_stage,
        monthly_budget=monthly_budget
    )

    # -------------------------
    # SEND TO AGENCY HQ BUTTON
    # -------------------------

    client_inputs = {
        "Brand Name": brand_name,
        "Website": website_url,
        "Social": social_url,
        "Location": location,
        "Service": product_service,
        "Current Problem": current_problem,
        "Goal": client_goal,
        "Monthly Budget": monthly_budget,
        "Stage": lifecycle_stage
    }

    render_agency_hq_button(
        brand_name=brand_name,
        client_inputs=client_inputs,
        brand_data=brand_data,
        seo_data=seo_data,
        scores=scores,
        diagnosis_result=diagnosis_result,
        arc=arc,
        qualification_result=qualification_result,
        lifecycle_stage=lifecycle_stage,
        monthly_budget=monthly_budget,
        client_goal=client_goal,
    )

    # -------------------------
    # SAVE REPORT
    # -------------------------

    storage = ReportStorage()

    report_data = {
        "brand": brand_data,
        "seo": seo_data,
        "scores": scores,
        "diagnosis": diagnosis_result
    }

    date_str = datetime.now().strftime("%d_%b_%Y")
    file_name = f"{brand_name}_{date_str}"

    storage.save_report(file_name, report_data)

    st.success("Report saved")

    # -------------------------
    # PDF DOWNLOAD
    # -------------------------

    from reports.pdf_report import PDFReport

    pdf = PDFReport()

    results_data = {
        "Diagnosis": diagnosis_result,
        "Scores": scores,
        "SEO": seo_data,
        "Strategy": arc
    }

    flow_steps = [
        "Fix Positioning + Offer Clarity",
        "Define Emotional Narrative Direction",
        "Month 1: Awareness Content Execution",
        "Month 2: Authority + Trust Building",
        "Strengthen Conversion Messaging",
        "Ad Film Concept Development",
        "Ad Film Production",
        "Launch with Funnel Push",
        "Scale Winning Creatives"
    ]

    pdf_buffer = pdf.generate(
        f"{brand_name} Strategy Report",
        client_inputs,
        results_data,
        flow_steps,
        logo_path="assets/logo.png"
    )

    st.download_button(
        label="Download PDF Report",
        data=pdf_buffer,
        file_name=f"{brand_name}_Report.pdf",
        mime="application/pdf"
    )


# -------------------------
# SAVED REPORTS
# -------------------------

st.sidebar.markdown("---")
st.sidebar.subheader("Saved Reports")

storage = ReportStorage()
reports = storage.list_reports()

if reports:

    selected_report = st.sidebar.selectbox("Select Report", reports)

    col1, col2, col3 = st.sidebar.columns(3)

    if col1.button("Load"):
        st.json(storage.load_report(selected_report))

    report_path = storage.get_report_path(selected_report)
    with open(report_path, "rb") as f:
        col2.download_button("Download", f, selected_report)

    if col3.button("Delete"):
        storage.delete_report(selected_report)
        st.rerun()