from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    STYLE_BALANCED = "balanced"
    STYLE_PSYCH = "psych"
    STYLE_SPIRITUAL = "spiritual"
    STYLE_CHOICES = [
        (STYLE_BALANCED, "Balanced"),
        (STYLE_PSYCH, "Psychology"),
        (STYLE_SPIRITUAL, "Spiritual"),
    ]

    PRIVACY_PRIVATE = "private"
    PRIVACY_UNLISTED = "unlisted"
    PRIVACY_PUBLIC = "public"
    PRIVACY_CHOICES = [
        (PRIVACY_PRIVATE, "Private"),
        (PRIVACY_UNLISTED, "Unlisted"),
        (PRIVACY_PUBLIC, "Public"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    display_name = models.CharField(max_length=120, blank=True)
    timezone = models.CharField(max_length=64, default="UTC")
    interpretation_style = models.CharField(
        max_length=16,
        choices=STYLE_CHOICES,
        default=STYLE_BALANCED,
    )
    privacy_default = models.CharField(
        max_length=16,
        choices=PRIVACY_CHOICES,
        default=PRIVACY_PRIVATE,
    )

    def __str__(self) -> str:
        return self.display_name or self.user.get_username()


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self) -> str:
        return self.name


class Symbol(models.Model):
    CATEGORY_ANIMAL = "animal"
    CATEGORY_OBJECT = "object"
    CATEGORY_PLACE = "place"
    CATEGORY_PERSON = "person"
    CATEGORY_EVENT = "event"
    CATEGORY_ABSTRACT = "abstract"
    CATEGORY_CHOICES = [
        (CATEGORY_ANIMAL, "Animal"),
        (CATEGORY_OBJECT, "Object"),
        (CATEGORY_PLACE, "Place"),
        (CATEGORY_PERSON, "Person"),
        (CATEGORY_EVENT, "Event"),
        (CATEGORY_ABSTRACT, "Abstract"),
    ]

    name = models.CharField(max_length=120, unique=True)
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class DreamEntry(models.Model):
    PRIVACY_PRIVATE = "private"
    PRIVACY_UNLISTED = "unlisted"
    PRIVACY_PUBLIC = "public"
    PRIVACY_CHOICES = [
        (PRIVACY_PRIVATE, "Private"),
        (PRIVACY_UNLISTED, "Unlisted"),
        (PRIVACY_PUBLIC, "Public"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dream_entries",
    )
    title = models.CharField(max_length=160)
    narrative = models.TextField()
    date_dreamed = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mood_rating = models.SmallIntegerField(blank=True, null=True)
    emotions = models.JSONField(default=list, blank=True)
    people = models.JSONField(default=list, blank=True)
    settings = models.JSONField(default=list, blank=True)
    privacy = models.CharField(
        max_length=16,
        choices=PRIVACY_CHOICES,
        default=PRIVACY_PRIVATE,
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="dreams")
    symbols = models.ManyToManyField(
        Symbol,
        through="DreamSymbol",
        related_name="dreams",
    )

    class Meta:
        indexes = [
            models.Index(fields=["user", "date_dreamed"]),
            models.Index(fields=["user", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.user.get_username()})"


class DreamSymbol(models.Model):
    dream = models.ForeignKey(
        DreamEntry,
        on_delete=models.CASCADE,
        related_name="dream_symbols",
    )
    symbol = models.ForeignKey(
        Symbol,
        on_delete=models.CASCADE,
        related_name="symbol_dreams",
    )
    confidence = models.FloatField(default=0.0)
    note = models.CharField(max_length=240, blank=True)

    class Meta:
        unique_together = ("dream", "symbol")

    def __str__(self) -> str:
        return f"{self.symbol.name} in {self.dream.title}"


class Interpretation(models.Model):
    ANGLE_PSYCH = "psych"
    ANGLE_SPIRITUAL = "spiritual"
    ANGLE_COMBINED = "combined"
    ANGLE_CHOICES = [
        (ANGLE_PSYCH, "Psychology"),
        (ANGLE_SPIRITUAL, "Spiritual"),
        (ANGLE_COMBINED, "Combined"),
    ]

    dream = models.ForeignKey(
        DreamEntry,
        on_delete=models.CASCADE,
        related_name="interpretations",
    )
    angle = models.CharField(max_length=16, choices=ANGLE_CHOICES)
    summary = models.TextField()
    reflection_questions = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    model = models.CharField(max_length=80, blank=True)
    prompt_version = models.CharField(max_length=32, blank=True)

    def __str__(self) -> str:
        return f"{self.get_angle_display()} for {self.dream.title}"


class ClarifyingQuestion(models.Model):
    dream = models.ForeignKey(
        DreamEntry,
        on_delete=models.CASCADE,
        related_name="clarifying_questions",
    )
    question = models.TextField()
    answer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Q for {self.dream.title}"


class DreamMessage(models.Model):
    ROLE_USER = "user"
    ROLE_ASSISTANT = "assistant"
    ROLE_CHOICES = [
        (ROLE_USER, "User"),
        (ROLE_ASSISTANT, "Assistant"),
    ]

    dream = models.ForeignKey(
        DreamEntry,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(max_length=16, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.get_role_display()} message for {self.dream.title}"
