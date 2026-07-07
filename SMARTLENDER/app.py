import gradio as gr
import pandas as pd
from datetime import datetime

try:
    from reportlab.pdfgen import canvas
    PDF_AVAILABLE = True
except:
    PDF_AVAILABLE = False

def generate_pdf(name, score, status):
    if not PDF_AVAILABLE:
        return None
    filename = f"Eligibility_Report_{name.replace(' ', '_')}.pdf"
    c = canvas.Canvas(filename)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(100, 800, "Smart Lender Pro - Eligibility Report")
    c.setFont("Helvetica", 12)
    c.drawString(100, 770, f"Date: {datetime.now().strftime('%d %b %Y %H:%M')}")
    c.drawString(100, 740, f"Applicant: {name}")
    c.drawString(100, 710, f"Eligibility Score: {score}%")
    c.drawString(100, 680, f"Status: {status}")
    c.save()
    return filename

def predict(name, gender, married, education, employed, income, loan_amount, tenure):
    try:
        income_val = float(income)
        loan_val = float(loan_amount)
        tenure_val = float(tenure)
    except:
        return "Input Error", "₹0", "₹0K", "₹0", 0, 0, None

    credit_score = 650
    if employed == "Yes": credit_score += 100
    if income_val > 30000: credit_score += 50
    if education == "Graduate": credit_score += 30
    
    score = 0
    if employed == "Yes": score += 35
    if income_val > loan_val * 10: score += 35
    if education == "Graduate": score += 20
    if married == "Yes": score += 10
    eligibility = min(score, 100)
    
    roi = 10.5
    emi = (loan_val * 1000 * roi/12/100) / (1 - (1 + roi/12/100)**(-tenure_val)) if tenure_val > 0 else 0

    if eligibility >= 70:
        status = "PRE-APPROVED"
        status_html = f"""
        <div style='padding:35px; border-radius:20px; background:linear-gradient(135deg, #10B981 0%, #059669 100%); color:white; box-shadow:0 15px 40px rgba(16,185,129,0.4);'>
        <h2>✅ LOAN {status}</h2>
        <h3>Congratulations! You are eligible</h3>
        <p><b>Eligibility:</b> {eligibility}% | <b>Credit Score:</b> {credit_score}</p>
        <p><b>Est. EMI:</b> ₹{emi:,.0f} / month for {int(tenure_val)} months</p>
        </div>"""
    else:
        status = "REJECTED"
        status_html = f"""
        <div style='padding:35px; border-radius:20px; background:linear-gradient(135deg, #EF4444 0%, #DC2626 100%); color:white; box-shadow:0 15px 40px rgba(239,68,68,0.4);'>
        <h2>❌ LOAN {status}</h2>
        <h3>Not eligible at this time</h3>
        <p><b>Eligibility:</b> {eligibility}% | <b>Credit Score:</b> {credit_score}</p>
        <p>Improve Income, CIBIL or add Co-applicant</p>
        </div>"""

    pdf_file = generate_pdf(name, eligibility, status) if PDF_AVAILABLE else None
    return status_html, f"₹{income_val:,.0f}", f"₹{loan_val:,.0f}K", f"₹{emi:,.0f}", int(credit_score), eligibility, pdf_file

