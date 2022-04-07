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
