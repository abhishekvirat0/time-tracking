from .models import Team


def active_team(request):
    if request.user.is_authenticated:

        if request.userProfile.active_team_id:
            team = Team.objects.get(pk=request.userProfile.active_team_id)

            return {'active_team': team}
        return {'active_team': None}