with gr.Blocks(title="Smart Lender Pro") as demo:
    
    gr.HTML("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap');
    .gradio-container {font-family: 'Outfit', sans-serif; background: #0F172A;}
    .header {
        background: linear-gradient(120deg, #0F172A 0%, #1E3A8A 50%, #0F172A 100%);
        padding: 40px;
        border-radius: 24px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        border: 1px solid rgba(96,165,250,0.2);
    }
    .header h1 {
        margin:0; font-size:38px; font-weight:700; 
        background: linear-gradient(90deg, #60A5FA, #34D399, #FBBF24); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
    }
    .glass-card {
        background: rgba(30,41,59,0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(96,165,250,0.2);
        border-radius: 18px;
        padding: 22px;
        transition: all 0.3s ease;
    }
    .glass-card:hover {transform: translateY(-6px); box-shadow: 0 15px 35px rgba(96,165,250,0.3);}
    .side-img {border-radius: 16px; border: 2px solid rgba(96,165,250,0.3);}
    </style>
    <div class="header">
        <h1>🏦 Smart Lender Pro</h1>
        <p style="opacity:0.85; margin-top:12px; font-size:15px;">AI-Powered Instant Loan Decisions • Bank Grade Security</p>
    </div>
    """)

    with gr.Row():
        # LEFT SIDE - BANK PHOTO
        with gr.Column(scale=1):
            gr.HTML("""
            <img class="side-img" src="https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=400" width="100%">
            <div style="margin-top:15px; padding:15px; background:rgba(30,41,59,0.6); border-radius:12px;">
                <h4 style="color:#60A5FA; margin:5px 0;">🏛️ Trusted Banking</h4>
                <p style="color:#94A3B8; font-size:13px;">RBI Approved • 256-bit SSL Secured</p>
            </div>
            """)
            
        # MIDDLE - MAIN CONTENT
        with gr.Column(scale=2):
            out_status = gr.HTML()
            
            with gr.Row():
                with gr.Column():
                    gr.HTML("<div class='glass-card'><h4 style='color:#34D399; margin:0;'>💰 Monthly Income</h4></div>")
                    card1 = gr.Textbox(show_label=False, interactive=False)
                with gr.Column():
                    gr.HTML("<div class='glass-card'><h4 style='color:#FBBF24; margin:0;'>🏠 Loan Amount</h4></div>")
                    card2 = gr.Textbox(show_label=False, interactive=False) 
                with gr.Column():
                    gr.HTML("<div class='glass-card'><h4 style='color:#60A5FA; margin:0;'>📈 Est. EMI</h4></div>")
                    card3 = gr.Textbox(show_label=False, interactive=False)

        # RIGHT SIDE - CREDIT CARD PHOTO
        with gr.Column(scale=1):
            gr.HTML("""
            <img class="side-img" src="https://images.unsplash.com/photo-1556740738-b6a63e27c4df?w=400" width="100%">
            <div style="margin-top:15px; padding:15px; background:rgba(30,41,59,0.6); border-radius:12px;">
                <h4 style="color:#FBBF24; margin:5px 0;">💳 Credit Benefits</h4>
                <p style="color:#94A3B8; font-size:13px;">Low Interest • Instant Approval</p>
            </div>
            """)
            gr.HTML("<div class='glass-card'><h4 style='color:#60A5FA; margin:0;'>📊 Credit Score</h4></div>")
            credit_gauge = gr.Slider(300, 900, value=650, label="", interactive=False, show_label=False)
            download_btn = gr.File(label="📄 Download Eligibility Report")

    with gr.Tabs():
        with gr.TabItem("📝 Application"):
            name = gr.Textbox(label="Full Name", placeholder="Enter your full name")
            with gr.Row():
                gender = gr.Radio(["Male", "Female"], label="Gender", value="Male")
                married = gr.Radio(["Yes", "No"], label="Married", value="No")
                education = gr.Radio(["Graduate", "Not Graduate"], label="Education", value="Graduate")
                employed = gr.Radio(["Yes", "No"], label="Self Employed", value="Yes")
            with gr.Row():
                income = gr.Slider(10000, 200000, value=40000, step=5000, label="Monthly Income (₹)")
                loan_amount = gr.Slider(50, 5000, value=500, step=50, label="Loan Amount (₹ in Thousands)")
                tenure = gr.Slider(12, 84, value=36, step=6, label="Loan Tenure (Months)")
            
            gr.Button("⚡ Get Instant Decision", variant="primary", size="lg").click(
                fn=predict, 
                inputs=[name, gender, married, education, employed, income, loan_amount, tenure], 
                outputs=[out_status, card1, card2, card3, credit_gauge, credit_gauge, download_btn]
            )

    gr.HTML("<div style='text-align:center; color:#94A3B8; padding:25px;'>© 2026 Smart Lender Pro | Powered by AI</div>")

demo.launch()