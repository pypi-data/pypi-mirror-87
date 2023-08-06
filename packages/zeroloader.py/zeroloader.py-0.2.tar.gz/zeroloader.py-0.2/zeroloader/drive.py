from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

scopes = ["https://www.googleapis.com/auth/drive"]


def get_cred(service_file):
    return service_account.Credentials.from_service_account_file(
        service_file, scopes=scopes
    )


class GoogleDrive:
    def __init__(self, service_file):
        self.service = build("drive", "v3", credentials=get_cred(service_file))

    def create_folder(self, folder_name, parent_id):
        metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id],
        }
        f = self.service.files().create(body=metadata, fields="id").execute()
        return f.get("id")

    def download(self, id, output_dir, output_filename=None):
        if not output_filename:
            output_filename = id
        destination = f"{output_dir}/{output_filename}"
        request = self.service.files().get_media(fileId=id)
        file = open(destination, "wb")
        media_request = MediaIoBaseDownload(file, request)
        done = False
        while not done:
            status, done = media_request.next_chunk()
        return destination

    def upload(self, src, filename, parent, file_id=None):
        # upload
        file_metadata = {"name": filename}
        if file_id:
            f = (
                self.service.files()
                .update(
                    fileId=file_id,
                    body=file_metadata,
                    media_body=MediaFileUpload(
                        src, mimetype="application/octet-stream", resumable=True
                    ),
                    fields="id",
                )
                .execute()
            )
        else:
            file_metadata["parents"] = [parent]
            f = (
                self.service.files()
                .create(
                    body=file_metadata,
                    media_body=MediaFileUpload(
                        src, mimetype="application/octet-stream", resumable=True
                    ),
                    fields="id",
                )
                .execute()
            )

        return f.get("id")

    def list_files(self, parent_id):
        result = (
            self.service.files()
            .list(
                q=f"'{parent_id}' in parents", spaces="drive", fields="files(id, name)"
            )
            .execute()
        )
        return result["files"]
