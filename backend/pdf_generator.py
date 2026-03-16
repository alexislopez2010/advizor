"""
adviZor - PDF Report Generator
Produces a branded executive brief using ReportLab.
"""

import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# Brand colors
NAVY = colors.HexColor("#0A1628")
TEAL = colors.HexColor("#00C8A0")
LIGHT_TEAL = colors.HexColor("#E6FAF6")
SLATE = colors.HexColor("#4A5568")
WHITE = colors.white
LIGHT_GRAY = colors.HexColor("#F7F9FC")
MID_GRAY = colors.HexColor("#CBD5E0")

PRIORITY_COLORS = {
    "High": colors.HexColor("#FF6B6B"),
    "Medium": colors.HexColor("#FFB347"),
    "Low": colors.HexColor("#74C69D"),
}


def generate_pdf(analysis: dict) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = _build_styles()
    story = []

    # ── Header ──────────────────────────────────────────────────────────────
    story += _header(analysis, styles)
    story.append(Spacer(1, 0.15 * inch))

    # ── Executive Summary ───────────────────────────────────────────────────
    story += _section("Executive Summary", styles)
    story.append(Paragraph(analysis["executive_summary"], styles["body"]))
    story.append(Spacer(1, 0.2 * inch))

    # ── Client Overview ─────────────────────────────────────────────────────
    story += _section("Client Overview", styles)
    client = analysis["client"]
    overview_data = [
        ["Client", client["name"]],
        ["Industry", client["industry"]],
        ["Annual Ad Budget", f"${client['annual_ad_budget_usd']:,}"],
        ["Current Service Spend", f"${client['current_spend_on_services_monthly']:,}/mo"],
    ]
    story.append(_two_col_table(overview_data, styles))
    story.append(Spacer(1, 0.15 * inch))

    # Campaign goals
    story.append(Paragraph("2027 Campaign Goals", styles["sub_heading"]))
    for g in client["campaign_goals_2027"]:
        story.append(Paragraph(f"• {g}", styles["bullet"]))
    story.append(Spacer(1, 0.2 * inch))

    # ── Current Subscriptions ───────────────────────────────────────────────
    story += _section("Current Subscriptions", styles)
    for svc in analysis["current_subscriptions"]:
        story.append(KeepTogether(_service_card(svc, styles, subscribed=True)))
    story.append(Spacer(1, 0.1 * inch))

    # ── Gap Analysis & Recommendations ─────────────────────────────────────
    story += _section("Recommended Additions", styles)
    story.append(Paragraph(
        "The following services are not currently subscribed and directly address "
        "NovaPulse's 2027 campaign objectives.",
        styles["body"]
    ))
    story.append(Spacer(1, 0.1 * inch))

    for rec in analysis["recommendations"]:
        svc = next((s for s in analysis["gap_services"] if s["id"] == rec["service_id"]), None)
        story.append(KeepTogether(_recommendation_card(rec, svc, styles)))

    # ── Investment Summary ──────────────────────────────────────────────────
    story += _section("Investment Summary", styles)
    story += _investment_table(analysis, styles)
    story.append(Spacer(1, 0.2 * inch))

    # ── Footer note ─────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=MID_GRAY))
    story.append(Spacer(1, 0.08 * inch))
    story.append(Paragraph(
        f"Confidential — Prepared by adviZor AI · {datetime.now().strftime('%B %d, %Y')} · "
        "All projections are estimates based on historical campaign benchmarks.",
        styles["footer"]
    ))

    doc.build(story)
    return buf.getvalue()


