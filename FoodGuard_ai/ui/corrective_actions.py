import streamlit as st
from datetime import date
from database.repository import list_findings,list_actions,add_action,update_action

def render_corrective_actions(factory):
    st.title("📝 Corrective Actions")
    findings=list_findings(factory["id"])
    if findings:
        fopts={f"{f['severity']} — {f['title']}":f for f in findings}
        selected=st.selectbox("Create action for finding",list(fopts))
        f=fopts[selected]
        with st.form("action_form"):
            action=st.text_area("Immediate / corrective action *",value=f["recommendation"])
            preventive=st.text_area("Preventive action",value="")
            responsible=st.text_input("Responsible person",value="")
            due=st.date_input("Due date",value=date.today())
            ok=st.form_submit_button("Create Corrective Action",type="primary")
        if ok:
            if not action.strip(): st.error("Action is required.")
            else:
                add_action(factory["id"],f["id"],action,preventive,responsible,str(due))
                st.success("Corrective action created.")
    st.divider(); st.subheader("Action tracker")
    for a in list_actions(factory["id"]):
        with st.container(border=True):
            st.write(f"**{a['action']}**")
            st.caption(f"Due: {a['due_date']} • Responsible: {a['responsible'] or 'Not assigned'}")
            status=st.selectbox("Status",["Open","In Progress","Completed"],index=["Open","In Progress","Completed"].index(a["status"]),key=f"status_{a['id']}")
            evidence=st.text_input("Resolution evidence / note",value=a["evidence"] or "",key=f"ev_{a['id']}")
            if st.button("Save",key=f"save_{a['id']}"):
                update_action(a["id"],status,evidence); st.success("Saved.")
