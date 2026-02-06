from django.contrib import admin

from .models import (
    ClarifyingQuestion,
    DreamEntry,
    DreamSymbol,
    Interpretation,
    Symbol,
    Tag,
    UserProfile,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "interpretation_style", "privacy_default")
    search_fields = ("user__username", "display_name")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(DreamEntry)
class DreamEntryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "date_dreamed", "privacy", "created_at")
    list_filter = ("privacy", "date_dreamed")
    search_fields = ("title", "narrative", "user__username")
    autocomplete_fields = ("tags", "symbols")
    date_hierarchy = "date_dreamed"


@admin.register(DreamSymbol)
class DreamSymbolAdmin(admin.ModelAdmin):
    list_display = ("dream", "symbol", "confidence")
    list_filter = ("symbol",)
    search_fields = ("dream__title", "symbol__name")


@admin.register(Interpretation)
class InterpretationAdmin(admin.ModelAdmin):
    list_display = ("dream", "angle", "model", "created_at")
    list_filter = ("angle",)
    search_fields = ("dream__title", "summary")


@admin.register(ClarifyingQuestion)
class ClarifyingQuestionAdmin(admin.ModelAdmin):
    list_display = ("dream", "created_at")
    search_fields = ("dream__title", "question", "answer")
