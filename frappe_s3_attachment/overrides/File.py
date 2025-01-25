import frappe
from frappe.core.doctype.file.file import File
from frappe.utils import get_url

class FileOverride(File):
    def validate_file_url(self):
        if self.is_remote_file or not self.file_url:
            return

        if not self.file_url.startswith(("/files/", "/private/files/", "/api/method/frappe_s3_attachment.controller.generate_file")):
            # Probably an invalid URL since it doesn't start with http either
            frappe.throw(
                _("URL must start with http:// or https://"),
                title=_("Invalid URL"),
            )
    def get_full_path(self):

        site_url = get_url()

        if file_path.startswith("/api/method/frappe_s3_attachment.controller.generate_file"):
            return site_url + file_path

        return super().get_full_path()