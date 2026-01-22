from threading import Lock
from django.conf import settings
import os
from datetime import datetime


class Config:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Config, cls).__new__(cls)
                cls._instance.settings = {
                    "command_file": os.path.join(
                        settings.MEDIA_ROOT,
                        "GPL_AUDIT",
                        "command_file",
                        "GPL_Audit_command_updated.txt",
                    ),
                    "pre_log_folder": os.path.join(
                        settings.MEDIA_ROOT, "GPL_AUDIT", "pre_input_files/"
                    ),
                    "post_log_folder": os.path.join(
                        settings.MEDIA_ROOT, "GPL_AUDIT", "post_input_files/"
                    ),
                    "pre_output_excel": os.path.join(
                        settings.MEDIA_ROOT,
                        "GPL_AUDIT",
                        "gpl_pre_audit",
                        f"PRE_GPL_AUDIT.xlsx",
                    ),
                    "gpl_pre_post_audit": os.path.join(
                        settings.MEDIA_ROOT,
                        "GPL_AUDIT",
                        "gpl_pre_post_audit",
                        f"GPL_POST_AUDIT.xlsx",
                    ),
                    "GPL_correction_script": os.path.join(
                        settings.MEDIA_ROOT,
                        "GPL_AUDIT",
                        "script_generated",
                        "GPL_Correction_Script.txt",
                    ),
                    "GPL_Relation_script": os.path.join(
                        settings.MEDIA_ROOT,
                        "GPL_AUDIT",
                        "script_generated",
                        "Relation_Correction_Script.txt",
                    ),
                    "GPL_AUDIT_OUTPUT": os.path.join(
                        settings.MEDIA_ROOT,
                        "GPL_AUDIT",
                        "GPL_AUDIT_OUTPUT",
                    ),
                    "max_threads": 8,
                }
            return cls._instance

    def get(self, key, url=False):
        """
        Fetches a configuration value.
        If `url=True`, returns the corresponding MEDIA_URL path.
        """
        value = self.settings.get(key)
        if url and value and value.startswith(settings.MEDIA_ROOT):
            return value.replace(settings.MEDIA_ROOT, settings.MEDIA_URL).replace(
                "\\", "/"
            )
        return value
