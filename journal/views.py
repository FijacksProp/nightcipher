from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import DreamEntryForm
from .models import DreamEntry, DreamMessage, Interpretation


def home(request):
    latest_dream = None
    interpretations = []
    messages = []

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        narrative = request.POST.get("narrative", "").strip()
        if narrative:
            title = request.POST.get("title", "").strip() or "Untitled Dream"
            entry = DreamEntry.objects.create(
                user=request.user,
                title=title,
                narrative=narrative,
                date_dreamed=timezone.localdate(),
            )
            Interpretation.objects.create(
                dream=entry,
                angle=Interpretation.ANGLE_PSYCH,
                summary="Psychological interpretation will appear here.",
            )
            Interpretation.objects.create(
                dream=entry,
                angle=Interpretation.ANGLE_SPIRITUAL,
                summary="Spiritual interpretation will appear here.",
            )
            DreamMessage.objects.create(
                dream=entry,
                role=DreamMessage.ROLE_ASSISTANT,
                content="Thanks for sharing. What emotion felt strongest in this dream?",
            )
            latest_dream = entry

    if request.user.is_authenticated and latest_dream is None:
        latest_dream = (
            DreamEntry.objects.filter(user=request.user).order_by("-created_at").first()
        )

    if latest_dream:
        interpretations = list(latest_dream.interpretations.all())
        messages = list(latest_dream.messages.all())

    return render(
        request,
        "journal/home.html",
        {
            "latest_dream": latest_dream,
            "interpretations": interpretations,
            "messages": messages,
        },
    )


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
    if request.method == "POST":
        message = request.POST.get("message", "").strip()
        if message:
            DreamMessage.objects.create(
                dream=entry,
                role=DreamMessage.ROLE_USER,
                content=message,
            )
            DreamMessage.objects.create(
                dream=entry,
                role=DreamMessage.ROLE_ASSISTANT,
                content="Thanks. I’ll incorporate that into your dream context.",
            )
        return redirect("dream_detail", pk=entry.pk)
    return render(request, "journal/dream_detail.html", {"entry": entry})


@login_required
def dream_delete(request, pk: int):
    entry = get_object_or_404(DreamEntry, pk=pk, user=request.user)
    if request.method == "POST":
        entry.delete()
        return redirect("dreams")
    return render(request, "journal/dream_delete.html", {"entry": entry})


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
