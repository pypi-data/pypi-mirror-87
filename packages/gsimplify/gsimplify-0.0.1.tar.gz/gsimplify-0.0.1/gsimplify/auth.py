import json

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build

SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents.readonly",
]


def load_creds():
    """
    Loads creds from a pickle file. If creds do not exist, requests for user authorization. Modified from the Google Drive API Python quickstart guide.

    Returns:
        creds (tuple): the creds for the google drive API
    """
    credentials = service_account.Credentials.from_service_account_file(
        "creds.json", scopes=SCOPES
    )
    return credentials
