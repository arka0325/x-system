"""
X System — Client Output Renderer
Place this file in your brand_os/ folder alongside app.py
"""

import streamlit as st


# ─────────────────────────────────────────
# INJECT GLOBAL CSS
# ─────────────────────────────────────────

def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    :root {
        --bg:        #05070f;
        --surface:   #0d1017;
        --border:    #1a1f2e;
        --accent:    #c8ff00;
        --accent2:   #00d4ff;
        --text:      #e8eaf0;
        --muted:     #6b7280;
        --danger:    #ff4d6d;
        --warn:      #ffb347;
        --ok:        #39d98a;
    }

    html, body, [class*="css"] {
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    h1, h2, h3, h4 {
        font-family: 'Syne', sans-serif !important;
        letter-spacing: -0.02em;
    }

    .stButton > button {
        background: transparent !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif !important;
        border-radius: 6px !important;
        transition: all 0.2s !important;
    }

    .stButton > button:hover {
        border-color: var(--accent) !important;
        color: var(--accent) !important;
    }

    .stSelectbox > div, .stTextInput > div > div, .stTextArea > div > div {
        background: var(--surface) !important;
        border-color: var(--border) !important;
        color: var(--text) !important;
        border-radius: 6px !important;
    }

    .stSidebar {
        background: var(--surface) !important;
        border-right: 1px solid var(--border) !important;
    }

    hr { border-color: var(--border) !important; }

    /* ── Cards ── */
    .x-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 24px 28px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }

    .x-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent), transparent);
    }

    .x-card-accent2::before {
        background: linear-gradient(90deg, var(--accent2), transparent);
    }

    .x-card-label {
        font-family: 'Syne', sans-serif;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 6px;
    }

    .x-card-title {
        font-family: 'Syne', sans-serif;
        font-size: 18px;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 12px;
    }

    .x-card-body {
        font-size: 14px;
        color: #9ca3af;
        line-height: 1.7;
    }

    /* ── Score Grid ── */
    .score-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 14px;
        margin-top: 16px;
    }

    .score-item {
        background: #0d1017;
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 20px 18px;
    }

    .score-number {
        font-family: 'Syne', sans-serif;
        font-size: 36px;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 6px;
    }

    .score-label {
        font-size: 11px;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 10px;
    }

    .score-reason {
        font-size: 12px;
        color: #6b7280;
        line-height: 1.6;
        white-space: normal;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }

    .score-high  { color: var(--ok); }
    .score-mid   { color: var(--warn); }
    .score-low   { color: var(--danger); }

    /* ── Month Cards ── */
    .month-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 28px;
        margin-bottom: 16px;
    }

    .month-badge {
        display: inline-block;
        background: var(--accent);
        color: #000;
        font-family: 'Syne', sans-serif;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.1em;
        padding: 4px 12px;
        border-radius: 4px;
        margin-bottom: 14px;
    }

    .month-objective {
        font-family: 'Syne', sans-serif;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 8px;
        color: var(--text);
    }

    /* ── Tags ── */
    .tag {
        display: inline-block;
        background: #1a1f2e;
        border: 1px solid var(--border);
        color: var(--text);
        font-size: 12px;
        padding: 4px 10px;
        border-radius: 20px;
        margin: 3px;
    }

    .tag-accent {
        background: rgba(200,255,0,0.08);
        border-color: rgba(200,255,0,0.3);
        color: var(--accent);
    }

    /* ── Qual Badge ── */
    .qual-badge {
        display: inline-block;
        font-family: 'Syne', sans-serif;
        font-size: 13px;
        font-weight: 700;
        padding: 6px 18px;
        border-radius: 6px;
        letter-spacing: 0.05em;
    }

    .qual-high   { background: rgba(57,217,138,0.12);  color: var(--ok);     border: 1px solid rgba(57,217,138,0.3); }
    .qual-medium { background: rgba(255,179,71,0.12);   color: var(--warn);   border: 1px solid rgba(255,179,71,0.3); }
    .qual-low    { background: rgba(255,77,109,0.12);   color: var(--danger); border: 1px solid rgba(255,77,109,0.3); }

    /* ── Section Header ── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 36px 0 20px;
    }

    .section-header-line {
        flex: 1;
        height: 1px;
        background: var(--border);
    }

    .section-header-label {
        font-family: 'Syne', sans-serif;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--muted);
        white-space: nowrap;
    }

    /* ── Hero ── */
    .report-hero {
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 40px;
        margin-bottom: 32px;
        background: linear-gradient(135deg, #0d1017 0%, #090c14 100%);
        position: relative;
        overflow: hidden;
    }

    .report-hero::after {
        content: 'X';
        position: absolute;
        right: 40px;
        top: 50%;
        transform: translateY(-50%);
        font-family: 'Syne', sans-serif;
        font-size: 120px;
        font-weight: 800;
        color: rgba(200,255,0,0.04);
        line-height: 1;
        pointer-events: none;
    }

    .report-brand {
        font-family: 'Syne', sans-serif;
        font-size: 36px;
        font-weight: 800;
        color: var(--text);
        margin-bottom: 6px;
        letter-spacing: -0.03em;
    }

    .report-subtitle {
        font-size: 14px;
        color: var(--muted);
    }

    .report-meta {
        display: flex;
        gap: 24px;
        margin-top: 20px;
        flex-wrap: wrap;
    }

    .report-meta-item {
        font-size: 12px;
        color: var(--muted);
    }

    .report-meta-item span {
        color: var(--text);
        font-weight: 500;
    }

    /* ── Issue List ── */
    .issue-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 1px solid var(--border);
        font-size: 14px;
        color: #9ca3af;
        line-height: 1.6;
    }

    .issue-item:last-child { border-bottom: none; }

    .issue-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        margin-top: 8px;
        flex-shrink: 0;
    }

    /* ── Simple Flow ── */
    .flow-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 14px;
    }

    .flow-week {
        font-family: 'Syne', sans-serif;
        font-size: 13px;
        font-weight: 700;
        color: var(--accent);
        margin-bottom: 10px;
        letter-spacing: 0.05em;
    }

    .flow-post {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 8px 0;
        border-bottom: 1px solid var(--border);
        font-size: 13px;
        color: #9ca3af;
    }

    .flow-post:last-child { border-bottom: none; }

    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────

