import streamlit as st
from pathlib import Path
from validation.input_validator import validate_upload
from analysis.router import analyze_input

OPTIONS={
"Temperature Records":["csv","xlsx","xls"],
"Cleaning Records":["csv","xlsx","xls"],
"SOP Review":["pdf","docx","txt"],
"HACCP Review":["pdf","docx","txt"],
"Inspection Report":["pdf","docx","txt"],
"Laboratory Report":["pdf","docx","txt","csv","xlsx","xls"],
"Visual Inspection":["jpg","jpeg","png","webp"]
}

def render_audit(factory):
    st.title("🔍 AI Audit")
    analysis_type=st.selectbox("What do you want to analyze?",list(OPTIONS))
    st.info("Only the selected analysis needs its own input. Missing modules do not stop other analyses.")
    extra={}
    if analysis_type=="Temperature Records":
        st.subheader("Required information")
        c1,c2=st.columns(2)
        with c1: extra["min"]=st.number_input("Minimum temperature (°C) *",value=0.0)
        with c2: extra["max"]=st.number_input("Maximum temperature (°C) *",value=5.0)
    uploaded=st.file_uploader("Upload required evidence *",type=OPTIONS[analysis_type])
    if uploaded:
        st.success(f"Ready: {uploaded.name}")
    if st.button("Run FactoryGuard Analysis",type="primary",disabled=uploaded is None):
        with st.status("Running analysis...",expanded=True) as status:
            try:
                result,sources=analyze_input(factory,analysis_type,uploaded,extra)
                st.session_state.last_result=result
                st.session_state.last_sources=sources
                status.update(label="Analysis completed",state="complete")
            except Exception as e:
                status.update(label="Analysis failed",state="error")
                st.error(str(e))
    result=st.session_state.get("last_result")
    if result:
        st.divider(); st.subheader("Analysis Result")
        st.write(result.get("summary",""))
        findings=result.get("findings",[])
        st.metric("Potential findings",len(findings))
        for i,f in enumerate(findings,1):
            with st.expander(f"{f.get('severity','Medium')} — {f.get('title','Finding')}"):
                st.write("**Evidence**"); st.write(f.get("evidence","Not available"))
                st.write("**Why flagged**"); st.write(f.get("explanation",""))
                st.write("**Recommended action**"); st.write(f.get("recommendation",""))
        missing=result.get("missing_information",[])
        if missing: st.warning("Missing information: " + "; ".join(map(str,missing)))
        sources=st.session_state.get("last_sources",[])
        if sources:
            st.subheader("📖 RAG Evidence")
            for s in sources:
                st.caption(f"{s['document_name']} • page {s['page']}")
                st.write(s["text"])
