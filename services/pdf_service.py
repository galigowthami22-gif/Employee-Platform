from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_payslip(payroll, employee, file_path):
    doc = SimpleDocTemplate(file_path)
    styles = (getSampleStyleSheet())
    elements = []
    elements.append(Paragraph("Employee Payslip", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Employee : {employee.first_name}", styles["Normal"]))
    elements.append(Paragraph(f"Payroll ID : {payroll.id}", styles["Normal"]))
    elements.append(Paragraph(f"Gross Salary : {payroll.gross_salary}", styles["Normal"]))
    elements.append(Paragraph(f"Deductions : {payroll.total_deductions}", styles["Normal"]))
    elements.append(Paragraph(f"Net Salary : {payroll.net_salary}", styles["Normal"]))
    doc.build(elements)
    return file_path