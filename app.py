import streamlit as st
from fpdf import FPDF
import pandas as pd
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="SwiftBill - PDF Generator", page_icon="⚡")

# Custom CSS for a clean "Software" look
st.markdown("""
    <style>
    .stDownloadButton > button {
        background-color: #28a745 !important;
        color: white !important;
        width: 100%;
        height: 50px;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ SwiftBill")
st.subheader("Generate & Save Professional Invoices")

# --- DATA INPUT ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        biz_name = st.text_input("Your Company", "My Business LLC")
        biz_email = st.text_input("Your Email", "billing@example.com")
    with col2:
        client_name = st.text_input("Bill To (Client)", "Client Name")
        inv_date = st.date_input("Date", datetime.now())

# --- THE TABLE ---
st.write("### 📝 Items & Services")
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame([{"Description": "Consulting", "Qty": 1, "Rate": 100}])

edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)

# Calculation
subtotal = (edited_df['Qty'] * edited_df['Rate']).sum()
st.write(f"### **Total: ${subtotal:,.2f}**")

# --- THE PDF SAVE LOGIC ---
def export_as_pdf(df, biz, email, client, date, total):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 10, "INVOICE", ln=True, align='C')
    pdf.ln(10)
    
    # Header Info
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"From: {biz}", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Email: {email}", ln=True)
    pdf.cell(0, 10, f"Date: {date}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, f"Bill To: {client}", ln=True)
    pdf.ln(10)

    # Table
    pdf.set_fill_color(200, 220, 255)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(90, 10, " Description", border=1, fill=True)
    pdf.cell(30, 10, " Qty", border=1, fill=True)
    pdf.cell(30, 10, " Rate", border=1, fill=True)
    pdf.cell(30, 10, " Total", border=1, fill=True)
    pdf.ln()

    pdf.set_font("Arial", size=10)
    for i, row in df.iterrows():
        pdf.cell(90, 10, f" {row['Description']}", border=1)
        pdf.cell(30, 10, f" {row['Qty']}", border=1)
        pdf.cell(30, 10, f" ${row['Rate']}", border=1)
        pdf.cell(30, 10, f" ${row['Qty']*row['Rate']}", border=1)
        pdf.ln()

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"GRAND TOTAL: ${total:,.2f}", ln=True, align='R')
    
    return pdf.output(dest='S').encode('latin-1')

# --- THE SAVE BUTTON ---
st.write("---")
pdf_data = export_as_pdf(edited_df, biz_name, biz_email, client_name, inv_date, subtotal)

st.download_button(
    label="📥 SAVE INVOICE AS PDF",
    data=pdf_data,
    file_name=f"Invoice_{client_name}.pdf",
    mime="application/pdf"
)

st.caption("Tip: This will save directly to your computer/phone's Downloads folder.")
