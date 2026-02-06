from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DreamEntryForm
from .models import DreamEntry


def home(request):
    return render(request, "journal/home.html")


def community(request):
    return render(request, "journal/community.html")


@login_required
def dreams(request):
    entries = DreamEntry.objects.filter(user=request.user).order_by("-date_dreamed")
    return render(request, "journal/dreams_list.html", {"entries": entries})


@login_required
def dream_new(request):
    if request.method == "POST":
        form = DreamEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(user=request.user)
            return redirect("dream_detail", pk=entry.pk)
    else:
        form = DreamEntryForm()
    return render(request, "journal/dream_form.html", {"form": form})


@login_required
def dream_detail(request, pk: int):
    entry = get_object_or_404(DreamEntry, pk=pk, user=request.user)
    return render(request, "journal/dream_detail.html", {"entry": entry})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dreams")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})
