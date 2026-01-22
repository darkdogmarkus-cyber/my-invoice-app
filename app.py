import streamlit as st
from fpdf import FPDF
import pandas as pd

st.set_page_config(page_title="ProInvoice", page_icon="📄")

# --- DATA INITIALIZATION ---
# This prevents the ValueError by ensuring the data structure exists
if 'invoice_items' not in st.session_state:
    st.session_state.invoice_items = pd.DataFrame([
        {"Description": "Service 1", "Hours": 1.0, "Rate": 50.0}
    ])

st.title("📄 ProInvoice Generator")

# --- SIDEBAR ---
st.sidebar.header("Business Details")
biz_name = st.sidebar.text_input("Your Business Name", "My Company LLC")
biz_email = st.sidebar.text_input("Your Email", "billing@company.com")

st.sidebar.header("Client Details")
client_name = st.sidebar.text_input("Client Name", "Client Co.")

# --- MAIN INTERFACE ---
st.write("### Edit Invoice Items")
st.info("Double-click a cell to edit. Use the empty row at the bottom to add more.")

# The actual editor
edited_df = st.data_editor(
    st.session_state.invoice_items, 
    num_rows="dynamic",
    use_container_width=True
)

# Calculation Logic
subtotal = (edited_df['Hours'] * edited_df['Rate']).sum()
tax_rate = st.number_input("Tax Rate (%)", value=0.0, step=1.0)
tax_total = subtotal * (tax_rate / 100)
grand_total = subtotal + tax_total

st.write(f"**Grand Total:** ${grand_total:,.2f}")

# --- PDF GENERATOR FUNCTION ---
def create_pdf(df, biz, email, client, total_val):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, biz, ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Contact: {email}", ln=True)
    pdf.ln(10)
    
    # Client Info
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Bill To: {client}", ln=True)
    pdf.ln(5)
    
    # Table Header
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(90, 10, "Description", border=1, fill=True)
    pdf.cell(30, 10, "Hours", border=1, fill=True)
    pdf.cell(30, 10, "Rate", border=1, fill=True)
    pdf.cell(30, 10, "Total", border=1, fill=True)
    pdf.ln()
    
    # Table Rows
    pdf.set_font("Arial", size=10)
    for _, row in df.iterrows():
        pdf.cell(90, 10, str(row['Description']), border=1)
        pdf.cell(30, 10, str(row['Hours']), border=1)
        pdf.cell(30, 10, f"{row['Rate']}", border=1)
        pdf.cell(30, 10, f"{row['Hours']*row['Rate']}", border=1)
        pdf.ln()
        
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Grand Total: ${total_val:,.2f}", ln=True, align='R')
    return pdf.output(dest='S').encode('latin-1')

# --- DOWNLOAD ---
if st.button("Generate & Download PDF"):
    try:
        pdf_bytes = create_pdf(edited_df, biz_name, biz_email, client_name, grand_total)
        st.download_button(
            label="Click here to save file",
            data=pdf_bytes,
            file_name="invoice.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Error generating PDF: {e}")

# --- MONETIZATION ---
st.markdown("---")
st.write("⭐ **Pro Tip:** Want to remove the generic font and add your logo?")
st.link_button("Upgrade to Premium ($5)", "https://your-payment-link.com")
