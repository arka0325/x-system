"""
X System — PDF Report Generator
Replace your reports/pdf_report.py with this file.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
import io
from datetime import datetime


# ─────────────────────────────────────────
# COLOURS
# ─────────────────────────────────────────
WHITE      = colors.HexColor("#FFFFFF")
BLACK      = colors.HexColor("#0a0a0a")
ACCENT     = colors.HexColor("#7ab648")   # ArkX green
LIGHT_GREY = colors.HexColor("#f5f5f5")
MID_GREY   = colors.HexColor("#e0e0e0")
TEXT_GREY  = colors.HexColor("#555555")
DARK_GREY  = colors.HexColor("#222222")
OK_GREEN   = colors.HexColor("#2e9e5e")
WARN_ORG   = colors.HexColor("#d97706")
DANGER_RED = colors.HexColor("#dc2626")
ACCENT_BG  = colors.HexColor("#f0f7e8")


# ─────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────

def make_styles():
    return {
        "cover_brand": ParagraphStyle("cover_brand",
            fontName="Helvetica-Bold", fontSize=28,
            textColor=BLACK, leading=34, spaceAfter=6),

        "cover_sub": ParagraphStyle("cover_sub",
            fontName="Helvetica", fontSize=12,
            textColor=TEXT_GREY, leading=18, spaceAfter=4),

        "cover_meta": ParagraphStyle("cover_meta",
            fontName="Helvetica", fontSize=10,
            textColor=TEXT_GREY, leading=16),

        "section_label": ParagraphStyle("section_label",
            fontName="Helvetica-Bold", fontSize=8,
            textColor=ACCENT, leading=12, spaceAfter=4,
            spaceBefore=20, letterSpacing=1.5),

        "section_title": ParagraphStyle("section_title",
            fontName="Helvetica-Bold", fontSize=16,
            textColor=BLACK, leading=20, spaceAfter=12),

        "card_label": ParagraphStyle("card_label",
            fontName="Helvetica-Bold", fontSize=8,
            textColor=TEXT_GREY, leading=12, spaceAfter=3,
            letterSpacing=0.8),

        "card_value": ParagraphStyle("card_value",
            fontName="Helvetica", fontSize=11,
            textColor=DARK_GREY, leading=16, spaceAfter=2),

        "card_value_accent": ParagraphStyle("card_value_accent",
            fontName="Helvetica-Bold", fontSize=11,
            textColor=ACCENT, leading=16, spaceAfter=2),

        "body": ParagraphStyle("body",
            fontName="Helvetica", fontSize=10,
            textColor=TEXT_GREY, leading=16, spaceAfter=6),

        "bullet": ParagraphStyle("bullet",
            fontName="Helvetica", fontSize=10,
            textColor=TEXT_GREY, leading=16, spaceAfter=4,
            leftIndent=12, bulletIndent=0),

        "score_big": ParagraphStyle("score_big",
            fontName="Helvetica-Bold", fontSize=32,
            textColor=BLACK, leading=36, alignment=TA_CENTER),

        "score_label": ParagraphStyle("score_label",
            fontName="Helvetica", fontSize=8,
            textColor=TEXT_GREY, leading=12, alignment=TA_CENTER),

        "month_num": ParagraphStyle("month_num",
            fontName="Helvetica-Bold", fontSize=9,
            textColor=WHITE, leading=12),

        "month_title": ParagraphStyle("month_title",
            fontName="Helvetica-Bold", fontSize=13,
            textColor=BLACK, leading=18, spaceAfter=6),

        "footer": ParagraphStyle("footer",
            fontName="Helvetica", fontSize=8,
            textColor=TEXT_GREY, leading=12, alignment=TA_CENTER),

        "tag": ParagraphStyle("tag",
            fontName="Helvetica", fontSize=9,
            textColor=ACCENT, leading=12),
    }


# ─────────────────────────────────────────
# PAGE TEMPLATE WITH HEADER/FOOTER
# ─────────────────────────────────────────

class XReportCanvas(canvas.Canvas):
    def __init__(self, *args, brand_name="", logo_path=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.brand_name = brand_name
        self.logo_path = logo_path
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, total_pages):
        w, h = A4
        page_num = self._pageNumber

        # Top bar
        self.setFillColor(WHITE)
        self.rect(0, h - 14*mm, w, 14*mm, fill=1, stroke=0)
        # Top bar border bottom
        self.setStrokeColor(MID_GREY)
        self.setLineWidth(0.5)
        self.line(0, h - 14*mm, w, h - 14*mm)

        # ArkX logo image in top bar
        import os
        if self.logo_path and os.path.exists(self.logo_path):
            self.drawImage(
                self.logo_path,
                15*mm, h - 11.5*mm,
                width=28*mm, height=7*mm,
                preserveAspectRatio=True,
                mask="auto"
            )
        else:
            self.setFillColor(WHITE)
            self.setFont("Helvetica-Bold", 9)
            self.drawString(15*mm, h - 9*mm, "arkx")

        # Brand name in top bar (right)
        self.setFillColor(TEXT_GREY)
        self.setFont("Helvetica", 8)
        self.drawRightString(w - 15*mm, h - 9*mm, self.brand_name + " · Brand Intelligence Report")

        # Bottom bar
        self.setFillColor(LIGHT_GREY)
        self.rect(0, 0, w, 10*mm, fill=1, stroke=0)

        # Footer text
        self.setFillColor(TEXT_GREY)
        self.setFont("Helvetica", 7)
        self.drawString(15*mm, 3.5*mm, "Powered by X System · Arka Mukherjee · Confidential")
        self.drawRightString(w - 15*mm, 3.5*mm, f"Page {page_num} of {total_pages}")

        # Accent line under top bar
        self.setStrokeColor(ACCENT)
        self.setLineWidth(1.5)
        self.line(0, h - 14*mm, w, h - 14*mm)


# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────

def score_color_val(score):
    try:
        v = float(score)
        if v >= 70: return OK_GREEN
        if v >= 40: return WARN_ORG
        return DANGER_RED
    except:
        return WARN_ORG


def score_color_10(score):
    try:
        v = float(score)
        if v >= 7: return OK_GREEN
        if v >= 4: return WARN_ORG
        return DANGER_RED
    except:
        return WARN_ORG


def divider(color=MID_GREY, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=8, spaceBefore=4)


def section_header(label, title, S):
    return [
        divider(ACCENT, 1.5),
        Paragraph(label.upper(), S["section_label"]),
        Paragraph(title, S["section_title"]),
    ]


def bullet_item(text, S):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])


def info_card_table(pairs, S, col_count=2):
    """Render key-value pairs in a clean grey card grid."""
    rows = []
    row = []
    for i, (label, value) in enumerate(pairs):
        cell = [
            Paragraph(label, S["card_label"]),
            Paragraph(str(value) if value else "—", S["card_value"]),
        ]
        row.append(cell)
        if len(row) == col_count:
            rows.append(row)
            row = []
    if row:
        while len(row) < col_count:
            row.append([Paragraph("", S["card_label"]), Paragraph("", S["card_value"])])
        rows.append(row)

    # Flatten each cell into a mini-table
    flat_rows = []
    for row in rows:
        flat_row = []
        for cell in row:
            flat_row.append(Table(
                [[cell[0]], [cell[1]]],
                colWidths=["100%"],
                style=TableStyle([
                    ("BACKGROUND", (0,0), (-1,-1), LIGHT_GREY),
                    ("TOPPADDING", (0,0), (-1,-1), 6),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
                    ("LEFTPADDING", (0,0), (-1,-1), 8),
                    ("RIGHTPADDING", (0,0), (-1,-1), 8),
                    ("ROWBACKGROUNDS", (0,0), (-1,-1), [LIGHT_GREY]),
                ])
            ))
        flat_rows.append(flat_row)

    col_w = (A4[0] - 30*mm) / col_count
    t = Table(flat_rows, colWidths=[col_w - 2] * col_count,
              spaceBefore=6, spaceAfter=10)
    t.setStyle(TableStyle([
        ("LEFTPADDING",  (0,0), (-1,-1), 2),
        ("RIGHTPADDING", (0,0), (-1,-1), 2),
        ("TOPPADDING",   (0,0), (-1,-1), 2),
        ("BOTTOMPADDING",(0,0), (-1,-1), 2),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
    ]))
    return t


def score_grid(scores_dict, S):
    """Render pillar scores as a visual grid."""
    items = []
    for pillar, data in scores_dict.items():
        score = data.get("score", "—")
        reason = data.get("reason", "")
        label = pillar.replace("_", " ").title()
        color = score_color_val(score)

        cell = Table(
            [
                [Paragraph(str(score), ParagraphStyle("sc",
                    fontName="Helvetica-Bold", fontSize=28,
                    textColor=color, leading=32, alignment=TA_CENTER))],
                [Paragraph(label, S["score_label"])],
                [Paragraph(reason[:100] + ("…" if len(str(reason)) > 100 else ""),
                    ParagraphStyle("sr", fontName="Helvetica", fontSize=8,
                    textColor=TEXT_GREY, leading=12, alignment=TA_CENTER))],
            ],
            style=TableStyle([
                ("BACKGROUND", (0,0), (-1,-1), LIGHT_GREY),
                ("TOPPADDING",    (0,0), (-1,-1), 10),
                ("BOTTOMPADDING", (0,0), (-1,-1), 10),
                ("LEFTPADDING",   (0,0), (-1,-1), 8),
                ("RIGHTPADDING",  (0,0), (-1,-1), 8),
                ("LINEABOVE", (0,0), (-1,0), 2, color),
                ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ])
        )
        items.append(cell)

    # 2 per row
    rows = []
    for i in range(0, len(items), 2):
        row = items[i:i+2]
        while len(row) < 2:
            row.append(Paragraph("", S["body"]))
        rows.append(row)

    col_w = (A4[0] - 30*mm) / 2
    t = Table(rows, colWidths=[col_w - 2, col_w - 2], spaceBefore=8, spaceAfter=12)
    t.setStyle(TableStyle([
        ("LEFTPADDING",  (0,0), (-1,-1), 2),
        ("RIGHTPADDING", (0,0), (-1,-1), 2),
        ("TOPPADDING",   (0,0), (-1,-1), 2),
        ("BOTTOMPADDING",(0,0), (-1,-1), 2),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
    ]))
    return t


def month_card(month_num, title, focus_items, weekly_structure, color, S):
    """Render a single month strategy card."""
    badge_color = color

    # Badge
    badge = Table(
        [[Paragraph(f"MONTH {month_num}", ParagraphStyle("mb",
            fontName="Helvetica-Bold", fontSize=8, textColor=WHITE,
            leading=12, letterSpacing=1))]],
        style=TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), badge_color),
            ("TOPPADDING",    (0,0), (-1,-1), 4),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
            ("LEFTPADDING",   (0,0), (-1,-1), 10),
            ("RIGHTPADDING",  (0,0), (-1,-1), 10),
        ])
    )

    elements = [badge, Spacer(1, 6), Paragraph(str(title), S["month_title"])]

    if isinstance(focus_items, list):
        for item in focus_items:
            elements.append(bullet_item(str(item), S))
    elif focus_items:
        elements.append(Paragraph(str(focus_items), S["body"]))

    if weekly_structure and isinstance(weekly_structure, dict):
        elements.append(Spacer(1, 6))
        elements.append(Paragraph("WEEKLY STRUCTURE", S["card_label"]))
        for k, v in weekly_structure.items():
            label = k.replace("_", " ").title()
            elements.append(Paragraph(f"  {label}: {v} posts/week", S["body"]))

    card = Table(
        [[elements]],
        style=TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), LIGHT_GREY),
            ("TOPPADDING",    (0,0), (-1,-1), 14),
            ("BOTTOMPADDING", (0,0), (-1,-1), 14),
            ("LEFTPADDING",   (0,0), (-1,-1), 14),
            ("RIGHTPADDING",  (0,0), (-1,-1), 14),
            ("LINEABOVE",     (0,0), (-1,0), 2, badge_color),
        ]),
        spaceBefore=8, spaceAfter=8
    )
    return card


def flow_step(text, S, is_last=False):
    """Single flowchart step."""
    step = Table(
        [[Paragraph(str(text), ParagraphStyle("fs",
            fontName="Helvetica-Bold", fontSize=10,
            textColor=BLACK, leading=14, alignment=TA_CENTER))]],
        style=TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), LIGHT_GREY),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (-1,-1), 12),
            ("RIGHTPADDING",  (0,0), (-1,-1), 12),
            ("BOX",           (0,0), (-1,-1), 0.5, MID_GREY),
            ("LINEABOVE",     (0,0), (-1,0), 2, ACCENT),
        ]),
        colWidths=[A4[0] - 60*mm],
        spaceBefore=0, spaceAfter=0
    )
    arrow = Table(
        [[Paragraph("▼", ParagraphStyle("ar", fontName="Helvetica",
            fontSize=10, textColor=MID_GREY, leading=14, alignment=TA_CENTER))]],
        colWidths=[A4[0] - 60*mm],
    ) if not is_last else None

    return [step] + ([arrow] if arrow else [])


# ─────────────────────────────────────────
# MAIN PDF CLASS
# ─────────────────────────────────────────

class PDFReport:

    def generate(self, title, client_inputs, results_data, flow_steps, logo_path=None):
        buffer = io.BytesIO()
        brand_name = client_inputs.get("Brand Name", "Brand")

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=15*mm,
            rightMargin=15*mm,
            topMargin=20*mm,
            bottomMargin=16*mm,
        )

        S = make_styles()
        story = []

        # ── COVER PAGE ──
        story.append(Spacer(1, 20*mm))

        # Green accent bar
        cover_bar = Table(
            [[Paragraph("BRAND INTELLIGENCE REPORT", ParagraphStyle("cb",
                fontName="Helvetica-Bold", fontSize=8, textColor=WHITE,
                leading=12, letterSpacing=1.5))]],
            style=TableStyle([
                ("BACKGROUND",    (0,0), (-1,-1), ACCENT),
                ("TOPPADDING",    (0,0), (-1,-1), 6),
                ("BOTTOMPADDING", (0,0), (-1,-1), 6),
                ("LEFTPADDING",   (0,0), (-1,-1), 12),
                ("RIGHTPADDING",  (0,0), (-1,-1), 12),
            ]),
            colWidths=[A4[0] - 30*mm]
        )
        story.append(cover_bar)
        story.append(Spacer(1, 12))
        story.append(Paragraph(brand_name, S["cover_brand"]))
        story.append(Paragraph("Powered by X System · ArkX Intelligence", S["cover_sub"]))
        story.append(Spacer(1, 8))
        story.append(divider(MID_GREY))
        story.append(Spacer(1, 8))

        # Client meta grid
        meta_pairs = [
            ("Date", datetime.now().strftime("%d %b %Y")),
            ("Goal", client_inputs.get("Goal", "—")),
            ("Location", client_inputs.get("Location", "—")),
            ("Monthly Budget", f"₹{int(client_inputs.get('Monthly Budget', 0)):,}"),
            ("Service", client_inputs.get("Service", "—")),
            ("Brand Stage", client_inputs.get("Stage", "—")),
        ]
        story.append(info_card_table(meta_pairs, S, col_count=3))
        story.append(PageBreak())


        # ── BRAND INTELLIGENCE ──
        diag = results_data.get("Diagnosis", {})
        scores = results_data.get("Scores", {})
        seo = results_data.get("SEO", {})
        strategy = results_data.get("Strategy", [])

        story += section_header("01", "Brand Intelligence", S)

        current_problem = client_inputs.get("Current Problem", "—")
        if current_problem:
            story.append(Paragraph("Current Problem", S["card_label"]))
            story.append(Paragraph(current_problem, S["body"]))
            story.append(Spacer(1, 6))

        brand_pairs = [
            ("Strategic Mode", diag.get("primary_mode", "—")),
            ("Risk Level", diag.get("risk_level", "—")),
            ("Strategic Priority", diag.get("strategic_priority", "—")),
            ("Secondary Mode", diag.get("secondary_mode", "—")),
        ]
        story.append(info_card_table(brand_pairs, S, col_count=2))

        reasoning = diag.get("reasoning", "")
        if reasoning:
            story.append(Paragraph("Reasoning", S["card_label"]))
            story.append(Paragraph(str(reasoning), S["body"]))
            story.append(Spacer(1, 8))

        immediate = diag.get("immediate_actions", [])
        if immediate:
            story.append(Paragraph("Immediate Actions", S["card_label"]))
            for action in (immediate if isinstance(immediate, list) else [immediate]):
                story.append(bullet_item(str(action), S))
            story.append(Spacer(1, 8))


        # ── SEO INTELLIGENCE ──
        story += section_header("02", "SEO Intelligence", S)

        seo_score = seo.get("seo_health_score", "—")
        seo_color = score_color_val(seo_score)

        seo_score_cell = Table(
            [
                [Paragraph(str(seo_score), ParagraphStyle("ss",
                    fontName="Helvetica-Bold", fontSize=40,
                    textColor=seo_color, leading=44, alignment=TA_CENTER))],
                [Paragraph("SEO HEALTH SCORE / 100", S["score_label"])],
            ],
            style=TableStyle([
                ("BACKGROUND",    (0,0), (-1,-1), LIGHT_GREY),
                ("TOPPADDING",    (0,0), (-1,-1), 10),
                ("BOTTOMPADDING", (0,0), (-1,-1), 10),
                ("ALIGN",         (0,0), (-1,-1), "CENTER"),
                ("LINEABOVE",     (0,0), (-1,0), 2, seo_color),
            ]),
            colWidths=[50*mm]
        )

        seo_signals_content = [
            [Paragraph("Keyword Alignment", S["card_label"]),
             Paragraph(str(seo.get("keyword_alignment","—")), S["card_value"])],
            [Paragraph("Intent Match", S["card_label"]),
             Paragraph(str(seo.get("intent_match_quality","—")), S["card_value"])],
            [Paragraph("Ranking Risk", S["card_label"]),
             Paragraph(str(seo.get("ranking_risk","—")), S["card_value_accent"])],
        ]

        seo_signals = Table(seo_signals_content,
            colWidths=[35*mm, 60*mm],
            style=TableStyle([
                ("TOPPADDING",    (0,0), (-1,-1), 4),
                ("BOTTOMPADDING", (0,0), (-1,-1), 4),
                ("LINEBELOW",     (0,0), (-1,-2), 0.5, MID_GREY),
                ("VALIGN",        (0,0), (-1,-1), "TOP"),
            ]))

        seo_row = Table(
            [[seo_score_cell, seo_signals]],
            colWidths=[55*mm, A4[0] - 30*mm - 55*mm],
            style=TableStyle([
                ("LEFTPADDING",  (0,0), (-1,-1), 0),
                ("RIGHTPADDING", (0,0), (-1,-1), 0),
                ("TOPPADDING",   (0,0), (-1,-1), 0),
                ("BOTTOMPADDING",(0,0), (-1,-1), 0),
                ("LEFTPADDING",  (0,1), (0,1), 10),
                ("VALIGN",       (0,0), (-1,-1), "TOP"),
            ]),
            spaceBefore=8, spaceAfter=10
        )
        story.append(seo_row)

        seo_weaknesses = seo.get("seo_weaknesses", [])
        if seo_weaknesses:
            story.append(Paragraph("SEO Weaknesses", S["card_label"]))
            for w in (seo_weaknesses if isinstance(seo_weaknesses, list) else [seo_weaknesses]):
                story.append(bullet_item(str(w), S))
            story.append(Spacer(1, 8))

        seo_topics = seo.get("seo_topics", [])
        if seo_topics:
            story.append(Paragraph("Recommended Content Topics", S["card_label"]))
            topics_text = "  ·  ".join([
                t.get("title","") if isinstance(t, dict) else str(t)
                for t in seo_topics[:6]
            ])
            story.append(Paragraph(topics_text, S["tag"]))
            story.append(Spacer(1, 8))


        # ── PILLAR SCORES ──
        story += section_header("03", "Pillar Scores", S)
        if scores:
            story.append(score_grid(scores, S))

        story.append(PageBreak())


        # ── 90-DAY STRATEGY ──
        story += section_header("04", "90-Day Strategy", S)

        month_colors = [
            colors.HexColor("#1a1a1a"),
            colors.HexColor("#2e6b1a"),
            colors.HexColor("#1a3d6b"),
        ]

        if strategy and isinstance(strategy, list) and len(strategy) > 0:
            for i, month in enumerate(strategy):
                if isinstance(month, dict):
                    phase   = month.get("phase") or month.get("objective") or f"Phase {i+1}"
                    focus   = month.get("focus", [])
                    weekly  = month.get("weekly_structure", {})
                    m_num   = month.get("month", i + 1)
                    story.append(KeepTogether(
                        [month_card(m_num, phase, focus, weekly, month_colors[i % 3], S)]
                    ))
                else:
                    story.append(Paragraph(str(month), S["body"]))
        else:
            # Fallback from diagnosis
            immediate = diag.get("immediate_actions", [])
            mode      = diag.get("primary_mode", "Stabilize")
            priority  = diag.get("strategic_priority", "Growth")
            reasoning = diag.get("reasoning", "")

            fallback_months = [
                (1, f"Foundation — {mode}", immediate[:3] or ["Brand audit", "Messaging fix", "Content baseline"], {}, month_colors[0]),
                (2, f"Build — {priority}", immediate[3:6] or ["Content calendar", "SEO push", "Lead magnet"], {}, month_colors[1]),
                (3, "Scale — Conversion Push", ["Retargeting campaigns", "Case study content", "Performance review"], {}, month_colors[2]),
            ]
            for m_num, phase, focus, weekly, color in fallback_months:
                story.append(KeepTogether([month_card(m_num, phase, focus, weekly, color, S)]))


        # ── SIMPLIFIED FLOW ──
        story += section_header("05", "Simplified Strategy Flow", S)

        immediate = diag.get("immediate_actions", [])
        weeks = [
            ("Week 1–2",  immediate[:2]  if len(immediate) >= 2  else ["Brand audit & positioning review", "Fix core messaging"]),
            ("Week 3–4",  immediate[2:4] if len(immediate) >= 4  else ["Content calendar setup", "SEO baseline"]),
            ("Week 5–8",  ["Authority content push", "Lead magnet launch", "Paid test campaign"]),
            ("Week 9–12", ["Scale winning content", "Retargeting ads", "Monthly performance review"]),
        ]

        for week_label, posts in weeks:
            row_content = [[Paragraph(week_label, ParagraphStyle("wl",
                fontName="Helvetica-Bold", fontSize=9, textColor=ACCENT, leading=14))]]
            for p in posts:
                row_content.append([bullet_item(str(p), S)])

            week_table = Table(row_content,
                style=TableStyle([
                    ("BACKGROUND",    (0,0), (-1,-1), LIGHT_GREY),
                    ("TOPPADDING",    (0,0), (-1,-1), 4),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
                    ("LEFTPADDING",   (0,0), (-1,-1), 10),
                    ("RIGHTPADDING",  (0,0), (-1,-1), 10),
                    ("LINEABOVE",     (0,0), (-1,0), 2, ACCENT),
                ]),
                colWidths=[A4[0] - 30*mm],
                spaceBefore=6, spaceAfter=2
            )
            story.append(week_table)

        story.append(Spacer(1, 8))


        # ── STRATEGIC FLOWCHART ──
        story.append(PageBreak())
        story += section_header("06", "Strategic Execution Flowchart", S)

        dynamic_steps = []
        if diag.get("immediate_actions"):
            for action in diag["immediate_actions"][:3]:
                dynamic_steps.append(str(action))

        all_steps = dynamic_steps + [s for s in flow_steps if s not in dynamic_steps]

        center_table_rows = []
        for i, step_text in enumerate(all_steps):
            is_last = (i == len(all_steps) - 1)
            step_elems = flow_step(step_text, S, is_last)
            for elem in step_elems:
                row = Table([[elem]],
                    colWidths=[A4[0] - 30*mm],
                    style=TableStyle([
                        ("ALIGN", (0,0), (-1,-1), "CENTER"),
                        ("LEFTPADDING",  (0,0), (-1,-1), 0),
                        ("RIGHTPADDING", (0,0), (-1,-1), 0),
                        ("TOPPADDING",   (0,0), (-1,-1), 0),
                        ("BOTTOMPADDING",(0,0), (-1,-1), 0),
                    ])
                )
                center_table_rows.append([row])

        flow_table = Table(center_table_rows,
            colWidths=[A4[0] - 30*mm],
            style=TableStyle([
                ("ALIGN",        (0,0), (-1,-1), "CENTER"),
                ("LEFTPADDING",  (0,0), (-1,-1), 20*mm),
                ("RIGHTPADDING", (0,0), (-1,-1), 20*mm),
                ("TOPPADDING",   (0,0), (-1,-1), 1),
                ("BOTTOMPADDING",(0,0), (-1,-1), 1),
            ])
        )
        story.append(flow_table)


        # ── BUILD ──
        def make_canvas(filename, doc):
            return XReportCanvas(filename, pagesize=A4, brand_name=brand_name)

        doc.build(story, canvasmaker=lambda *a, **kw: XReportCanvas(*a, brand_name=brand_name, logo_path=logo_path, **kw))

        buffer.seek(0)
        return buffer.read()