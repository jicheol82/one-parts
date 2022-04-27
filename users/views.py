from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from core.mixins import OnlyForMember
from users.models import User

# 본인만 가능
class AccountView(OnlyForMember, UpdateView):
    model = User
    template_name = "users/update-profile.html"
    login_url = reverse_lazy("core:login")
    fields = (
        "username",
        "email",
        "company",
        "branch",
        "my_equips",
    )

    def get_object(self):

        return self.request.user


# 본인만 가능
class UpdatePasswordView(OnlyForMember, SuccessMessageMixin, PasswordChangeView):

    template_name = "users/update-password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm new password"
        }
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()
