from rest_framework import serializers


class ExcelUploadSerializer(serializers.Serializer):
    pre_audit_file = serializers.FileField(required=False)
    PRE_POST_AUDIT_FILE = serializers.FileField(required=False)
    post_log_files = serializers.ListField(
        child=serializers.FileField(), required=False
    )
    pre_log_files = serializers.ListField(child=serializers.FileField(), required=False)

    def validate(self, data):
        # Get the service type from the request
        request = self.context.get("request")
        services = request.POST.get("services") if request else None

        if services == "GPL PRE POST AUDIT":
            if not data.get("pre_audit_file"):
                raise serializers.ValidationError(
                    "Pre-audit file is required for GPL PRE POST AUDIT"
                )
            if not data.get("post_log_files"):
                raise serializers.ValidationError(
                    "Post log files are required for GPL PRE POST AUDIT"
                )
        elif services == "GPL PRE AUDIT":
            if not data.get("pre_log_files"):
                raise serializers.ValidationError(
                    "Pre log files are required for GPL PRE AUDIT"
                )
        elif services == "SCRIPT GENERATOR":
            if not data.get("PRE_POST_AUDIT_FILE"):
                raise serializers.ValidationError(
                    "PRE_POST_AUDIT_FILE is required for SCRIPT GENERATOR"
                )

        return data
