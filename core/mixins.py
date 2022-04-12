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
