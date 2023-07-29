from django.urls import path

from theatre.views import index

urlpatterns = [
    path("", index, name="index")
]
app_name = "theatre"
