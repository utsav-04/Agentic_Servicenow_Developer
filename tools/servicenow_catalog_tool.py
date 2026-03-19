import requests
from crewai.tools import tool
from utils.config import INSTANCE, USERNAME, PASSWORD


@tool("create_catalog_item")
def create_catalog_item(name: str, short_description: str, description: str):
    """
    Create a catalog item in ServiceNow.
    """

    url = f"{INSTANCE}/api/now/table/sc_cat_item"

    payload = {
        "name": name,
        "short_description": short_description,
        "description": description
    }

    response = requests.post(
        url,
        auth=(USERNAME, PASSWORD),
        headers={"Content-Type": "application/json"},
        json=payload
    )

    return response.json()


@tool
def create_variable(cat_item: str, name: str, question_text: str, var_type: str):
    """
    Create a variable for a ServiceNow catalog item.
    """

    url = f"{INSTANCE}/api/now/table/item_option_new"

    payload = {
        "cat_item": cat_item,
        "name": name,
        "question_text": question_text,
        "type": var_type
    }

    response = requests.post(
        url,
        auth=(USERNAME, PASSWORD),
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 201:
        return "Variable created successfully"
    else:
        return f"Failed: {response.text}"
    

@tool
def create_client_script(name: str, cat_item: str, script: str, script_type: str):
    """
    Create a ServiceNow catalog client script.
    """

    url = f"{INSTANCE}/api/now/table/catalog_script_client"

    payload = {
        "name": name,
        "cat_item": cat_item,
        "type": script_type,
        "applies_to": "item",
        "script": script
    }

    response = requests.post(
        url,
        auth=(USERNAME, PASSWORD),
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 201:
        return "Client Script created successfully"
    else:
        return f"Failed to create script: {response.text}"

@tool
def create_update_set(name: str):
    """
    Create an update set in ServiceNow.
    """

    url = f"{INSTANCE}/api/now/table/sys_update_set"

    payload = {
        "name": name
    }

    response = requests.post(
        url,
        auth=(USERNAME, PASSWORD),
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 201:
        return "Update Set created successfully"
    else:
        return f"Failed to create update set: {response.text}"
    

@tool
def ask_user_input(question: str) -> str:
    """Ask the user a question and return their response."""
    return input(f"\nAgent: {question}\nYou: ")


@tool("get_incident")
def get_incident(incident_number: str):
    """
    Retrieve an incident record from ServiceNow by its number.
    """
    url = f"{INSTANCE}/api/now/table/incident"
    params = {"number": incident_number}

    response = requests.get(
        url,
        auth=(USERNAME, PASSWORD),
        headers={"Content-Type": "application/json"},
        params=params
    )

    if response.status_code == 200:
        data = response.json()
        if "result" in data and len(data["result"]) > 0:
            return data["result"][0]  # return the incident record
        else:
            return f"No incident found with number {incident_number}"
    else:
        return f"Failed to fetch incident: {response.text}"
    

@tool("get_summary")
def get_summary(change_number: str):
    """
    Retrieve a change request record from ServiceNow by its number and summarize it.
    """
    url = f"{INSTANCE}/api/now/table/change_request"
    params = {"number": change_number}

    response = requests.get(
        url,
        auth=(USERNAME, PASSWORD),
        headers={"Content-Type": "application/json"},
        params=params
    )

    if response.status_code == 200:
        data = response.json()
        if "result" in data and len(data["result"]) > 0:
            return data["result"][0]  # return the change request record
        else:
            return f"No change request found with number {change_number}"
    else:
        return f"Failed to fetch change request: {response.text}"