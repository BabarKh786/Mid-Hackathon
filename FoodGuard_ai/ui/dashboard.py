import streamlit as st
from database.repository import list_findings,list_actions,list_documents

def render_dashboard(factory):
    findings=list_findings(factory["id"]); actions=list_actions(factory["id"]); docs=list_documents(factory["id"])
    st.title("🛡️ FactoryGuard AI")
    st.caption(f"{factory['name']} • {factory['business_type']} • {factory['primary_product']}")
    c1,c2,c3,c4=st.columns(4)
    open_high=sum(1 for f in findings if f["severity"] in ["Critical","High"] and f["status"]!="Resolved")
    open_actions=sum(1 for a in actions if a["status"]!="Completed")
    with c1: st.metric("Documents",len(docs))
    with c2: st.metric("High/Critical Risks",open_high)
    with c3: st.metric("Open Actions",open_actions)
    with c4: st.metric("Analyses",len(findings))
    st.divider()
    st.subheader("⚠️ Priority Issues")
    if not findings: st.info("No findings yet. Start an AI Audit.")
    else:
        for f in findings[:5]:
            st.write(f"**{f['severity']} — {f['title']}**")
            st.caption(f["recommendation"])
