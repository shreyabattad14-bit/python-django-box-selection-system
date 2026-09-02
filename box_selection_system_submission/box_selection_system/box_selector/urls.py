from django.urls import path
from .views import recommend_box_api

urlpatterns = [
    path("recommend-box/", recommend_box_api, name="recommend-box"),
]
