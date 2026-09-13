import streamlit as st
from database.repository import list_findings

def render_findings(factory):
    st.title("⚠️ Findings")
    findings=list_findings(factory["id"])
    if not findings: st.info("No findings yet."); return
    for f in findings:
        with st.container(border=True):
            st.write(f"### {f['severity']} — {f['title']}")
            st.caption(f"{f['category']} • {f['status']} • {f['created_at']}")
            st.write(f["evidence"])
            st.write(f["explanation"])
            st.write("**Recommendation:**",f["recommendation"])
