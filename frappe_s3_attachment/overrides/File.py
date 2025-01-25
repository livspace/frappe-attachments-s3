import frappe
from frappe.core.doctype.file.file import File
from frappe.utils import get_url
from urllib.parse import urlparse, parse_qsl

from frappe_s3_attachment.controller import S3Operations


class FileOverride(File):
    def is_s3file(self):
        file_path = self.file_url or self.file_name
        return not self.is_folder and file_path.startswith("/api/method/frappe_s3_attachment.controller.generate_file")

    def validate_file_url(self):
        if self.is_s3file:
            return
        super().validate_file_url()

    def get_full_path(self):
        file_path = self.file_url or self.file_name
        if self.is_s3file:
            site_url = get_url()
            return site_url + file_path

        return super().get_full_path()

    def get_content(self, encodings=None) -> bytes | str:

        file_path = self.file_url or self.file_name
        if self.is_s3file():
            s3ops = S3Operations()
            parsed_url = urlparse(file_path)
            s3key = dict(parse_qsl(parsed_url.query))["key"]
            self._content = s3ops.read_file_from_s3(s3key)
            return self._content

        return super().get_content(encodings)