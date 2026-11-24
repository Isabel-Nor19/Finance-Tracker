import streamlit as st
import traceback
import pandas as pd
from src.validator import validate_csv
from src.auditor import generate_summary

# 1. Page Configuration
st.set_page_config(page_title="BudgetGaze Auditor", page_icon="📊", layout="centered")

st.title("📊 BudgetGaze: Personal Finance Auditor")
st.markdown("Upload your raw banking CSV statement to clean, categorize, and audit your transactions instantly.")
st.divider()

# 2. File Upload Component
uploaded_file = st.file_uploader("Choose your bank statement CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Streamlit handles files in memory, so we pass the uploaded object directly
        cleaned_data = validate_csv(uploaded_file)
        
        # Run calculations
        income, spending, category_breakdown = generate_summary(cleaned_data)
        
        # 3. Present High-Level KPI Metrics side-by-side
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Total Income", value=f"£{income:.2f}")
        col2.metric(label="Total Spending", value=f"£{spending:.2f}")
        
        net_savings = income - spending
        if net_savings >= 0:
            col3.metric(label="Net Savings", value=f"£{net_savings:.2f}")
        else:
            col3.metric(label="Net Savings", value=f"£{net_savings:.2f}", delta="-Deficit")

        st.divider()
        
        # 4. Interactive Layout Splitting: Table on left, Graph on right
        tab1, tab2 = st.tabs(["📋 Data Breakdown", "📉 Visual Spending Chart"])
        
        with tab1:
            st.subheader("Spending Breakdown by Category")
            # Displays a beautiful, searchable interactive data table
            st.dataframe(category_breakdown, use_container_width=True)
            
            st.subheader("Sanitized Raw Records")
            st.dataframe(cleaned_data, use_container_width=True)
            
        with tab2:
            st.subheader("Spending Distribution")
            # Generates a clean native bar chart instantly from the dataframe
            st.bar_chart(data=category_breakdown, x="Category", y="Amount")
            
    except Exception as e:
        st.error(f"System Failure: {e}")
        st.info("Please ensure your CSV file columns are labeled exactly: Date, Description, Amount")

