from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import DreamEntryForm
from .models import DreamEntry, DreamMessage, Interpretation, Symbol, Tag
from .services import AIServiceError, dream_chat_reply, interpret_and_extract


def home(request):
    latest_dream = None
    interpretations = []
    messages = []
    ai_error = None

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        narrative = request.POST.get("narrative", "").strip()
        if narrative:
            try:
                ai_data = interpret_and_extract(narrative)
            except AIServiceError as exc:
                ai_error = str(exc)
                ai_data = {}

            title = (ai_data.get("title") or "Untitled Dream").strip()
            entry = DreamEntry.objects.create(
                user=request.user,
                title=title,
                narrative=narrative,
                date_dreamed=timezone.localdate(),
                emotions=ai_data.get("emotions") or [],
                people=ai_data.get("people") or [],
                settings=ai_data.get("settings") or [],
            )
            psych_summary = ai_data.get("psych_summary") or "Psychological interpretation pending."
            spiritual_summary = ai_data.get("spiritual_summary") or "Spiritual interpretation pending."
            Interpretation.objects.create(
                dream=entry,
                angle=Interpretation.ANGLE_PSYCH,
                summary=psych_summary,
            )
            Interpretation.objects.create(
                dream=entry,
                angle=Interpretation.ANGLE_SPIRITUAL,
                summary=spiritual_summary,
            )
            tags = ai_data.get("tags") or []
            if tags:
                tag_objs = [Tag.objects.get_or_create(name=name)[0] for name in tags]
                entry.tags.set(tag_objs)
            symbols = ai_data.get("symbols") or []
            if symbols:
                symbol_objs = [
                    Symbol.objects.get_or_create(
                        name=name, defaults={"category": Symbol.CATEGORY_ABSTRACT}
                    )[0]
                    for name in symbols
                ]
                entry.symbols.set(symbol_objs)
            followup = ai_data.get("followup_question") or (
                "What emotion felt strongest in this dream?"
            )
            DreamMessage.objects.create(
                dream=entry,
                role=DreamMessage.ROLE_ASSISTANT,
                content=followup,
            )
            latest_dream = entry

    if request.user.is_authenticated and latest_dream is None:
        latest_dream = (
            DreamEntry.objects.filter(user=request.user).order_by("-created_at").first()
        )

    if latest_dream:
        interpretations = list(latest_dream.interpretations.all())
        messages = list(latest_dream.messages.all())

    context = {
        "latest_dream": latest_dream,
        "interpretations": interpretations,
        "messages": messages,
        "ai_error": ai_error,
    }

    if request.headers.get("HX-Request") == "true" and request.method == "POST":
        return render(request, "journal/partials/home_session.html", context)

    return render(request, "journal/home.html", context)


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
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in entry.messages.all().order_by("-created_at")[:8][::-1]
            ]
            try:
                reply = dream_chat_reply(entry.narrative, history, message)
            except AIServiceError as exc:
                reply = f"AI unavailable: {exc}"
            DreamMessage.objects.create(
                dream=entry,
                role=DreamMessage.ROLE_ASSISTANT,
                content=reply or "Thanks. I’ll incorporate that into your dream context.",
            )
        if request.headers.get("HX-Request") == "true":
            return render(
                request,
                "journal/partials/dream_messages.html",
                {"entry": entry},
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
