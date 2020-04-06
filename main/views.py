from django.http import HttpResponse
from django.shortcuts import render, redirect
from main.models import Tutorial, TutorialCategory, TutorialSeries
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm


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
                      context={ # "tutorial_series": matching_series,
                                "part_ones": series_urls})

    tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]
    if single_slug in tutorials:
        this_tutorial = Tutorial.objects.get(tutorial_slug=single_slug)
        tutorials_form_series = Tutorial.objects.filter(
            tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by("tutorial_published")

        this_tutorial_idx = list(tutorials_form_series).index(this_tutorial)

        return render(request=request,
                      template_name="main/tutorial.html",
                      context={"tutorial": this_tutorial,
                               "sidebar": tutorials_form_series,
                               "this_tutorial_idx": this_tutorial_idx})

    return HttpResponse(f"{single_slug} does not correspond to anything!")


def homepage(request):
    return render(request=request,
                  template_name="main/categories.html",
                  context={"categories": TutorialCategory.objects.all()}
                  )


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
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
                    request.session['member_id'] = user.id
                    print(request.session['member_id'])
                    # request.session.set_expiry(30)  # sets the exp. value of the session
                    request.session.set_expiry(request.session.get_expiry_age())
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}")
                    # if req is None:
                    #     messages.error(request, "Your session has been expired!")
                    #     return redirect("main:homepage")
                    return redirect("main:homepage")
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
    return redirect("main:homepage")