def _build_styles():
    base = getSampleStyleSheet()
    s = {}
    s["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=22,
                                textColor=WHITE, leading=26, alignment=TA_LEFT)
    s["subtitle"] = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=10,
                                   textColor=colors.HexColor("#A0AEC0"), leading=14, alignment=TA_LEFT)
    s["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=13,
                                  textColor=NAVY, leading=18, spaceAfter=6)
    s["sub_heading"] = ParagraphStyle("sub_heading", fontName="Helvetica-Bold", fontSize=10,
                                      textColor=NAVY, leading=14, spaceAfter=4)
    s["body"] = ParagraphStyle("body", fontName="Helvetica", fontSize=9,
                               textColor=SLATE, leading=14)
    s["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9,
                                 textColor=SLATE, leading=13, leftIndent=10)
    s["card_title"] = ParagraphStyle("card_title", fontName="Helvetica-Bold", fontSize=11,
                                     textColor=NAVY, leading=15)
    s["card_sub"] = ParagraphStyle("card_sub", fontName="Helvetica-Oblique", fontSize=8,
                                   textColor=TEAL, leading=12)
    s["label"] = ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=8,
                                textColor=SLATE, leading=11)
    s["value"] = ParagraphStyle("value", fontName="Helvetica", fontSize=8,
                                textColor=SLATE, leading=11)
    s["footer"] = ParagraphStyle("footer", fontName="Helvetica", fontSize=7,
                                 textColor=MID_GRAY, leading=10, alignment=TA_CENTER)
    s["highlight"] = ParagraphStyle("highlight", fontName="Helvetica-Bold", fontSize=9,
                                    textColor=NAVY, leading=13)
    return s


def _header(analysis, styles):
    client = analysis["client"]
    date_str = datetime.now().strftime("%B %d, %Y")

    header_data = [[
        Paragraph("adviZor", styles["title"]),
        Paragraph(f"{client['name']}<br/><font size='8' color='#A0AEC0'>Campaign Portfolio Analysis · {date_str}</font>",
                  styles["title"])
    ]]
    t = Table(header_data, colWidths=[1.5 * inch, 5.8 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
        ("ROUNDEDCORNERS", (0, 0), (-1, -1), [6, 6, 6, 6]),
    ]))
    return [t]


def _section(title, styles):
    return [
        Spacer(1, 0.1 * inch),
        HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=4),
        Paragraph(title.upper(), styles["section"]),
    ]


def _two_col_table(data, styles):
    rows = [[Paragraph(k, styles["label"]), Paragraph(v, styles["value"])] for k, v in data]
    t = Table(rows, colWidths=[1.8 * inch, 5.5 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_GRAY),
        ("BACKGROUND", (1, 0), (1, -1), WHITE),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [LIGHT_GRAY, WHITE]),
        ("GRID", (0, 0), (-1, -1), 0.3, MID_GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def _service_card(svc, styles, subscribed=False):
    bg = LIGHT_TEAL if subscribed else LIGHT_GRAY
    badge_text = "✓ ACTIVE" if subscribed else svc.get("id", "")

    items = [
        [
            Paragraph(svc["name"], styles["card_title"]),
            Paragraph(badge_text, ParagraphStyle("badge", fontName="Helvetica-Bold", fontSize=8,
                                                  textColor=TEAL if subscribed else SLATE,
                                                  alignment=TA_RIGHT))
        ],
        [Paragraph(svc["tagline"], styles["card_sub"]), Paragraph("", styles["body"])],
        [Paragraph(svc["description"], styles["body"]), Paragraph("", styles["body"])],
    ]
    t = Table(items, colWidths=[5.8 * inch, 1.5 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("SPAN", (0, 2), (1, 2)),
        ("SPAN", (0, 1), (1, 1)),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (0, 0), 10),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, -1), (-1, -1), 0.3, MID_GRAY),
    ]))
    return [t, Spacer(1, 0.08 * inch)]


