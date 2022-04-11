from pyexpat import model
from django.shortcuts import render
from django.views.generic import DetailView
from users.models import User


class ProfileView(DetailView):
    model = User
    context_object_name = "context_obj"
