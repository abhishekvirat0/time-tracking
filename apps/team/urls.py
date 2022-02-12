from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import AddTeamView, GetTeamView

urlpatterns = [
    path('add', AddTeamView.as_view()),
    path('team/get', GetTeamView.as_view())
]