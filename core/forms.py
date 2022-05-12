from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from users.models import User, Domain


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_("ID"), widget=forms.TextInput(attrs={"placeholder": _("Username")})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Password")})
    )

    def clean(self):
        # login.html의 form에서 입력된 값 가져오기
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        # 로그인 정보의 일치 여부는 form에서 처리하고
        # 인증은 view에서 처리한다
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # cleaned_data는 딕셔너리
                return self.cleaned_data
            else:
                # 원하는 필드에 에러 메시지를 생성한다
                self.add_error(
                    "password", forms.ValidationError(_("Password is wrong"))
                )
        except User.DoesNotExist:
            self.add_error("username", forms.ValidationError(_("ID does not exist")))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User

        fields = (
            "username",
            "email",
            "password",
        )

    password = forms.CharField(
        label=_("Password"),
        validators=[password_validation.validate_password],
        widget=forms.PasswordInput(),
    )

    password1 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(),
    )

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

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        user.set_password(password)
        user.save()
