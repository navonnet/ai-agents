from dotenv import load_dotenv
import os
from fastapi import Body
import requests
from typing import Optional, Dict, Any
import base64

load_dotenv()

class waAPiClient:
    def __init__(self):
        self.apikey = os.getenv("WA_API_KEY")
        self.accountId = os.getenv("WA_ACCOUNT_ID")
        self.base_url = f"https://api.wildapricot.org/v2.1/accounts/{self.accountId}"
        
        if not self.apikey or not self.accountId:
            raise ValueError("WA_API_KEY and WA_ACCOUNT_ID must be set in environment variables")

    def getToken(self):
        print(self.apikey)
        raw = f"APIKEY:{self.apikey}"
        encodedKey = base64.b64encode(raw.encode("utf-8")).decode("utf-8")
        headers = {
            "Authorization": f"Basic {encodedKey}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        body = {
            "scope": "auto",
            "grant_type": "client_credentials"
        }
        
        url = "https://oauth.wildapricot.org/auth/token"
        
        try:
            response = requests.post(url, headers=headers, data=body)
            response.raise_for_status()
            return response.json().get("access_token")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching events: {e}")
            return {"error": str(e)}


    def listEvents(self, limit: Optional[int] = 100, after: Optional[str] = None) -> Dict[str, Any]:
        """
        Get events from WildApricot API
        
        Args:
            limit: Maximum number of events to return (default: 100)
            after: Cursor for pagination (optional)
            
        Returns:
            Dictionary containing events data
        """
        token = self.getToken()
        if token is None:
            raise Exception("Token could not be retrieved")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
            
        params = {}
        if limit:
            params["$top"] = limit
        if after:
            params["$skip"] = after
            
        url = f"{self.base_url}/events"
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching events: {e}")
            return {"error": str(e)}
    
    def findContactViaEmail(self, email:str) -> Dict[str, Any]:
        """
        Get a contact by email from WildApricot API
        
        Returns:
            Dictionary containing contact data
        """
        token = self.getToken()
        if token is None:
            raise Exception("Token could not be retrieved")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
             
        url = f"{self.base_url}/contacts?$async=false&$filter=Email eq {email}"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching contacts: {e}")
            return {"error": str(e)}

    def listContacts(self, limit: Optional[int] = 100, after: Optional[str] = None) -> Dict[str, Any]:
        """
        Get contacts from WildApricot API
        
        Args:
            limit: Maximum number of events to return (default: 100)
            after: Cursor for pagination (optional)
            
        Returns:
            Dictionary containing contact data
        """
        token = self.getToken()
        if token is None:
            raise Exception("Token could not be retrieved")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
            
        params = {}
        if limit:
            params["$top"] = limit
        if after:
            params["$skip"] = after
            
        url = f"{self.base_url}/contacts?$async=false"
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching contacts: {e}")
            return {"error": str(e)}

    # Function to create a contact using the API
    def create_contact(self, email: str, firstName: str, lastName: str) -> dict:
        try:

            """Create a contact in Wild Apricot.
            - first_name: given name only (e.g. 'Terry')
            - last_name: family name only (e.g. 'Halson')"""

            token = self.getToken()
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            payload = {
                "Email": email,
                "FirstName": firstName,
                "LastName": lastName
            }

            response = requests.post(f"{self.base_url}/Contacts", headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["Id"]
        except Exception as e:
            # Instead of raising, return a safe dict so the agent doesn’t retry forever
            return {"error": f"create_contact failed: {str(e)}"}


    # Function to create a contact using the API
    def register_for_event(self, contactId: int, eventName: str, regType: str) -> dict:
        """Create a contact in Wild Apricot."""
        token = self.getToken()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        evtResponse = requests.get(f"{self.base_url}/Events?$filter=Name eq '{eventName}'", headers=headers)
        evtResponse.raise_for_status()
        
        events = evtResponse.json().get("Events", [])
        if not events or len(events) > 1:
            return f"No or more events found with the name '{eventName}'."
        
        eventId = events[0]["Id"]

        print(f"Event ID for '{eventName}': {eventId}")
        
        evtTypeResponse = requests.get(f"{self.base_url}/EventRegistrationTypes?eventId={eventId}", headers=headers)
        evtTypeResponse.raise_for_status()
        if not evtTypeResponse.json():
            return f"Event '{eventName}' not found or has no registration types."
        
        eventTypes = evtTypeResponse.json()
        eventType = next((et for et in eventTypes if et["Name"].lower() == regType.lower()), None) 
        if not eventType:
            return f"Event type '{eventType}' not found for event '{eventName}'."
                                
        if not eventId or not eventType:
            return f"Event '{eventName}' or type '{eventType}' not found."
        
        if not contactId:
            return "Contact ID must be provided or found by email."

        print(f"Registering contact ID {contactId} for event ID {eventId} with type ID {eventType['Id']}")
        # Prepare the payload for registration
        payload = {
            "Event": {
                "Id": eventId
            },
            "RegistrationTypeId": eventType["Id"],
            "Contact": {
                "Id": contactId
            }
        }
        response = requests.post(f"{self.base_url}/EventRegistrations", headers=headers, json=payload)
        
        #print(f"Event Registration Response: {response.json()}")
        response.raise_for_status()
        #print reponse.json()
        
        return response.json()["Id"]

    # Write a method to get all eventRegistrations for an event
    def get_event_registrations(self, eventName: str, limit: Optional[int] = 100, after: Optional[str] = None) -> dict:
        """Get all event registrations for a specific event.""" 
        token = self.getToken()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        evtResponse = requests.get(f"{self.base_url}/Events?$filter=Name eq '{eventName}'", headers=headers)
        evtResponse.raise_for_status()
        
        events = evtResponse.json().get("Events", [])
        if not events or len(events) > 1:
            return f"No or more events found with the name '{eventName}'."
        
        eventId = events[0]["Id"]

        params = {}
        if limit:
            params["$top"] = limit
        if after:
            params["$skip"] = after

        regs = requests.get(f"{self.base_url}/EventRegistrations?eventId={eventId}", headers=headers, params=params)
        regs.raise_for_status()
        if not regs.json():
            return f"Event '{event}' not found or has no registrations."

        return regs.json()

if __name__ == "__main__":
    try:
        client = waAPiClient()
        events = client.create_contact("testuser1_12@wa.com","TestUser12_1","User_12")
        print("Events:", events)
    except Exception as e:
        print(f"Error: {e}")
