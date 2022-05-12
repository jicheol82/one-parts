from django import forms
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget
from .models import Feed


class FeedWriteForm(forms.ModelForm):

    # content = SummernoteTextField()

    class Meta:
        model = Feed
        fields = [
            "content",
        ]
        widgets = {"content": SummernoteWidget()}

    # def clean(self):
    #     cleaned_data = super().clean()
    #     contents = cleaned_data.get("content", "")

    #     if contents == "":
    #         self.add_error("content", "Input your contents")
