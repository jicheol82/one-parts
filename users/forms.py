from django import forms
from django.utils.translation import gettext_lazy as _
from users.models import User, Domain


class AccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        # 메일 도메인을 확인해서 등록회사 여부를 확인한다
        email = self.cleaned_data.get("email")
        domain = email.split("@")[1]
        try:
            Domain.objects.get(name=domain)
            return email
        except Domain.DoesNotExist:
            raise forms.ValidationError(
                "Not registered Domain. Please contact Administrator"
            )
