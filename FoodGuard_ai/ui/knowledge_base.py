import streamlit as st
from rag.ingest import ingest_uploaded_documents
from database.repository import list_documents

def render_knowledge_base(factory):
    st.title("📚 Knowledge Base")
    st.caption("Upload factory-specific SOPs and procedures. These documents ground RAG answers.")
    doc_type=st.selectbox("Document type",["SOP","HACCP Plan","Product Specification","Procedure","Other"])
    files=st.file_uploader("Upload factory knowledge",type=["pdf","docx","txt"],accept_multiple_files=True)
    if st.button("Index documents",type="primary",disabled=not files):
        try:
            names,n=ingest_uploaded_documents(factory["id"],files,doc_type)
            st.success(f"Indexed {len(names)} document(s) and {n} knowledge chunks.")
        except Exception as e:
            st.error(f"Could not index the documents: {e}")
    st.subheader("Indexed documents")
    for d in list_documents(factory["id"]):
        st.write(f"📄 **{d['name']}** — {d['doc_type']} — {'✓ Indexed' if d['indexed'] else 'Not indexed'}")
