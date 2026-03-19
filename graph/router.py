from langchain_google_genai import ChatGoogleGenerativeAI
import os

#os.environ["GOOGLE_API_KEY"] = "AIzaSyDCRnC8Od93KmRU8DAt3Ihf1aCxmQPKMEM"
os.environ["GOOGLE_API_KEY"] = "AIzaSyCVa3sNUxI-KiRh8EZG4a6HaOhDiIl9csc"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
)


def detect_intent(user_input):

    prompt = f"""
You are an intent classification assistant.

Classify the user request into ONE of the following intents:

catalog_creation  -> user wants to create a ServiceNow catalog item
add_variable      -> user wants to create/add a variable to a catalog item
create_client_script -> user wants to create a ServiceNow catalog client script
create_update_set   -> user wants to create an update set in ServiceNow
incident_summary  -> summarize incidents
change_summary       -> summarize Change requests
general_chat      -> normal conversation

User message:
{user_input}

Return ONLY the intent name.
Example outputs:
catalog_creation
add_variable
create_client_script
create_update_set
incident_summary
change_summary
general_chat
"""

    response = llm.invoke(prompt)

    intent = response.content.strip().lower()

    return intent