def section_header(label):
    st.markdown(f"""
    <div class="section-header">
        <div class="section-header-line"></div>
        <div class="section-header-label">{label}</div>
        <div class="section-header-line"></div>
    </div>
    """, unsafe_allow_html=True)


def score_color(score):
    try:
        v = float(score)
        if v >= 70: return "score-high"
        if v >= 40: return "score-mid"
        return "score-low"
    except:
        return "score-mid"


def score_color_10(score):
    try:
        v = float(score)
        if v >= 7: return "score-high"
        if v >= 4: return "score-mid"
        return "score-low"
    except:
        return "score-mid"


def qual_class(status):
    s = str(status).lower()
    if any(x in s for x in ["high", "strong", "qualified", "ready"]): return "qual-high"
    if any(x in s for x in ["medium", "moderate", "conditional"]):     return "qual-medium"
    return "qual-low"


def render_list_items(items, dot_color="var(--accent)"):
    if not items:
        return ""
    if isinstance(items, str):
        items = [items]
    html = ""
    for item in items:
        if isinstance(item, dict):
            item = str(item)
        html += f"""
        <div class="issue-item">
            <div class="issue-dot" style="background:{dot_color}"></div>
            <div>{item}</div>
        </div>"""
    return html


# ─────────────────────────────────────────
# STRATEGY FALLBACK (when arc = [])
# ─────────────────────────────────────────

