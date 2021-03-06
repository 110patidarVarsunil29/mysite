from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.sessions.models import Session


# Model to store the list of logged in users

class UserSession(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='logged_in_user', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.user.username


class TutorialCategory(models.Model):
    tutorial_category = models.CharField(max_length=200)
    category_summary = models.CharField(max_length=200)
    category_slug = models.CharField(max_length=200, default=1)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.tutorial_category


class TutorialSeries(models.Model):
    tutorial_series = models.CharField(max_length=200)
    tutorial_category = models.ForeignKey(TutorialCategory, default=1, verbose_name="Category",
                                          on_delete=models.SET_DEFAULT)
    series_summary = models.CharField(max_length=200)

    class Meta:
        # otherwise we get "Tutorial Series in admin"
        verbose_name_plural = "Series"

    def __str__(self):
        return self.tutorial_series


class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=200)
    tutorial_content = models.TextField()
    tutorial_published = models.DateTimeField('date published', default=datetime.now())
    tutorial_series = models.ForeignKey(TutorialSeries, default=1, verbose_name="Series", on_delete=models.SET_DEFAULT)
    tutorial_slug = models.CharField(max_length=200, default=1)

    def __str__(self):
        return self.tutorial_title


# Managing Files and upload files

class UserProfile(models.Model):
    fname = models.CharField(max_length=200)
    display_picture = models.FileField()

    def __str__(self):
        return self.fname
