"""
Logic Model Sandbox for Program Evaluation and Planning

This module provides a flexible framework to define, simulate, and analyze logic models
for program evaluation and planning. It supports defining the standard components of a 
logic model—inputs, activities, outputs, outcomes, and impacts—each as a class, and 
offers functionality for visualization, validation, scenario testing, and export.

Usage:
    Analysts and evaluators can instantiate the LogicModel class, add components, 
    define relationships, simulate changes, and export configurations.

Author: Copilot
Date: 2025-07-30
"""

import json
from typing import List, Dict, Optional, Any, Set
import networkx as nx
import matplotlib.pyplot as plt

# Core logic model components

class LogicComponent:
    """
    Base class for logic model components.
    Each component has a name, description, and a unique ID.
    """
    _id_counter = 0

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.id = LogicComponent._id_counter
        LogicComponent._id_counter += 1
        # Store links to next components (dependencies)
        self.links: List['LogicComponent'] = []

    def add_link(self, component: 'LogicComponent'):
        """Link this component to another (e.g., activity to output)."""
        if component not in self.links:
            self.links.append(component)

    def to_dict(self) -> dict:
        """Serialize the component for export."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__,
            "links": [c.id for c in self.links]
        }

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"

class Input(LogicComponent):
    """Resources used by the program (e.g., funding, staff)."""

class Activity(LogicComponent):
    """Actions taken or work performed using inputs."""

class Output(LogicComponent):
    """Direct products or services resulting from activities."""

class Outcome(LogicComponent):
    """Short- or medium-term results or changes (e.g., knowledge, behavior)."""

class Impact(LogicComponent):
    """Long-term, fundamental changes (e.g., community health, policy)."""

# Logic model container and engine

class LogicModel:
    """
    Aggregates all components and supports scenario testing, visualization, validation, and export.
    """

    def __init__(self, name: str = "Logic Model"):
        self.name = name
        # Store all components by type
        self.inputs: List[Input] = []
        self.activities: List[Activity] = []
        self.outputs: List[Output] = []
        self.outcomes: List[Outcome] = []
        self.impacts: List[Impact] = []
        # Map ID to component for quick lookup
        self._id_map: Dict[int, LogicComponent] = {}

    def add_component(self, component: LogicComponent):
        """Add a component to the model and register in the ID map."""
        comp_list = {
            Input: self.inputs,
            Activity: self.activities,
            Output: self.outputs,
            Outcome: self.outcomes,
            Impact: self.impacts
        }[type(component)]
        comp_list.append(component)
        self._id_map[component.id] = component

    def get_component_by_id(self, cid: int) -> LogicComponent:
        return self._id_map[cid]

    def simulate(self, changed_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate how changes in inputs affect downstream outcomes and impacts.
        For demonstration: simple propagation of changes, allowing for user-defined logic per component.
        """
        # Map component to "state" (could be any measurable attribute, e.g., value, level)
        state: Dict[int, Any] = {}

        # Initialize input values
        for inp in self.inputs:
            val = changed_inputs.get(inp.name, getattr(inp, 'value', 1))
            state[inp.id] = val

        # Propagate through the model (topological sort)
        for comp_type in [Activity, Output, Outcome, Impact]:
            comp_list = getattr(self, f"{comp_type.__name__.lower()}s")
            for comp in comp_list:
                # For each component, determine its state as a function of its dependencies
                # Simple rule: sum of upstream states, or default to 1
                upstream = [c for c in self._id_map.values() if comp in c.links]
                if upstream:
                    state[comp.id] = sum(state.get(u.id, 1) for u in upstream)
                else:
                    state[comp.id] = getattr(comp, 'value', 1)

        # Return only outcomes and impacts for clarity
        result = {}
        for comp in self.outcomes + self.impacts:
            result[comp.name] = state.get(comp.id, None)
        return result

    def validate(self) -> Dict[str, List[str]]:
        """
        Validate logical consistency:
        - Check for missing links (components not connected to others)
        - Check for circular dependencies (cycles)
        """
        G = nx.DiGraph()
        for comp in self._id_map.values():
            G.add_node(comp.id)
            for link in comp.links:
                G.add_edge(comp.id, link.id)

        # Find isolated components (no in/out edges)
        isolated = [
            comp.name for comp in self._id_map.values()
            if G.degree(comp.id) == 0
        ]
        # Find cycles
        try:
            cycles = list(nx.find_cycle(G, orientation='original'))
            cycle_names = [
                (self._id_map[u].name, self._id_map[v].name) for u, v, _ in cycles
            ]
        except nx.NetworkXNoCycle:
            cycle_names = []
        return {"isolated_components": isolated, "circular_dependencies": cycle_names}

    def visualize(self, figsize=(10, 7)):
        """
        Visualize the logic model as a directed graph using matplotlib.
        """
        G = nx.DiGraph()
        label_map = {}
        color_map = []
        node_types = {}
        for comp_list, color in [
            (self.inputs, 'skyblue'),
            (self.activities, 'orange'),
            (self.outputs, 'lightgreen'),
            (self.outcomes, 'plum'),
            (self.impacts, 'gold')
        ]:
            for comp in comp_list:
                G.add_node(comp.id)
                label_map[comp.id] = f"{comp.name}\n({comp.__class__.__name__})"
                color_map.append(color)
                node_types[comp.id] = comp.__class__.__name__
                for link in comp.links:
                    G.add_edge(comp.id, link.id)

        pos = nx.multipartite_layout(G, subset_key=lambda n: [
            'Input', 'Activity', 'Output', 'Outcome', 'Impact'
        ].index(node_types[n]))
        plt.figure(figsize=figsize)
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color=color_map)
        nx.draw_networkx_labels(G, pos, labels=label_map, font_size=10)
        nx.draw_networkx_edges(G, pos, arrows=True)
        plt.title(self.name)
        plt.axis('off')
        plt.show()

    def export_json(self, path: Optional[str] = None) -> str:
        """
        Export the logic model configuration to JSON.
        """
        data = {
            "name": self.name,
            "components": [comp.to_dict() for comp in self._id_map.values()]
        }
        json_str = json.dumps(data, indent=2)
        if path:
            with open(path, "w") as f:
                f.write(json_str)
        return json_str

    def summary(self) -> None:
        """Print a high-level summary of the logic model."""
        print(f"Logic Model: {self.name}")
        for comp_type in ['inputs', 'activities', 'outputs', 'outcomes', 'impacts']:
            comps = getattr(self, comp_type)
            print(f"  {comp_type.capitalize()}: {len(comps)}")
        print(f"  Total components: {len(self._id_map)}")

