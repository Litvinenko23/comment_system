from django.shortcuts import render


def index(request):
    return render(request, "comments_app/index.html")


def room(request):
    return render(request, "comments_app/room.html")
