from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib import messages


class OnlyForMember(LoginRequiredMixin):
    login_url = reverse_lazy("core:login")

    def handle_no_permission(self):
        messages.error(self.request, "Please log in first")
        return super().handle_no_permission()


class OnlyForGuest(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "You've logged in already")
        return redirect("core:home")


class OnlyForVerifiedMember(UserPassesTestMixin):
    login_url = reverse_lazy("core:login")

    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_verified
        return False

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "Please complete your company verifcation")
            return redirect("users:account")
        else:
            messages.error(self.request, "Please log in first")
            return super().handle_no_permission()
