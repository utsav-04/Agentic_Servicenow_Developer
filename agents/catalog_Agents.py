from crewai import Agent
from tools.servicenow_catalog_tool import ask_user_input, create_catalog_item, create_client_script, create_update_set, create_variable, get_incident,get_summary
from utils.llm import llm


catalog_agent = Agent(
    role="ServiceNow Catalog Assistant",

    goal="Help users create catalog items in ServiceNow",

    backstory="""
    You assist users in creating catalog items.
    Ask the user for:
    1. name
    2. short description
    3. description
    Once collected, create the catalog item.
    """,

    tools=[create_catalog_item],
    llm=llm,

    verbose=True
)


variable_agent = Agent(
    role="ServiceNow Variable Creator",
    goal="Create catalog variables in ServiceNow",
    backstory="Expert ServiceNow developer specialized in catalog variables.",
    tools=[create_variable],
    llm=llm,
    verbose=True
)


client_script_agent = Agent(
    role="ServiceNow Client Script Developer",
    goal="Write catalog client scripts and create them in ServiceNow",
    backstory="""
    Expert ServiceNow developer who writes client scripts
    based on user requirements.
    """,
    tools=[create_client_script],
    llm=llm,
    verbose=True
)

update_agent = Agent(
    role="Servicenow Update set Creator",
    goal="Create update sets in ServiceNow",
    backstory="""
    Expert ServiceNow developer who creates update sets
    """,
    tools=[create_update_set, ask_user_input],
    llm=llm,
    verbose=True
)

incident_agent = Agent(
    role="ServiceNow Incident Summarizer",
    goal="Summarize ServiceNow incidents based on key fields",
    backstory="Expert ServiceNow analyst who summarizes incidents clearly.",
    tools=[get_incident],
    llm=llm,
    verbose=True
)

change_management_agent = Agent(
    role="ServiceNow Change Management Summarizer",
    goal="Summarize ServiceNow change requests based on key fields",
    backstory="Expert ServiceNow analyst who summarizes change requests clearly.",
    tools=[get_summary],
    llm=llm,
    verbose=True
)