from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build
from pydantic import BaseModel

from gsimplify.typedefs import DocType, FolderType, DriveObj

"""
TODO: Fix potential race conditions with a one-time fetch of drive objects
"""

"""
TODO: Fix potential race conditions with a one-time fetch of drive objects
"""


class Drive:
    def __init__(self, drive_id: str, creds):
        self.drive_id = drive_id
        self.service: Resource = build("drive", "v3", credentials=creds)
        self.drive_info = self.service.teamdrives().get(teamDriveId=drive_id).execute()
        self.files = self.contains()

    def contains(self):
        drive_objs = (
            self.service.files()
            .list(
                corpora="teamDrive",
                supportsTeamDrives=True,
                teamDriveId=self.drive_id,
                includeTeamDriveItems=True,
                fields="*",  # TODO: restrict scope of fields to cut down on build times
            )
            .execute()
            .get("files")
        )

        container = []
        for each_obj in drive_objs:
            if each_obj.get("mimeType") == "application/vnd.google-apps.folder":
                container.append(
                    FolderType(
                        kind=each_obj.get("kind"),
                        id=each_obj.get("id"),
                        name=each_obj.get("name"),
                        mime_type=each_obj.get("mimeType"),
                        drive_id=each_obj.get("driveId"),
                        parents=each_obj.get("parents")[0],
                    )
                )
            else:
                if each_obj.get("name").startswith("PUBLIC:"):
                    public = True
                    draft = False
                elif each_obj.get("name").startswith("DRAFT:"):
                    public = False
                    draft = True
                else:
                    public = False
                    draft = False

                if each_obj.get("mimeType") == "application/vnd.google-apps.document":

                    container.append(
                        DocType(
                            kind=each_obj.get("kind"),
                            id=each_obj.get("id"),
                            name=each_obj.get("name"),
                            mime_type=each_obj.get("mimeType"),
                            drive_id=each_obj.get("driveId"),
                            draft=draft,
                            public=public,
                            pointer=" ".join(each_obj.get("name").split(": ")[1:]),
                            parents=each_obj.get("parents")[0],
                            webViewLink=each_obj.get("webViewLink"),
                        )
                    )

                else:
                    container.append(
                        DriveObj(
                            kind=each_obj.get("kind"),
                            id=each_obj.get("id"),
                            name=each_obj.get("name"),
                            mime_type=each_obj.get("mimeType"),
                            drive_id=each_obj.get("driveId"),
                            pointer=" ".join(each_obj.get("name").split(": ")[1:]),
                            parents=each_obj.get("parents")[0],
                            draft=draft,
                            public=public,
                            webViewLink=each_obj.get("webViewLink"),
                        )
                    )

        return container

    def docs(self, public: Optional[bool] = None, draft: Optional[bool] = None):
        selector = self._selector(public, draft)

        return [x for x in self.files if isinstance(x, DocType) and selector(x)]

    def media(self, public: Optional[bool] = None, draft: Optional[bool] = None):
        selector = self._selector(public, draft)
        return [
            x
            for x in self.files
            if not isinstance(x, FolderType)
            and not isinstance(x, DocType)
            and selector(x)
        ]

    def folders(self):
        return [x for x in self.files if isinstance(x, FolderType)]

    def _selector(self, public: Optional[bool] = None, draft: Optional[bool] = None):
        if public:
            public_selector = lambda x: x if x.public else False
        elif public == False:
            public_selector = lambda x: x if not x.public else False
        else:
            public_selector = lambda x: x

        if draft:
            selector = lambda x: public_selector(x) and public_selector(x).draft
        elif public == False:
            selector = lambda x: public_selector(x) and not public_selector(x).draft
        else:
            selector = lambda x: public_selector(x)

        return selector
