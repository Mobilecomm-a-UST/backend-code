from django.http import HttpResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def home_page(request):
    html_content = """
        <html>
            <head>
                <title>McomBackend</title>
            </head>
            <body style="font-family: Arial; background-color: #f5f5f5; text-align: center; margin-top: 20%;">
                <h1 style="color: #2c3e50;">McomBackend Tool</h1>
                <p style="font-size: 18px; color: #555;">
                    McomBackend Tool backend server is running successfully...
                </p>
            </body>
        </html>
    """
    return HttpResponse(html_content, content_type="text/html")
