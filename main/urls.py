from django.urls import path
from . import views
from django.conf.urls.static import static
from mysite import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns


app_name = "main"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path('upload/', views.create_profile, name="upload"),
    path("contact/", views.contact, name="contact"),
    path("<single_slug>/", views.single_slug, name="single_slug"),
    path("<single_slug>/<double_slug>", views.double_slug, name="double_slug"),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
