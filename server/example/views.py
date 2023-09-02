
from django.http import HttpResponse

def index():
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
        </body>
    </html>
    '''
    return HttpResponse(html)