from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.PageByKeyView.as_view(key="ABOUT"), name="about"),
    path("services/", views.ServicesListView.as_view(), name="services"),
    path("departments/", views.DepartmentsListView.as_view(), name="departments"),
    path("news-events/", views.NewsEventsListView.as_view(), name="news_events"),
    path("news-events/<slug:slug>/", views.NewsEventDetailView.as_view(), name="news_event_detail"),
    path("careers/", views.CareersListView.as_view(), name="careers"),
    path("careers/<slug:slug>/", views.CareerDetailView.as_view(), name="career_detail"),
    path("contact/", views.PageByKeyView.as_view(key="CONTACT"), name="contact"),
]

