from langchain.tools import StructuredTool
from inputModels import CreateContactInput, RegisterForEventInput
from langchain_core.tools import Tool
from wa_api import waAPiClient

class wa_tools:

    def __init__(self) -> None:
        client = waAPiClient() 
        self.tools=[
            Tool(
                name="list_contacts",
                func=client.listContacts,
                description="Call this tool to fetch list available contacts in wildapricot."
            ),
            Tool(
                name="findContactViaEmail",
                func=client.findContactViaEmail,
                description="Call this tool to find a contact by email. To check of a contact exist with an email."
            ),
            Tool(
                name="list_events",
                func=client.listEvents,
                description="Call this tool to fetch list available events in wildapricot. Only fetch active events."
            ),
            StructuredTool(
                name="create_contact",
                func=client.create_contact,
                description="""
                Call this tool to add a new contact.

                Required args:
                - email: the person's email
                - first_name: ONLY the given name (e.g. 'John' from 'John Wick')
                - last_name: ONLY the family name (e.g. 'Wick' from 'John Wick')

                If the user provides a full name (e.g. 'Terry Halson'), you MUST split it
                into first_name='Terry' and last_name='Halson' before calling this tool.
                Do not pass the full name as first_name.
                Before creating contact, do display a final consolidated information and ask the user to confirm.
                """,
            args_schema=CreateContactInput),
            Tool(
                    name="get_event_registrations",
                    func=client.get_event_registrations,
                    description="""Call this tool to get current registrations for an event, 
                                    fetch event detail from list_events, ask user the name of the event.
                                    """
            ),
            StructuredTool(
                    name="register_for_event",
                    func=client.register_for_event,
                    description="""Call this tool to register a contact for an event. User must provide details about the active event 
                                    and if contact is missing add a new contact first and then create a new registration.
                                    If email provided then search contact by tool 'findContactViaEmail' and the extract the id as contactId
                                    If no contact found using the email, create a new contact by using tool create_contact
                                    If creating contact do ask email, firstName and last of a contact.
                                    if regType is not provided then you must ask the user for that, don't pass the default value,
                                    Registration type are custom values to be fetch from evant details, These can't any random values. It has to match with exat setup types.
                                    Don't show registeration types as example, display as list and ask user to choose one the value.
                                    Do not proceed with register_for_event until create_contact susceeded and you have contact Id.
                                    If contactId is zero then findContactViaEmail
                                    Before creating record, do display a final consolidated information and ask the user to confirm.""",
                    args_schema=RegisterForEventInput
            )]

    def getAll(self) -> list:
        return self.tools