# Example usage (remove or comment this before importing as a module)
if __name__ == "__main__":
    # Build a sample logic model
    lm = LogicModel("Sample Program")

    inp_funds = Input("Funding", "Allocated budget")
    inp_staff = Input("Staff", "Personnel assigned")

    act_train = Activity("Training", "Conduct staff training")
    act_educate = Activity("Education", "Run community workshops")

    out_trained = Output("Staff Trained", "Number of staff trained")
    out_sessions = Output("Workshops Held", "Workshops delivered")

    outcome_awareness = Outcome("Increased Awareness", "Improved community awareness")
    impact_health = Impact("Improved Health", "Better health outcomes in community")

    # Add components
    for comp in [inp_funds, inp_staff, act_train, act_educate, out_trained,
                 out_sessions, outcome_awareness, impact_health]:
        lm.add_component(comp)

    # Link components to form the logic structure
    inp_funds.add_link(act_train)
    inp_staff.add_link(act_train)
    act_train.add_link(out_trained)
    out_trained.add_link(act_educate)
    act_educate.add_link(out_sessions)
    out_sessions.add_link(outcome_awareness)
    outcome_awareness.add_link(impact_health)

    # Visualize model
    lm.visualize()

    # Simulate scenario: increase staff and funding
    results = lm.simulate({'Funding': 2, 'Staff': 3})
    print("\nSimulation results (changed inputs):")
    for k, v in results.items():
        print(f"  {k}: {v}")

    # Validate structure
    print("\nValidation:")
    print(lm.validate())

    # Export to JSON
    print("\nJSON Export:")
    print(lm.export_json())
