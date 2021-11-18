from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from .forms import AddGrocery, Profile, FilterGrocery
from .models import Grocery


@login_required(login_url="/login")
def add(request):
    if request.method == "POST":
        f = AddGrocery(request.POST)
        if f.is_valid():
            added = f.save(commit=False)
            added.user = request.user
            added.save()
            return render(request, "add.html", {"form": f, "message": "Done"})
        else:

            return render(request, "add.html", {"form": f, "message": "Error"})
    else:
        f = AddGrocery()
        return render(request, "add.html", {"form": f})


@login_required(login_url="/login")
def index(request):
    if request.method == "POST":
        f = FilterGrocery(request.POST)
        if f.is_valid():
            groceries = Grocery.objects.all().filter(user=request.user, date=f.cleaned_data["date_filter"])
            context = {"groceries": groceries, "form": f}
        else:
            error = f.errors
            groceries = Grocery.objects.all().filter(user=request.user)
            context = {"groceries": groceries, "form": f, "error": error}
    else:
        groceries = Grocery.objects.all().filter(user=request.user)
        f = FilterGrocery()
        context = {"groceries": groceries, "form": f}
    return render(request, "index.html", context)


@login_required(login_url="/login")
def update(request, id):
    if request.method == "POST":
        instance = get_object_or_404(Grocery, id=id)
        f = AddGrocery(request.POST, instance=instance)
        if f.is_valid() and instance.user == request.user:
            Grocery.objects.filter(id=id).update(**f.cleaned_data)
        return redirect("/")
    else:
        instance = get_object_or_404(Grocery, id=id)
        f = AddGrocery(
            initial={
                "name": instance.name,
                "quantity": instance.quantity,
                "status": instance.status,
                "date": instance.date,
            }
        )
        return render(request, "update.html", {"form": f, "id": id})


@require_http_methods(["GET"])
@login_required(login_url="/login")
def delete(request, id):
    grocery = Grocery.objects.get(id=id)
    if grocery.user == request.user:
        grocery.delete()
    return HttpResponseRedirect("/")


def register_page(request):
    if request.method == "POST":
        form = Profile(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST["username"]
            password = request.POST["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            context = {"form": form}
            return render(request, "register.html", context)
    else:
        form = Profile()
        context = {"form": form}
        return render(request, "register.html", context)


def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password1"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("Invalid credentials")
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    form = Profile()
    return render(request, "login.html", {"form": form})


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/")
