from gc import get_objects
from django.shortcuts import redirect
from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from core.mixins import OnlyForMember
from users.models import User
from users.forms import AccountForm

# 본인만 가능
class AccountUpdateView(OnlyForMember, UpdateView):
    model = User
    form_class = AccountForm
    template_name = "users/account.html"
    login_url = reverse_lazy("core:login")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        result = self.object.verify_email()
        if result:
            form.save()
            messages.success(self.request, "success")
        else:
            messages.error(self.request, "Fail update")
            return redirect("users:account")
        return super().form_valid(form)


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
