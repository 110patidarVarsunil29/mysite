from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from main.models import Tutorial, TutorialCategory, TutorialSeries, UserSession
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, forms, ContactForm
# import logging
from django.contrib.sessions.models import Session
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError


def contact(request):
    if request.method == "POST":
        subject = 'Mail from Vjsh.'
        full_name = request.POST.get('full_name', '')
        email_address = request.POST.get('email_address', '')
        message = request.POST.get('message', '')
        email_content = "Full Name:=" + full_name + "\n" + "Email Address:= " + email_address + "\n" + message
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['patidarsunil110@gmail.com']
        if subject and message:
            try:
                send_mail(subject, email_content, email_from, recipient_list)
            except BadHeaderError:
                return render(request=request,
                              template_name="main/contact.html",
                              context={"email_error": "Invalid header found."})
            return render(request=request,
                          template_name="main/contact.html",
                          context={"email_info": "Thank you for contacting to us, we will contact soon!."})

        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return render(request=request,
                          template_name="main/contact.html",
                          context={"email_filed": "Make sure all fields are entered and valid."})
    else:
        form = ContactForm()
        return render(request,
                      "main/contact.html",
                      {"form": form})


def single_slug(request, single_slug):
    # first check to see if the url is in categories.

    categories = [c.category_slug for c in TutorialCategory.objects.all()]
    if single_slug in categories:
        matching_series = TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)
        series_urls = {}

        for m in matching_series.all():
            part_one = Tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest(
                "tutorial_published")
            series_urls[m] = part_one.tutorial_slug

        return render(request=request,
                      template_name='main/category.html',
                      context={  # "tutorial_series": matching_series,
                          "part_ones": series_urls})


def double_slug(request, single_slug, double_slug):
    tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]
    if double_slug in tutorials:
        this_tutorial = Tutorial.objects.get(tutorial_slug=double_slug)
        tutorials_form_series = Tutorial.objects.filter(
            tutorial_series__tutorial_series=this_tutorial.tutorial_series). \
            order_by("tutorial_published")

        this_tutorial_idx = list(tutorials_form_series).index(this_tutorial)

        return render(request=request,
                      template_name="main/tutorial.html",
                      context={"tutorial": this_tutorial,
                               "sidebar": tutorials_form_series,
                               "this_tutorial_idx": this_tutorial_idx})

    return HttpResponse(f"{double_slug} does not correspond to anything!")


def homepage(request):
    return render(request=request,
                  template_name="main/categories.html",
                  context={"categories": TutorialCategory.objects.all()}
                  )


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            # login(request, user)
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request=request,
                          template_name="main/register.html",
                          context={"form": form})

    form = NewUserForm
    return render(request=request,
                  template_name="main/register.html",
                  context={"form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # enable user session (db based session)
                if user.is_active:
                    user_id = request.session['member_id'] = user.id
                    request.session.set_expiry(request.session.get_expiry_age())
                    # date 11/04/2020 new concept
                    current_users = [us.user_id for us in UserSession.objects.all()]
                    session_details = [Session.objects.filter(expire_date__lte=datetime.now())]
                    print("check user_id ", user_id)
                    print("current_users check ", list(current_users))
                    if user_id in current_users and session_details is not None:
                        messages.error(request, "user is already active, Please try after some time!")
                        return redirect("main:login")
                    else:
                        login(request, user)
                        messages.info(request, f"You are now logged in as {username}")
                        return redirect("main:homepage")
                # date 11/04/2020 end new concept
                else:
                    messages.error(request, "Invalid username or password!")
            else:
                messages.error(request, "Invalid username or password!")
        else:
            messages.error(request, "Invalid username or password!")
    form = AuthenticationForm()
    return render(request,
                  "main/login.html",
                  {"form": form})


def logout_request(request):
    try:
        print(request.session['member_id'])
        logout(request)
        del request.session['member_id']
        messages.info(request, "User Logout successfully!")
    except KeyError:
        pass
    return render(request,
                  "main/logout.html")
