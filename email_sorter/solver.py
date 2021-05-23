from __future__ import print_function
import os.path
import email
import base64
import datetime
import pandas as pd
from dateutil.parser import parse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
MAX_RESULT = 511
NEXTPAGETOKEN = "nextPageToken"
MESSAGES = "messages"
SPACES = "        "


class Service:
    def __init__(self, credential_filepath):
        self.__cred_filepath = credential_filepath

    def get_service(self):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.__cred_filepath, SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return build("gmail", "v1", credentials=creds)


class GetMessages(Service):
    def __init__(self, credential_filepath, user_id):
        super().__init__(credential_filepath)
        self.__user_id = user_id
        self.__service = super().get_service()
        self.base_function = self.__service.users().messages()

    def get_all_message_ids(self):
        # TODO: cleanup function too big breakdown more
        try:
            search_id = self.base_function.list(
                userId=self.__user_id, maxResults=MAX_RESULT
            ).execute()
            pageToken = None
            if NEXTPAGETOKEN in search_id:
                pageToken = search_id[NEXTPAGETOKEN]

            message_list = search_id[MESSAGES]
            while pageToken:
                results = self.base_function.list(
                    userId=self.__user_id, maxResults=MAX_RESULT, pageToken=pageToken
                ).execute()
                message_list.append(results[MESSAGES])
                if NEXTPAGETOKEN in results:
                    pageToken = results[NEXTPAGETOKEN]
                else:
                    break
            print("No more messages")
        except Exception:
            print("An error occured: %s") % error
        return [Messages(raw_dict) for raw_dict in message_list]

    def get_message_info(self, msg_id):
        mime_msg = self.decode_message(msg_id)
        # get message within email
        message = get_message_text(mime_msg)
        label_ids = mime_msg["labelIds"]
        read_status = "UNREAD" if "UNREAD" in label_ids else "READ"
        sender = mime_msg["From"]
        subject = mime_msg["subject"]
        received = self.date_string_format(mime_msg["Received"])
        return {
            "message_id": msg_id,
            "sender": sender,
            "subject": subject,
            "received": received,
            "message": message,
            "read_status": read_status,
        }

    def get_message_text(self, mime_msg):
        content = mime_msg.get_content_maintype()
        if content == "multipart":
            text_format, _ = mime_msg.get_payload()
            message_draft = text_format.get_payload()
        elif content == "text":
            message_draft = mime_msg.get_payload()
        # if message is too large return too large
        return message_draft if len(message_draft) >= 500 else "MESSAGE TOO LARGE"

    def decode_message(self, msg_id):
        try:
            message = self.base_function.get(
                userId=self.__user_id, id=msg_id, format="raw"
            ).execute()
            text = base64.urlsafe_b64decode(message["raw"].encode("ASCII"))
            return email.message_from_bytes(text)
        except Exception:
            print("An error occured: %s") % error

    def date_string_format(self, raw_date_string: str):
        if SPACES in raw_date_string:
            return parse(raw_date_string.split(SPACES)[1])

    def main():
        message_id_list = self.get_all_message_ids()
        message_format_list = [
            self.get_message_info(message.id) for message in message_id_list
        ]
        return pd.DataFrame(message_format_list)


class Messages:
    def __init__(self, raw_id_dict: dict):
        self.msg_id = raw_id_dict.get("id")
        self.thread_id = raw_id_dict.get("threadId")

    @property
    def id(self):
        return self.msg_id

    @property
    def id(self):
        return self.thread_id
