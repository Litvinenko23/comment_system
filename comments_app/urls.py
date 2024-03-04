from django.urls import path

from comments_app import views


urlpatterns = [
    path("", views.room),
]

app_name = 'comments_app'
