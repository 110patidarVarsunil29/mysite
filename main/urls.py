from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("contact/", views.contact, name="contact"),
    path("<single_slug>/", views.single_slug, name="single_slug"),
    path("<single_slug>/<double_slug>", views.double_slug, name="double_slug"),

]
