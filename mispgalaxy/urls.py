from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("actors/", views.threat_actor_browser, name="threat_actor_browser"),
    path("actors/<int:actor_id>/", views.get_actor_details, name="get_actor_details"),


    path("search_actor_ajax/", views.search_actor_ajax, name="search_actor_ajax"),


]