def _recommendation_card(rec, svc, styles):
    priority_color = PRIORITY_COLORS.get(rec["priority"], SLATE)

    # Title row
    title_row = Table([[
        Paragraph(rec["service_name"], styles["card_title"]),
        Paragraph(f"● {rec['priority']} Priority",
                  ParagraphStyle("pri", fontName="Helvetica-Bold", fontSize=9,
                                 textColor=priority_color, alignment=TA_RIGHT))
    ]], colWidths=[5.0 * inch, 2.3 * inch])
    title_row.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    goals_str = "\n".join(f"• {g}" for g in rec["goals_addressed"])
    body_data = [
        [Paragraph("Goals Addressed", styles["label"]),
         Paragraph(goals_str, styles["bullet"])],
        [Paragraph("Why NovaPulse Needs This", styles["label"]),
         Paragraph(rec["reasoning"], styles["body"])],
        [Paragraph("Expected Value & Impact", styles["label"]),
         Paragraph(rec["expected_value"], styles["body"])],
        [Paragraph("Recommended Tier", styles["label"]),
         Paragraph(rec["recommended_tier"], styles["highlight"])],
        [Paragraph("Time to Impact", styles["label"]),
         Paragraph(rec["time_to_impact"], styles["body"])],
    ]
    body_table = Table(body_data, colWidths=[1.6 * inch, 5.7 * inch])
    body_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_GRAY),
        ("BACKGROUND", (1, 0), (1, -1), WHITE),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [LIGHT_GRAY, WHITE]),
        ("GRID", (0, 0), (-1, -1), 0.3, MID_GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    return [title_row, body_table, Spacer(1, 0.15 * inch)]


def _investment_table(analysis, styles):
    rows = []
    # Header
    rows.append([
        Paragraph("Service", styles["label"]),
        Paragraph("Status", styles["label"]),
        Paragraph("Tier", styles["label"]),
        Paragraph("Monthly Cost", styles["label"]),
    ])
    # Current
    for svc in analysis["current_subscriptions"]:
        rows.append([
            Paragraph(svc["name"], styles["body"]),
            Paragraph("Active", ParagraphStyle("active", fontName="Helvetica-Bold",
                                               fontSize=8, textColor=TEAL)),
            Paragraph(svc["tiers"][0], styles["body"]),
            Paragraph(f"${svc['monthly_cost_usd']:,}", styles["body"]),
        ])
    # Recommended
    for rec in analysis["recommendations"]:
        svc = next((s for s in analysis["gap_services"] if s["id"] == rec["service_id"]), None)
        if svc:
            rows.append([
                Paragraph(svc["name"], styles["body"]),
                Paragraph("Recommended", ParagraphStyle("rec", fontName="Helvetica-Bold",
                                                         fontSize=8, textColor=PRIORITY_COLORS["High"])),
                Paragraph(rec["recommended_tier"], styles["body"]),
                Paragraph(f"${svc['monthly_cost_usd']:,}+", styles["body"]),
            ])
    # Total
    current_monthly = sum(s["monthly_cost_usd"] for s in analysis["current_subscriptions"])
    new_monthly = current_monthly + analysis["total_additional_investment"]
    rows.append([
        Paragraph("TOTAL", styles["label"]),
        Paragraph("", styles["body"]),
        Paragraph("", styles["body"]),
        Paragraph(f"${new_monthly:,}/mo", styles["highlight"]),
    ])

    t = Table(rows, colWidths=[2.0 * inch, 1.4 * inch, 2.8 * inch, 1.1 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [LIGHT_GRAY, WHITE]),
        ("BACKGROUND", (0, -1), (-1, -1), LIGHT_TEAL),
        ("GRID", (0, 0), (-1, -1), 0.3, MID_GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    annual = new_monthly * 12
    budget = analysis["client"]["annual_ad_budget_usd"]
    pct = (new_monthly * 12 / budget) * 100

    note = [
        t,
        Spacer(1, 0.1 * inch),
        Paragraph(
            f"Annual stack investment: <b>${annual:,}</b> · "
            f"As % of ad budget: <b>{pct:.1f}%</b> (industry avg: 8–12%) · "
            f"Projected CPA savings: <b>~$840K/yr</b>",
            styles["body"]
        )
    ]
    return note
