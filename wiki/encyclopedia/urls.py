from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_display, name="entry_display"),
    path("search/", views.search, name="searching"),
    path("new_page/", views.new_page, name="new_page"),
    path("edit/", views.edit_page, name="edit_page"),
    path("save_edit/", views.save_edit, name="save_edit"),
    path('random/', views.random_page, name='random_page')
]

