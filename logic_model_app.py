import streamlit as st
from logic_model_sandbox import LogicModel, Input, Activity, Output, Outcome, Impact

st.title("Logic Model Sandbox (Web Version)")

# Initialize or load model from session state
if "logic_model" not in st.session_state:
    st.session_state.logic_model = LogicModel("Web Logic Model")

lm = st.session_state.logic_model

# Sidebar: Add new components
st.sidebar.header("Add New Component")
comp_type = st.sidebar.selectbox("Type", ["Input", "Activity", "Output", "Outcome", "Impact"])
comp_name = st.sidebar.text_input("Name")
comp_desc = st.sidebar.text_area("Description")
if st.sidebar.button("Add Component"):
    comp_cls = {"Input": Input, "Activity": Activity, "Output": Output, "Outcome": Outcome, "Impact": Impact}[comp_type]
    comp = comp_cls(comp_name, comp_desc)
    lm.add_component(comp)
    st.sidebar.success(f"{comp_type} added.")

# List all components
st.header("Components")
for comp in lm._id_map.values():
    st.write(f"{comp.id} - {comp.name} ({comp.__class__.__name__})")

# Link components
st.subheader("Link Components")
from_id = st.number_input("From Component ID", min_value=0, step=1)
to_id = st.number_input("To Component ID", min_value=0, step=1)
if st.button("Link"):
    try:
        lm.get_component_by_id(from_id).add_link(lm.get_component_by_id(to_id))
        st.success("Linked!")
    except Exception as e:
        st.error(str(e))

# Visualize model
st.subheader("Visualize")
if st.button("Show Graph"):
    lm.visualize()

# Simulate
st.subheader("Simulate")
input_names = [i.name for i in lm.inputs]
if input_names:
    changed = {}
    for n in input_names:
        changed[n] = st.number_input(f"Value for {n}", value=1)
    if st.button("Run Simulation"):
        res = lm.simulate(changed)
        st.write(res)

# Validate
st.subheader("Validate Model")
if st.button("Validate"):
    validation = lm.validate()
    st.write(validation)

# Export
st.subheader("Export to JSON")
if st.button("Export"):
    json_str = lm.export_json()
    st.code(json_str, language="json")