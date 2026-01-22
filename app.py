import streamlit as st
from fpdf import FPDF
import pandas as pd

st.set_page_config(page_title="ProInvoice Generator", page_icon="📄")

st.title("📄 Professional Invoice Generator")
st.subheader("Create and download your invoice in seconds.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Your Business Info")
biz_name = st.sidebar.text_input("Business Name", "Your Company Name")
biz_email = st.sidebar.text_input("Business Email", "email@example.com")

st.sidebar.header("Client Info")
client_name = st.sidebar.text_input("Client Name", "Client Co.")
invoice_date = st.sidebar.date_input("Invoice Date")

# --- ITEM TABLE ---
st.write("### Line Items")
if 'items' not in st.session_state:
    st.session_state.items = [{"Description": "Consulting", "Hours": 1.0, "Rate": 50.0}]

df = pd.DataFrame(st.session_state.items)
edited_df = st.data_editor(df, num_rows="dynamic")

# Calculations
subtotal = (edited_df['Hours'] * edited_df['Rate']).sum()
tax_rate = st.number_input("Tax Rate (%)", value=0.0)
tax_amount = subtotal * (tax_rate / 100)
total = subtotal + tax_amount

st.write(f"**Subtotal:** ${subtotal:,.2f}")
st.write(f"**Total Due:** ${total:,.2f}")

# --- PDF GENERATION ---
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=biz_name, ln=True, align='L')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Email: {biz_email}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Bill To: {client_name}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {invoice_date}", ln=True)
    pdf.ln(10)

    # Table Header
    pdf.cell(90, 10, "Description", border=1)
    pdf.cell(30, 10, "Hours", border=1)
    pdf.cell(30, 10, "Rate", border=1)
    pdf.cell(30, 10, "Total", border=1)
    pdf.ln(10)

    # Table Rows
    pdf.set_font("Arial", size=10)
    for index, row in edited_df.iterrows():
        pdf.cell(90, 10, str(row['Description']), border=1)
        pdf.cell(30, 10, str(row['Hours']), border=1)
        pdf.cell(30, 10, f"${row['Rate']}", border=1)
        pdf.cell(30, 10, f"${row['Hours']*row['Rate']}", border=1)
        pdf.ln(10)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"TOTAL DUE: ${total:,.2f}", ln=True, align='R')
    
    return pdf.output(dest='S').encode('latin-1')

# --- DOWNLOAD BUTTON ---
pdf_data = generate_pdf()
st.download_button(
    label="📩 Download Invoice PDF",
    data=pdf_data,
    file_name="invoice.pdf",
    mime="application/pdf"
)

# --- MONETIZATION SECTION ---
st.markdown("---")
st.info("💡 **Want to add your logo and remove the watermark?** [Click here to upgrade to Pro for $5](your-payment-link-here)")
