from typing import TypedDict
from crewai import Crew, Task
from langgraph.graph import StateGraph, END
from graph.router import detect_intent
from agents.catalog_Agents import catalog_agent
from agents.catalog_Agents import variable_agent
from agents.catalog_Agents import client_script_agent,update_agent, incident_agent , change_management_agent

class AgentState(TypedDict, total=False):
    input: str
    intent: str
    output: str
    active_flow: str


# ---------------- ROUTER NODE ----------------
def router_node(state: AgentState):

    user_input = state.get("input")

    # If a workflow is already active, continue it
    if state.get("active_flow"):
        return {"intent": state["active_flow"]}

    intent = detect_intent(user_input)
    print(f"DEBUG: Intent detected = '{intent}'")

    return {
        "intent": intent,
        "active_flow": intent
    }


# ---------------- CATALOG NODE ----------------
def catalog_node(state):

    user_input = state.get("input")

    task = Task(
        description=f"""
        Create a ServiceNow catalog item based on this request:

        {user_input}
        """,
        agent=catalog_agent,
        expected_output="A confirmation that the catalog item was created successfully."
    )

    crew = Crew(
        agents=[catalog_agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()

    return {
    "output": result,
    "active_flow": None
    }


# ---------------- VARIABLE NODE ----------------
def variable_node(state):

    user_input = state.get("input")

    task = Task(
        description=f"""
        Create a variable for a ServiceNow catalog item.

        Collect:
        - catalog item sys_id
        - variable name
        - variable type
        - question text

        User request:
        {user_input}
        """,
        agent=variable_agent,
        expected_output="Variable created successfully."
    )

    crew = Crew(
        agents=[variable_agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()

    return {
    "output": result,
    "active_flow": None
    }


# ---------------- CLIENT SCRIPT NODE ----------------

def client_script_node(state):

    user_input = state.get("input")

    task = Task(
        description=f"""
        User wants to create a ServiceNow catalog client script.

        Steps:
        1 Ask catalog item sys_id
        2 Ask script name
        3 Ask requirement
        4 Generate ServiceNow client script code
        5 Call create_client_script tool

        Requirement from user:
        {user_input}
        """,
        agent=client_script_agent,
        expected_output="Client script created successfully."
    )

    crew = Crew(
        agents=[client_script_agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()

    return {
    "output": result,
    "active_flow": None
    }


#----------------- UPDATE SET NODE ----------------

def update_set_node(state: AgentState):
    user_input = state.get("input")
    
    task = Task(
        description=f"""
        User wants to create an update set in ServiceNow.
        
        Steps:
        1. Ask for update set name
        2. Create update set using create_update_set tool
        
        User request: {user_input}
        """,
        agent=update_agent,
        expected_output="Update set created successfully."
    )
    
    crew = Crew(
        agents=[update_agent],
        tasks=[task],
        verbose=True
    )
    
    result = crew.kickoff()
    
    return {
        "output": result,
        "active_flow": None  # <- Only set to None when truly done
    }


# ----------------- INCIDENT SUMMARY NODE ----------------

def incident_summary_node(state: AgentState):
    user_input = state.get("input")
    
    task = Task(
        description=f"""
        Summarize the ServiceNow incident with number: {user_input} .
        
        Retrieve fields such as:
        - number
        - short_description
        - description
        - impact
        - urgency
        - category
        - priority
        - state

        Then write a **cohesive paragraph summary** in natural language,
        not a bullet list. The summary should explain the incident context,
        its impact, urgency, and resolution status in a readable way.
        """,
        agent=incident_agent,
        expected_output="A clear paragraph-style summary of the incident."
    )
    
    crew = Crew(
        agents=[incident_agent],
        tasks=[task],
        verbose=True
    )
    
    result = crew.kickoff()
    
    return {
        "output": result,
        "active_flow": None
    }


#----------------- CHANGE MANAGEMENT NODE ----------------

def change_management_node(state: AgentState):
    user_input = state.get("input")
    
    task = Task(
        description=f"""
        Summarize the ServiceNow change request with number:{user_input} .
        
        Retrieve fields such as:
        - number
        - short_description
        - description
        - justification
        - implementation_plan
        - backout_plan
        - test_plan
        - risk
        - impact
        - category
        - priority
        - state

        Then write a **cohesive paragraph summary** in natural language,
        not a bullet list. The summary should explain the change request context,
        its risk level, and approval status in a readable way.
        """,
        agent=change_management_agent,
        expected_output="A clear paragraph-style summary of the change request."
    )
    
    crew = Crew(
        agents=[change_management_agent],
        tasks=[task],
        verbose=True
    )
    
    result = crew.kickoff()
    
    return {
        "output": result,
        "active_flow": None
    }



# ---------------- ROUTING LOGIC ----------------
def route_intent(state: AgentState):

    intent = state.get("intent")

    if intent == "catalog_creation":
        return "catalog"

    elif intent == "add_variable":
        return "variable"

    elif intent == "create_client_script":
        return "client_script"

    elif intent == "create_update_set":
        return "update_set"
    
    elif intent == "incident_summary":
        return "incident"
    
    elif intent == "change_summary":
        return "change_management"

    return None

# ---------------- BUILD GRAPH ----------------
def build_graph():

    builder = StateGraph(AgentState)

    # Add nodes
    builder.add_node("router", router_node)
    builder.add_node("catalog", catalog_node)
    builder.add_node("variable", variable_node)
    builder.add_node("client_script", client_script_node)
    builder.add_node("update_set", update_set_node)
    builder.add_node("incident", incident_summary_node)
    builder.add_node("change_management", change_management_node)

    # Entry point
    builder.set_entry_point("router")

    # Conditional routing
    builder.add_conditional_edges(
        "router",
        route_intent,
        {
            "catalog": "catalog",
            "variable": "variable",
            "client_script": "client_script",
            "update_set": "update_set",
            "incident": "incident",
            "change_management": "change_management"
        }
    )

    # End edges
    builder.add_edge("catalog", END)
    builder.add_edge("variable", END)
    builder.add_edge("client_script", END)
    builder.add_edge("update_set", END)
    builder.add_edge("incident", END)
    builder.add_edge("change_management", END)

    return builder.compile()