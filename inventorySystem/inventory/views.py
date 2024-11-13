from django.shortcuts import render

# Create your views here.
def index(request):
    context ={
        "title" : "Index Page"
    }
    return render(request, "inventory/index.html", context=context)