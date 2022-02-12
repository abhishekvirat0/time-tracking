from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

# Create your views here.

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.team.models import Team


class GetTeamView(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.userProfile.active_team_id:
                team = Team.objects.filter(pk=request.user.userProfile.active_team_id)
                print(team)
                return HttpResponse(list(team), content_type="application/json")
        return JsonResponse({'team': None})


class AddTeamView(GenericAPIView):

    def post(self, request):
        title = request.data['title']
        if title:
            if Team.objects.filter(title=title).exists():
                return JsonResponse({'status': 'Team already exists!'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            team = Team.objects.create(title=title, created_by=request.user)
            team.members.add(request.user)
            team.save()
            userprofile = request.user.userProfile
            userprofile.active_team_id = team.id
            userprofile.save()

            return JsonResponse({'status': 'success'}, status=status.HTTP_200_OK)

        return JsonResponse({'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)
