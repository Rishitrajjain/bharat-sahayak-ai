from fpdf import FPDF

def generate_pdf(profile, schemes):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=14)

    pdf.cell(200,10,"Bharat Sahayak AI Report",ln=True)

    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    pdf.cell(200,10,f"Income: Rs {profile['income']}",ln=True)
    pdf.cell(200,10,f"Occupation: {profile['occupation']}",ln=True)
    pdf.cell(200,10,f"State: {profile['state']}",ln=True)

    pdf.ln(10)

    pdf.cell(200,10,"Recommended Schemes:",ln=True)

    for s in schemes:

        pdf.cell(200,10,f"{s['name']} - {s['benefit']}",ln=True)

    pdf.output("schemes_report.pdf")

    return "schemes_report.pdf"