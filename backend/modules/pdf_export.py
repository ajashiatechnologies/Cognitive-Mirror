from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import PageBreak
from io import BytesIO
from fastapi.responses import StreamingResponse

from reasoning_engine import analyze_reasoning
from modules.multi_agent import multi_agent_analysis


def generate_pdf(data):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    normal_style = styles["Normal"]

    # Run analysis
    base_result = analyze_reasoning(data)
    multi_result = multi_agent_analysis(data)

    # -----------------------
    # TITLE
    # -----------------------
    elements.append(Paragraph("CognitiveMirror Intelligence Report", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    # -----------------------
    # PROBLEM
    # -----------------------
    elements.append(Paragraph("<b>Problem Statement:</b>", styles["Heading2"]))
    elements.append(Paragraph(data.problem_statement, normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    # -----------------------
    # SCORES TABLE
    # -----------------------
    score_data = [
        ["Metric", "Score"],
        ["Overall Cognitive Score", str(base_result["overall_cognitive_score"])],
        ["Step Completeness", str(base_result["step_completeness_score"])],
        ["Logical Consistency", str(base_result["logical_consistency_score"])],
        ["Confidence Alignment", base_result["confidence_alignment"]],
        ["Cognitive Intelligence Index", str(round(multi_result["cognitive_intelligence_index"], 2))]
    ]

    table = Table(score_data, colWidths=[3 * inch, 2 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#813FF1")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.3 * inch))

    # -----------------------
    # LOGICAL GAPS
    # -----------------------
    elements.append(Paragraph("<b>Logical Gaps:</b>", styles["Heading2"]))
    gaps = base_result["logical_gaps"]

    if gaps:
        gap_items = [ListItem(Paragraph(f"Step {g['step_number']}: {g['issue']}", normal_style)) for g in gaps]
        elements.append(ListFlowable(gap_items))
    else:
        elements.append(Paragraph("No major logical gaps detected.", normal_style))

    elements.append(Spacer(1, 0.3 * inch))

    # -----------------------
    # BIAS ANALYSIS
    # -----------------------
    bias = multi_result["bias_agent"]

    elements.append(Paragraph("<b>Bias & Risk Analysis:</b>", styles["Heading2"]))
    elements.append(Paragraph(f"Confirmation Bias Risk: {bias['confirmation_bias_risk']}", normal_style))
    elements.append(Paragraph(f"Overconfidence Risk: {bias['overconfidence_risk']}", normal_style))
    elements.append(Paragraph(f"Emotional Reasoning Score: {bias['emotional_reasoning_score']}", normal_style))
    elements.append(Paragraph(f"Cognitive Risk Index: {bias['cognitive_risk_index']}", normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    # -----------------------
    # MENTOR MODE
    # -----------------------
    mentor = multi_result["mentor_mode"]

    elements.append(Paragraph("<b>AI Mentor Feedback:</b>", styles["Heading2"]))
    elements.append(Paragraph("<b>Strengths:</b>", normal_style))

    strengths = [ListItem(Paragraph(s, normal_style)) for s in mentor["strengths"]]
    elements.append(ListFlowable(strengths))

    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("<b>Improvement Areas:</b>", normal_style))
    improvements = [ListItem(Paragraph(s, normal_style)) for s in mentor["improvement_areas"]]
    elements.append(ListFlowable(improvements))

    elements.append(Spacer(1, 0.3 * inch))

    # -----------------------
    # SUMMARY
    # -----------------------
    elements.append(Paragraph("<b>AI Reasoning Summary:</b>", styles["Heading2"]))
    elements.append(Paragraph(base_result["reasoning_summary"], normal_style))

    doc.build(elements)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Cognitive_Report.pdf"}
    )