from django.urls import path

from . import views

urlpatterns = [
    path("", views.DownloadsListView.as_view(), name="list"),
]

