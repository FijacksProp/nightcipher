from django import forms

from .models import DreamEntry, Symbol, Tag


class DreamEntryForm(forms.ModelForm):
    tags_input = forms.CharField(required=False)
    symbols_input = forms.CharField(required=False)
    emotions_input = forms.CharField(required=False)
    people_input = forms.CharField(required=False)
    settings_input = forms.CharField(required=False)

    class Meta:
        model = DreamEntry
        fields = [
            "title",
            "date_dreamed",
            "narrative",
            "mood_rating",
            "privacy",
        ]
        widgets = {
            "date_dreamed": forms.DateInput(attrs={"type": "date"}),
        }

    @staticmethod
    def _split_list(value: str) -> list[str]:
        if not value:
            return []
        return [item.strip() for item in value.split(",") if item.strip()]

    def save(self, user, commit=True):
        instance = super().save(commit=False)
        instance.user = user
        instance.emotions = self._split_list(self.cleaned_data.get("emotions_input", ""))
        instance.people = self._split_list(self.cleaned_data.get("people_input", ""))
        instance.settings = self._split_list(self.cleaned_data.get("settings_input", ""))
        if commit:
            instance.save()
        tags = self._split_list(self.cleaned_data.get("tags_input", ""))
        if tags:
            tag_objs = [Tag.objects.get_or_create(name=name)[0] for name in tags]
            instance.tags.set(tag_objs)
        symbols = self._split_list(self.cleaned_data.get("symbols_input", ""))
        if symbols:
            symbol_objs = [
                Symbol.objects.get_or_create(
                    name=name,
                    defaults={"category": Symbol.CATEGORY_ABSTRACT},
                )[0]
                for name in symbols
            ]
            instance.symbols.set(symbol_objs)
        return instance
