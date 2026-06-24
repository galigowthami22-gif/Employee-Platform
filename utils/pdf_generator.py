from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_payslip(file_path, payroll):
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    content = []
    content.append(Paragraph("Employee Payslip", styles["Title"]))
    content.append(Spacer(1, 20))
    content.append(Paragraph(f"Employee ID: {payroll.employee_id}", styles["Normal"]))
    content.append(Paragraph(f"Gross Salary: {payroll.gross_salary}", styles["Normal"]))
    content.append(Paragraph(f"Deductions: {payroll.total_deductions}", styles["Normal"]))
    content.append(Paragraph(f"Net Salary: {payroll.net_salary}", styles["Normal"]))
    doc.build(content)