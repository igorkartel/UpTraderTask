from django.contrib import admin
from django.urls import path

from tree_coded_menu.views import index, index2, index3

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("2/", index2, name="index2"),
    path("3/", index3, name="index3"),
]
