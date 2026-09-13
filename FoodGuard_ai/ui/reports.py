import streamlit as st
from reports.pdf_generator import build_report

def render_reports(factory):
    st.title("📄 Reports")
    if st.button("Generate FactoryGuard PDF Report",type="primary"):
        pdf=build_report(factory)
        st.download_button("Download report",data=pdf,file_name="factoryguard_report.pdf",mime="application/pdf")
    st.caption("Reports summarize findings and corrective actions stored in the application.")
