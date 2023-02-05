from rest_framework.views import APIView, Response, Request, status
from .models import Team
from django.forms.models import model_to_dict
from .validators import is_not_validate_titles, ValidateTitlesError, ValidateFirstCupError, is_not_validate_first_cup, is_not_validate_titles_quantity
import ipdb
# Create your views here.


class TeamView(APIView):
    def get(self, request: Request) -> Request:
        teams = Team.objects.all()

        teams_list = []

        for team in teams:
            teams_dict = model_to_dict(team)
            teams_list.append(teams_dict)

        return Response(teams_list, status.HTTP_200_OK)

    def post(self, request: Request) -> Request:
        try:
            valid_data = is_not_validate_titles(request.data["titles"])

        except ValidateTitlesError as error:
            return Response({'error': error.message}, status.HTTP_400_BAD_REQUEST)

        try:
            valid_data = is_not_validate_first_cup(request.data["first_cup"])

        except ValidateFirstCupError as error:
            return Response({'error': error.message}, status.HTTP_400_BAD_REQUEST)

        try:
            valid_data = is_not_validate_titles_quantity(
                request.data["titles"], request.data["first_cup"])

        except ValidateTitlesError as error:
            return Response({'error': error.message}, status.HTTP_400_BAD_REQUEST)

        team = Team.objects.create(**request.data)
        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_201_CREATED)


class TeamDetailView(APIView):
    def get(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({'message': 'Team not found'}, status.HTTP_404_NOT_FOUND)

        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)

    def delete(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({'message': 'Team not found'}, status.HTTP_404_NOT_FOUND)

        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({'message': 'Team not found'}, status.HTTP_404_NOT_FOUND)

        for key, value in request.data.items():
            setattr(team, key, value)

        team.save()
        team_dict = model_to_dict(team)


        return Response(team_dict, status.HTTP_200_OK)
