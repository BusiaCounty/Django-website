from django.urls import path

from . import views

urlpatterns = [
    path("", views.NoticeListView.as_view(), name="list"),
    path("<slug:slug>/", views.NoticeDetailView.as_view(), name="detail"),
]

