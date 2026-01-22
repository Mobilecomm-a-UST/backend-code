from mailapp.tasks import send_email
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def send_email_view(request):
    to_address = request.POST.get("Email")
    subject = request.POST.get("Subject")
    body = request.POST.get("Body")

    # Call the Celery task asynchronously
    send_email(to_address, subject, body)

    return Response(
        {
            "Status": "True",
            "message": "Email request received. It will be sent shortly.",
        }
    )
