from django.urls import path
from . import util
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<title>/",util.get_entry, name="wiki"),
    path("wiki/<title>/edit/",views.edit,name="edit"),
    path("edited/<title>/",views.edited,name="edited"),
    path("create/",views.create,name="create"),
    path("random/",views.randome,name="random"),
    path("search/",views.search,name="search")
]
