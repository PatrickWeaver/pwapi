from django.http import HttpResponse

def index(request):
    print("HELLO WORLD VIEW")
    return HttpResponse("Hello, world 3")
