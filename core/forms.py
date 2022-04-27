from django import forms
from django.utils.translation import gettext_lazy as _
from users.models import User


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


class SignUpForm(forms.Form):
    """
    # class Meta는 UserCreationForm외에도 사용가능하다
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")
         widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email Name"}),
        }
    """

    username = forms.CharField(
        label=_("ID"), widget=forms.TextInput(attrs={"placeholder": _("Username")})
    )
    nickname = forms.CharField(
        label=_("nickname"),
        widget=forms.TextInput(attrs={"placeholder": _("Nickname")}),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )
    password1 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            User.objects.get(username=username)
            raise forms.ValidationError("User already exists with that email")
        except User.DoesNotExist:
            return username

    def clean_nickname(self):
        nickname = self.cleaned_data.get("nickname")
        try:
            User.objects.get(nickname=nickname)
            raise forms.ValidationError("Nick name already exists")
            # self.add_error("nickname", "nickname does already exist")
        except User.DoesNotExist:
            return nickname

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password == password1:
            return password
        else:
            raise forms.ValidationError("Password confirmation does not match")

    def save(self):
        username = self.cleaned_data.get("username")
        nickname = self.cleaned_data.get("nickname")
        password = self.cleaned_data.get("password")
        user = User.objects.create_user(username, nickname=nickname, password=password)
        user.save()
