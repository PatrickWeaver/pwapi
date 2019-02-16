from django.http import HttpResponse

header = "<h1>PW API</h1>"

def index(request):
    return HttpResponse(header + "<a href='/v1/'>v1</a>")

def v1(request):
    return HttpResponse(
    header +
    "<h2>Version 1:</h2>" +
    "<a href='blog/posts/'>Blog Posts</a><br>" +
    "<a href='portfolio/'>Portfolio</a><br>" +
    "<a href='blobs/'>Blobs</a><br>"
    )
