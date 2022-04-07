from cProfile import label
from enum import unique
from django import forms
from users.models import User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        # login.html의 form에서 입력된 값 가져오기
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        # 로그인 정보의 일치 여부는 form에서 처리하고
        # 인증은 view에서 처리한다
        try:
            user = User.objects.get(username=email)
            if user.check_password(password):
                # cleaned_data는 딕셔너리
                return self.cleaned_data
            else:
                # 원하는 필드에 에러 메시지를 생성한다
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.Form):
    username = forms.EmailField()
    nickname = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

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
