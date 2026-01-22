import streamlit as st
from fpdf import FPDF
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="SwiftBill - Instant Invoices", page_icon="⚡")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div.stButton > button:first-child {
        background-color: #007BFF;
        color: white;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ SwiftBill")
st.markdown("Create professional PDF invoices in under 60 seconds.")

# --- STEP 1: BUSINESS SETUP ---
with st.expander("🏢 Step 1: Your Business Details", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        biz_name = st.text_input("Company Name", "My Business Ltd")
        biz_email = st.text_input("Support Email", "billing@example.com")
    with col2:
        client_name = st.text_input("Client Name", "Client Company Inc.")
        inv_date = st.date_input("Invoice Date", datetime.now())

# --- STEP 2: INVOICE ITEMS ---
st.write("### 📝 Step 2: Line Items")
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame([
        {"Description": "Work/Service Name", "Quantity": 1.0, "Unit Price": 100.0}
    ])

# Improved Data Editor
edited_df = st.data_editor(
    st.session_state.data, 
    num_rows="dynamic", 
    use_container_width=True
)

# Math Logic
subtotal = (edited_df['Quantity'] * edited_df['Unit Price']).sum()
tax_rate = st.slider("Tax Rate (%)", 0, 25, 0)
tax_total = subtotal * (tax_rate / 100)
grand_total = subtotal + tax_total

# Display Totals
c1, c2, c3 = st.columns(3)
c1.metric("Subtotal", f"${subtotal:,.2f}")
c2.metric("Tax", f"${tax_total:,.2f}")
c3.metric("Grand Total", f"${grand_total:,.2f}", delta_color="normal")

# --- STEP 3: GENERATE ---
st.write("### 🚀 Step 3: Finalize")

def create_pdf(df, biz, email, client, date, total_val):
    pdf = FPDF()
    pdf.add_page()
    
    # Branding
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(0, 123, 255) # SwiftBill Blue
    pdf.cell(0, 20, "INVOICE", ln=True, align='R')
    
    # Biz Info
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, biz, ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 7, f"Contact: {email}", ln=True)
    pdf.cell(0, 7, f"Date: {date}", ln=True)
    pdf.ln(10)
    
    # Client Info
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, f"BILL TO: {client}", ln=True)
    pdf.ln(5)
    
    # Table Header
    pdf.set_fill_color(0, 123, 255)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(90, 10, " Description", border=1, fill=True)
    pdf.cell(30, 10, " Qty", border=1, fill=True)
    pdf.cell(30, 10, " Price", border=1, fill=True)
    pdf.cell(30, 10, " Total", border=1, fill=True)
    pdf.ln()
    
    # Table Rows
    pdf.set_text_color(0, 0, 0)
    for _, row in df.iterrows():
        pdf.cell(90, 10, f" {row['Description']}", border=1)
        pdf.cell(30, 10, f" {row['Quantity']}", border=1)
        pdf.cell(30, 10, f" ${row['Unit Price']}", border=1)
        pdf.cell(30, 10, f" ${row['Quantity']*row['Unit Price']}", border=1)
        pdf.ln()
        
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"TOTAL DUE: ${total_val:,.2f}  ", ln=True, align='R')
    return pdf.output(dest='S').encode('latin-1')

if st.button("Generate Professional PDF"):
    try:
        pdf_output = create_pdf(edited_df, biz_name, biz_email, client_name, inv_date, grand_total)
        st.success("Your invoice is ready!")
        st.download_button(
            label="⬇️ Download Now",
            data=pdf_output,
            file_name=f"SwiftBill_{client_name}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Something went wrong: {e}")

# --- UPSELL ---
st.markdown("---")
st.write("🔒 **SwiftBill Pro**")
st.write("Remove the 'PDF' branding, add your company logo, and save client templates.")
st.link_button("Upgrade to Pro for $5", "https://your-payment-link.com")
