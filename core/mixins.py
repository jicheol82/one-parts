from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages


class OnlyForMember(LoginRequiredMixin):
    login_url = reverse_lazy("core:login")


class OnlyForGuest(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "You've logged in already")
        return redirect("core:home")


class OnlyForVerifiedMember(UserPassesTestMixin):
    def test_func(self):
        try:
            self.request.user.company_verified
            return self.request.user.company_verified
        except Exception:
            return False

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "Please complete company verification.")
            return redirect("users:profile", self.request.user.pk)
        else:
            messages.error(self.request, "Please log in first")
            return redirect("core:login")
