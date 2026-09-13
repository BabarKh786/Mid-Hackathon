from io import BytesIO
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from database.repository import list_findings,list_actions

def build_report(factory):
    buf=BytesIO()
    doc=SimpleDocTemplate(buf)
    styles=getSampleStyleSheet()
    story=[Paragraph("FactoryGuard AI — Food Safety & Quality Report",styles["Title"]),
           Paragraph(f"{factory['name']} • {factory['business_type']} • {factory['primary_product']}",styles["Normal"]),Spacer(1,16)]
    findings=list_findings(factory["id"]); actions=list_actions(factory["id"])
    story.append(Paragraph(f"Total findings: {len(findings)}",styles["Heading2"]))
    if findings:
        data=[["Severity","Finding","Status"]]+[[f["severity"],f["title"],f["status"]] for f in findings]
        t=Table(data,repeatRows=1)
        t.setStyle(TableStyle([("GRID",(0,0),(-1,-1),.5,colors.grey),("BACKGROUND",(0,0),(-1,0),colors.lightgrey)]))
        story += [t,Spacer(1,14)]
    story.append(Paragraph(f"Corrective actions: {len(actions)}",styles["Heading2"]))
    for a in actions:
        story.append(Paragraph(f"<b>{a['status']}</b> — {a['action']} (Due: {a['due_date']})",styles["Normal"]))
        story.append(Spacer(1,6))
    doc.build(story)
    return buf.getvalue()