def render_strategy_from_diagnosis(diagnosis_result):
    immediate = diagnosis_result.get("immediate_actions", [])
    priority  = diagnosis_result.get("strategic_priority", "Growth")
    mode      = diagnosis_result.get("primary_mode", "Stabilize")
    reasoning = diagnosis_result.get("reasoning", "")

    months = [
        {
            "num": 1, "color": "var(--accent)", "text": "#000",
            "objective": f"Foundation — {mode}",
            "focus": reasoning[:140] + "…" if len(reasoning) > 140 else reasoning,
            "actions": immediate[:3] if immediate else ["Define brand positioning", "Fix core messaging", "Audit current content"]
        },
        {
            "num": 2, "color": "var(--accent2)", "text": "#fff",
            "objective": f"Build — {priority}",
            "focus": "Execute on validated positioning. Build authority content pipeline.",
            "actions": immediate[3:6] if len(immediate) > 3 else ["Launch content calendar", "SEO implementation", "Lead magnet creation"]
        },
        {
            "num": 3, "color": "#ff6b6b", "text": "#fff",
            "objective": "Scale — Conversion Push",
            "focus": "Amplify what's working. Push paid + organic together for maximum reach.",
            "actions": ["Retargeting campaigns", "Case study content", "Performance review + scale"]
        }
    ]

    for m in months:
        action_html = render_list_items(m["actions"], m["color"])
        st.markdown(f"""
        <div class="month-card">
            <div class="month-badge" style="background:{m['color']}; color:{m['text']}">MONTH {m['num']}</div>
            <div class="month-objective">{m['objective']}</div>
            <div class="x-card-body" style="margin-bottom:14px">{m['focus']}</div>
            {action_html}
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# MAIN RENDERER
# ─────────────────────────────────────────

def render_client_report(
    brand_data,
    seo_data,
    scores,
    diagnosis_result,
    arc,
    qualification_result,
    brand_name,
    client_goal=None,
    lifecycle_stage=None,
    monthly_budget=None
):
    inject_styles()

    from datetime import datetime
    date_str = datetime.now().strftime("%d %b %Y")

    # ── HERO ──
    st.markdown(f"""
    <div class="report-hero">
        <div class="x-card-label">Brand Intelligence Report</div>
        <div class="report-brand">{brand_name}</div>
        <div class="report-subtitle">Generated by X System · ArkX Intelligence</div>
        <div class="report-meta">
            <div class="report-meta-item">Date <span>{date_str}</span></div>
            {"<div class='report-meta-item'>Goal <span>" + str(client_goal) + "</span></div>" if client_goal else ""}
            {"<div class='report-meta-item'>Stage <span>" + str(lifecycle_stage) + "</span></div>" if lifecycle_stage else ""}
            {"<div class='report-meta-item'>Budget <span>₹" + f"{int(monthly_budget):,}" + "/mo</span></div>" if monthly_budget else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)


    # ── BRAND INTELLIGENCE ──
    section_header("Brand Intelligence")

    industry       = brand_data.get("industry", "—")
    business_model = brand_data.get("business_model", "—")
    target         = brand_data.get("target_audience", "—")
    value_prop     = brand_data.get("value_proposition", "—")
    tone           = brand_data.get("tone", "—")
    strengths      = brand_data.get("strengths", [])
    weaknesses     = brand_data.get("weaknesses", [])
    diag_summary   = brand_data.get("diagnostic_summary", "—")
    offer_score    = brand_data.get("offer_clarity_score", "—")
    cta_strength   = brand_data.get("CTA_strength", "—")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="x-card">
            <div class="x-card-label">Value Proposition</div>
            <div class="x-card-body">{value_prop}</div>
        </div>
        <div class="x-card">
            <div class="x-card-label">Target Audience</div>
            <div class="x-card-body">{target}</div>
        </div>
        <div class="x-card">
            <div class="x-card-label">Industry · Business Model</div>
            <div class="x-card-body">{industry} · {business_model}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="x-card">
            <div class="x-card-label">Brand Tone</div>
            <div class="x-card-body">{tone}</div>
        </div>
        <div class="x-card">
            <div class="x-card-label">Offer Clarity · CTA Strength</div>
            <div style="display:flex; gap:32px; margin-top:8px">
                <div>
                    <div class="score-number {score_color_10(offer_score)}" style="font-size:32px">{offer_score}</div>
                    <div class="score-label">Offer Clarity /10</div>
                </div>
                <div>
                    <div class="score-number {score_color_10(cta_strength)}" style="font-size:32px">{cta_strength}</div>
                    <div class="score-label">CTA Strength /10</div>
                </div>
            </div>
        </div>
        <div class="x-card">
            <div class="x-card-label">Diagnostic Summary</div>
            <div class="x-card-body">{diag_summary}</div>
        </div>
        """, unsafe_allow_html=True)

    if strengths:
        st.markdown(f"""
        <div class="x-card">
            <div class="x-card-label">Strengths</div>
            <div class="x-card-body">{render_list_items(strengths, "var(--ok)")}</div>
        </div>
        """, unsafe_allow_html=True)

    if weaknesses:
        st.markdown(f"""
        <div class="x-card">
            <div class="x-card-label">Weaknesses</div>
            <div class="x-card-body">{render_list_items(weaknesses, "var(--danger)")}</div>
        </div>
        """, unsafe_allow_html=True)


    # ── SEO INTELLIGENCE ──
    section_header("SEO Intelligence")

    seo_score      = seo_data.get("seo_health_score", "—")
    kw_alignment   = seo_data.get("keyword_alignment", "—")
    intent_quality = seo_data.get("intent_match_quality", "—")
    ranking_risk   = seo_data.get("ranking_risk", "—")
    seo_weaknesses = seo_data.get("seo_weaknesses", [])
    seo_topics     = seo_data.get("seo_topics", [])

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
        <div class="x-card" style="text-align:center; padding:32px;">
            <div class="x-card-label">SEO Health Score</div>
            <div class="score-number {score_color(seo_score)}" style="font-size:52px">{seo_score}</div>
            <div class="score-label">out of 100</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="x-card">
            <div class="x-card-label">SEO Signals</div>
            <div style="display:flex; gap:32px; margin-top:10px; flex-wrap:wrap">
                <div>
                    <div class="score-label">Keyword Alignment</div>
                    <div style="font-family:'Syne',sans-serif; font-size:17px; font-weight:700; color:var(--text)">{kw_alignment}</div>
                </div>
                <div>
                    <div class="score-label">Intent Match</div>
                    <div style="font-family:'Syne',sans-serif; font-size:17px; font-weight:700; color:var(--text)">{intent_quality}</div>
                </div>
                <div>
                    <div class="score-label">Ranking Risk</div>
                    <div style="font-family:'Syne',sans-serif; font-size:17px; font-weight:700; color:var(--warn)">{ranking_risk}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if seo_weaknesses:
        st.markdown(f"""
        <div class="x-card">
            <div class="x-card-label">SEO Weaknesses</div>
            <div class="x-card-body">{render_list_items(seo_weaknesses, "var(--warn)")}</div>
        </div>
        """, unsafe_allow_html=True)

    if seo_topics:
        topic_tags = "".join([
            f'<span class="tag tag-accent">{t.get("title","") if isinstance(t, dict) else t}</span>'
            for t in seo_topics[:6]
        ])
        st.markdown(f"""
        <div class="x-card">
            <div class="x-card-label">Recommended Content Topics</div>
            <div style="margin-top:10px">{topic_tags}</div>
        </div>
        """, unsafe_allow_html=True)


    # ── PILLAR SCORES ──
    section_header("Pillar Scores")

    score_html = '<div class="score-grid">'
    for pillar, data in scores.items():
        s   = data.get("score", "—")
        r   = data.get("reason", "")
        cls = score_color(s)
        label = pillar.replace("_", " ").title()
        score_html += f"""
        <div class="score-item">
            <div class="score-number {cls}">{s}</div>
            <div class="score-label">{label}</div>
            <div class="score-reason">{r}</div>
        </div>"""
    score_html += "</div>"
    st.markdown(score_html, unsafe_allow_html=True)


    # ── DIAGNOSIS ──
    section_header("Diagnosis")

    primary_mode      = diagnosis_result.get("primary_mode", "—")
    secondary_mode    = diagnosis_result.get("secondary_mode", "—")
    strat_priority    = diagnosis_result.get("strategic_priority", "—")
    risk_level        = diagnosis_result.get("risk_level", "—")
    immediate_actions = diagnosis_result.get("immediate_actions", [])
    reasoning         = diagnosis_result.get("reasoning", "—")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="x-card">
            <div class="x-card-label">Strategic Mode</div>
            <div class="x-card-title">{primary_mode}</div>
            <div class="x-card-body">Secondary: {secondary_mode}</div>
        </div>
        <div class="x-card">
            <div class="x-card-label">Strategic Priority</div>
            <div style="font-family:'Syne',sans-serif; font-size:18px; font-weight:700; color:var(--accent); margin-top:6px">{strat_priority}</div>
        </div>
        <div class="x-card">
            <div class="x-card-label">Risk Level</div>
            <div style="font-family:'Syne',sans-serif; font-size:18px; font-weight:700; color:var(--warn); margin-top:6px">{risk_level}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="x-card">
            <div class="x-card-label">Reasoning</div>
            <div class="x-card-body">{reasoning}</div>
        </div>
        """, unsafe_allow_html=True)
        if immediate_actions:
            st.markdown(f"""
            <div class="x-card x-card-accent2">
                <div class="x-card-label">Immediate Actions</div>
                <div class="x-card-body">{render_list_items(immediate_actions, "var(--accent2)")}</div>
            </div>
            """, unsafe_allow_html=True)


    # ── CLIENT QUALIFICATION ──
    section_header("Client Qualification")

    q_score   = qualification_result.get("qualification_score", "—")
    q_status  = qualification_result.get("qualification_status", "—")
    q_model   = qualification_result.get("engagement_model", "—")
    q_summary = qualification_result.get("recommendation_summary", "")
    risk_flags = qualification_result.get("risk_flags", [])
    q_cls     = qual_class(q_status)

    st.markdown(f"""
    <div class="x-card">
        <div style="display:flex; align-items:center; gap:32px; flex-wrap:wrap; margin-bottom:16px">
            <div>
                <div class="x-card-label">Qualification Score</div>
                <div class="score-number {score_color(q_score)}" style="font-size:52px">{q_score}</div>
            </div>
            <div>
                <div class="x-card-label">Status</div>
                <div class="qual-badge {q_cls}" style="margin-top:6px">{q_status}</div>
            </div>
            <div>
                <div class="x-card-label">Engagement Model</div>
                <div style="font-family:'Syne',sans-serif; font-size:18px; font-weight:700; margin-top:6px; color:var(--text)">{q_model}</div>
            </div>
        </div>
        {('<div class="x-card-body">' + q_summary + '</div>') if q_summary else ''}
    </div>
    """, unsafe_allow_html=True)

    if risk_flags:
        st.markdown(f"""
        <div class="x-card">
            <div class="x-card-label">Risk Flags</div>
            <div class="x-card-body">{render_list_items(risk_flags, "var(--danger)")}</div>
        </div>
        """, unsafe_allow_html=True)


    # ── 90-DAY STRATEGY ──
    section_header("90-Day Strategy")

    if arc and isinstance(arc, list) and len(arc) > 0:
        colors = [
            ("var(--accent)", "#000"),
            ("var(--accent2)", "#fff"),
            ("#ff6b6b", "#fff"),
        ]
        for i, month in enumerate(arc):
            color, text_color = colors[i % len(colors)]
            if isinstance(month, dict):
                phase   = month.get("phase") or month.get("objective") or month.get("goal", f"Phase {i+1}")
                focus   = month.get("focus", [])
                weekly  = month.get("weekly_structure", {})
                m_num   = month.get("month", i + 1)

                focus_html = render_list_items(focus, color) if isinstance(focus, list) else f'<div class="x-card-body">{focus}</div>'

                weekly_html = ""
                if weekly:
                    weekly_html = '<div style="margin-top:16px"><div class="x-card-label" style="margin-bottom:10px">Weekly Post Structure</div>'
                    for k, v in weekly.items():
                        label = k.replace("_", " ").title()
                        weekly_html += f'<div class="issue-item"><div class="issue-dot" style="background:{color}"></div><div>{label}: <strong style="color:var(--text)">{v} posts/week</strong></div></div>'
                    weekly_html += "</div>"

                st.markdown(f"""
                <div class="month-card">
                    <div class="month-badge" style="background:{color}; color:{text_color}">MONTH {m_num}</div>
                    <div class="month-objective">{phase}</div>
                    <div style="margin-top:12px">{focus_html}</div>
                    {weekly_html}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="month-card">
                    <div class="month-badge" style="background:{color}; color:{text_color}">MONTH {i+1}</div>
                    <div class="x-card-body">{str(month)}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        render_strategy_from_diagnosis(diagnosis_result)


    # ── SIMPLIFIED STRATEGY FLOW ──
    section_header("Simplified Strategy Flow")

    immediate_actions = diagnosis_result.get("immediate_actions", [])

    weeks = [
        {
            "week": "Week 1–2",
            "posts": immediate_actions[:2] if len(immediate_actions) >= 2 else ["Brand audit & positioning review", "Fix core messaging & offer clarity"]
        },
        {
            "week": "Week 3–4",
            "posts": immediate_actions[2:4] if len(immediate_actions) >= 4 else ["Content calendar setup", "SEO baseline & keyword targeting"]
        },
        {
            "week": "Week 5–8",
            "posts": ["Authority content push", "Lead magnet launch", "Paid test campaign (small budget)"]
        },
        {
            "week": "Week 9–12",
            "posts": ["Scale winning content formats", "Retargeting ads to warm audience", "Monthly performance review + optimise"]
        },
    ]

    for w in weeks:
        posts_html = "".join([
            f'<div class="flow-post"><div class="issue-dot" style="background:var(--accent); margin-top:6px; flex-shrink:0"></div><div>{p}</div></div>'
            for p in w["posts"]
        ])
        st.markdown(f"""
        <div class="flow-card">
            <div class="flow-week">{w['week']}</div>
            {posts_html}
        </div>
        """, unsafe_allow_html=True)


    # ── FOOTER ──
    st.markdown("""
    <div style="margin-top:56px; padding-top:24px; border-top:1px solid var(--border);
                display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px">
        <div style="font-family:'Syne',sans-serif; font-size:13px; color:var(--muted)">
            Powered by <span style="color:var(--accent); font-weight:700">X System</span> · Arka Mukherjee
        </div>
        <div style="font-size:12px; color:var(--muted)">Confidential · For client use only</div>
    </div>
    """, unsafe_allow_html=True)