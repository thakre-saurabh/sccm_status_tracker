"""
Run:
    pip install streamlit
    streamlit run demo_dashboard.py
"""

import time
import streamlit as st
from sccm_client import FakeSCCMClient
from qualys_client import FakeQualysClient

st.set_page_config(page_title="💻 SCCM Demo Dashboard", layout="wide")
st.title("📦 *Demo* SCCM + Qualys Deployment")

qid = st.text_input("Package / QID", value="12345")
total_devices = st.slider("How many devices should we simulate?", 10, 200, 50)
poll = st.number_input("Poll interval (seconds)", 1, 30, 3)

if st.button("🚀 Start Simulation") and qid:
    sccm = FakeSCCMClient(total_devices)
    qualys = FakeQualysClient()

    dep_id = sccm.get_deployment_id(qid)
    st.info(f"Monitoring **{dep_id}** — {total_devices} test devices")

    sccm_box = st.empty()
    qualys_box = st.empty()
    bar = st.progress(0)
    done = False

    while not done:
        status = sccm.get_status(dep_id)
        qstat = qualys.get_compliance_by_qid(
            qid, status["SuccessCount"], total_devices
        )

        # update widgets
        sccm_box.json(status)
        qualys_box.json(qstat)
        bar.progress(int(status["SuccessCount"] / total_devices * 100))

        done = status["SuccessCount"] >= total_devices
        time.sleep(poll)

    st.success("🎉 Simulation finished — 100 % success reached!")
