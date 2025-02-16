import os
import requests
from fastapi import APIRouter, HTTPException
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")

AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
PROFILE_URL = "https://api.linkedin.com/v2/me"
EMAIL_URL = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"

@router.get("/auth/linkedin/login")
def linkedin_login():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "r_liteprofile r_emailaddress"
    }
    return {"login_url": f"{AUTH_URL}?{urlencode(params)}"}

@router.get("/auth/linkedin/callback")
def linkedin_callback(code: str):
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    token_response = requests.post(TOKEN_URL, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to retrieve access token")

    headers = {"Authorization": f"Bearer {access_token}"}
    profile_data = requests.get(PROFILE_URL, headers=headers).json()
    email_data = requests.get(EMAIL_URL, headers=headers).json()

    user_info = {
        "name": profile_data.get("localizedFirstName", "") + " " + profile_data.get("localizedLastName", ""),
        "linkedin_id": profile_data.get("id", ""),
        "email": email_data.get("elements", [{}])[0].get("handle~", {}).get("emailAddress", ""),
    }
    
    return user_info
