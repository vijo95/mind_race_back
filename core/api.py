from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import get_user_model
from django.db.models import Q

from . models import (
    UserProfile,
    GuestProfile,
    Player,
    Category,
    Question,
    Game,
    GameProgress
)

from . serializers import (
    UserProfileSerializer,
    GuestProfileSerializer,
    GameSerializer,
    GameProgressSerializer,
    PlayerSerializer,
    QuestionSerializer,
)

import random
import datetime

class CreateGuestProfileAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        guest_id = request.data.get("guest_id", None)
        username = request.data.get("username", None)

        User = get_user_model()

        username_taken = User.objects.filter(username=username)
        if 0 < len(username_taken):
            return Response({"message":"taken"},status=HTTP_200_OK)

        username_taken = GuestProfile.objects.filter(username=username)
        if 0 < len(username_taken):
            return Response({"message":"taken"},status=HTTP_200_OK)

        try:
            guest_profile = GuestProfile.objects.create(
                guest_id=guest_id,
                username=username
            )
            player = Player.objects.create(
                guest_profile=guest_profile,
                username=username
            )
            return Response({"message":"ok"},status=HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)


class SearchContenderAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        username_search = request.data.get("username_search", None)

        User = get_user_model()

        users_list = []

        for user_profile in UserProfile.objects.filter(user__username__icontains=username_search):
                users_list.append(UserProfileSerializer(user_profile).data)

        for guest_profile in GuestProfile.objects.filter(username__icontains=username_search):
            users_list.append(GuestProfileSerializer(guest_profile).data)

        context = {
            "users_list": users_list
        }

        return Response(context,status=HTTP_200_OK)


class CreateGameAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self,request, *args, **kwargs):
        guest_or_user = request.data.get("guest_or_user", None)
        contender_id = request.data.get("contender_id", None)
        guest_id = request.data.get("guest_id", None)

        try:
            if guest_or_user == "guest":
                guest_profile = GuestProfile.objects.get(guest_id=guest_id)
                player1 = Player.objects.get(
                    guest_profile=guest_profile,
                    username=guest_profile.username
                )

            else:
                my_user = self.request.user
                user_profile = UserProfile.objects.get(user=my_user)
                player1 = Player.objects.get(
                    user_profile=user_profile,
                    username=my_user.username
                )


            guest_contender = GuestProfile.objects.filter(id=contender_id)
            if not guest_contender.exists():
                user_profile_contender = UserProfile.objects.filter(id=contender_id)
                player2 = Player.objects.get(
                    user_profile=user_profile_contender[0],
                    username=user_profile_contender[0].user.username
                )
            else:
                player2 = Player.objects.get(
                    guest_profile=guest_contender[0],
                    username=guest_contender[0].username
                )

            if player1 == player2:
                return Response({"message": "same player"},status=HTTP_200_OK)

            game_exists = Game.objects.filter(player1=player1,player2=player2)
            if game_exists.exists():
                if game_exists[0].in_progress:
                    return Response({"message": "already exists"},status=HTTP_200_OK)

            game_exists = Game.objects.filter(player1=player2,player2=player1)
            if game_exists.exists():
                if game_exists[0].in_progress:
                    return Response({"message": "already exists"},status=HTTP_200_OK)

            game = Game.objects.create(
                player1=player1,
                player2=player2,
                player1_username=player1.username,
                player2_username=player2.username,
                player_turn=player1,
                question=None
            )

            game_progress_p1 = GameProgress.objects.create(
                game=game,
                player=player1
            )

            game_progress_p2 = GameProgress.objects.create(
                game=game,
                player=player2
            )

            context = {
                "game_id":game.id
            }

            return Response(context,status=HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)


class HomeAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        guest_id = request.data.get("guest_id", None)

        try:
            if guest_id:
                guest_profile = GuestProfile.objects.get(guest_id=guest_id)
                player = Player.objects.get(guest_profile=guest_profile)
            else:
                user_profile = UserProfile.objects.get(user=self.request.user)
                player = Player.objects.get(user_profile=user_profile)


            games_list = Game.objects.filter(Q(player1=player) | Q(player2=player))

            games_list_progress = []
            for game in games_list:
                games_progress_p1 = GameProgress.objects.get(game=game,player=game.player1)
                games_progress_p2 = GameProgress.objects.get(game=game,player=game.player2)

                games_list_progress.append(
                        [{"game_id": game.id},
                        {"in_progress": game.in_progress},
                        GameProgressSerializer(games_progress_p1).data,
                        GameProgressSerializer(games_progress_p2).data,
                        {"start_date": game.start_date},
                        {"end_date": game.end_date},
                        {"winner": game.winner},
                        {"won": player.username == game.winner}]
                )

            context = {
                "games_list":games_list_progress
            }
            return Response(context,status=HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)


class GameInfoAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        game_id = request.data.get("game_id", None)
        guest_id = request.data.get("guest_id", None)

        try:
            game = Game.objects.get(id=game_id)
            games_progress_p1 = GameProgress.objects.get(game=game,player=game.player1)
            games_progress_p2 = GameProgress.objects.get(game=game,player=game.player2)

            player_turn = game.player_turn
            my_turn = None
            if player_turn != None:
                if guest_id != None:
                    guest_profile = GuestProfile.objects.get(guest_id=guest_id)
                    my_turn = guest_profile.username == player_turn.username
                else:
                    my_turn = self.request.user.username == player_turn.username


            question = game.question
            if question != None:
                question = QuestionSerializer(question).data

            game_info = [
                {"game_id": game.id},
                {"in_progress": game.in_progress},
                GameProgressSerializer(games_progress_p1).data,
                GameProgressSerializer(games_progress_p2).data,
                {"start_date": game.start_date},
                {"turn": PlayerSerializer(game.player_turn).data},
                {"question": question},
                {"my_turn": my_turn},
                {"winner": game.winner},
                {"end_date": game.end_date}
            ]

            return Response(game_info, status=HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)


class GenerateQuestionAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        guest_or_user = request.data.get("guest_or_user", None)
        guest_id = request.data.get("guest_id", None)
        game_id = request.data.get("game_id", None)

        try:
            game = Game.objects.get(id=game_id)
            player_turn = game.player_turn.username
            if guest_or_user == "user":
                if self.request.user.username != player_turn:
                    return Response({"message":"not your turn"}, statuts=HTTP_200_OK)
            elif guest_or_user == "guest":
                guest_profile = GuestProfile.objects.get(guest_id=guest_id)
                if guest_profile.username != player_turn:
                    return Response({"message":"not your turn"}, statuts=HTTP_200_OK)


            category_number = random.randint(1,6)
            category = Category.objects.get(id=category_number)

            question_1_list = Question.objects.filter(category=category, difficulty=1)
            len_q_1 = len(question_1_list)
            question_1 = question_1_list[random.randint(0,len_q_1-1)]

            question_2_list = Question.objects.filter(category=category, difficulty=2)
            len_q_2 = len(question_2_list)
            question_2 = question_2_list[random.randint(0,len_q_2-1)]

            context = {
                "category_id": category.id,
                "category": category.name,
                "question_1": QuestionSerializer(question_1).data,
                "question_2": QuestionSerializer(question_2).data,
            }

            return Response(context,status=HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)


class PickQuestionAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        game_id = request.data.get("game_id")
        question_id = request.data.get("question_id", None)
        guest_id = request.data.get("guest_id", None)

        try:
            if guest_id != None:
                game = Game.objects.get(id=game_id)
                question = Question.objects.get(id=question_id)

                game.question = question
                game.save()

                return Response({"message": "question picked"}, status=HTTP_200_OK)
            else:
                user = self.request.user
                if user.username != None:
                    game = Game.objects.get(id=game_id)
                    question = Question.objects.get(id=question_id)

                    game.question = question
                    game.save()

                    return Response({"message": "question picked"}, status=HTTP_200_OK)
                else:
                    return Response(status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)


class PickOptionAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        game_id = request.data.get("game_id")
        guest_id = request.data.get("guest_id", None)
        option_number = request.data.get("option_number", None)

        try:

            if guest_id != None:
                game = Game.objects.get(id=game_id)
                question = game.question

                if question.correct_choice == option_number:
                    game_progress = GameProgress.objects.get(game=game, player=game.player_turn)
                    category_id = game.question.category.id

                    if category_id == 1:
                        if game_progress.category1 <3:
                            game_progress.category1 += 1
                    elif category_id == 2:
                        if game_progress.category2 <3:
                            game_progress.category2 += 1
                    elif category_id == 3:
                        if game_progress.category3 <3:
                            game_progress.category3 += 1
                    elif category_id == 4:
                        if game_progress.category4 <3:
                            game_progress.category4 += 1
                    elif category_id == 5:
                        if game_progress.category5 <3:
                            game_progress.category5 += 1
                    elif category_id == 6:
                        if game_progress.category6 <3:
                            game_progress.category6 += 1


                    game_progress = GameProgress.objects.get(game=game,player=player)
                    points = game_progress.category1 + game_progress.category2 + game_progress.category3
                    points +=  game_progress.category4 + game_progress.category5 + game_progress.category6
                    if points == 18:
                        game.winner = GuestProfile.objects.get(guest_id=guest_id).username
                        game.in_progress = False
                        game.end_date = datetime.datetime.now()
                        game.player_turn = None

                        game.question = None
                        game_progress.save()
                        game.save()

                        return Response({"message":"winner"}, status=HTTP_200_OK)

                    game.question = None
                    game_progress.save()
                    game.save()
                    return Response({"message":"correct"}, status=HTTP_200_OK)
                else:
                    if game.question.difficulty == 2:
                        game.question = Question.objects.get(category=game.question.category, difficulty=3)
                    else:
                        player_turn = game.player_turn
                        player1 = game.player1
                        player2 = game.player2

                        if player_turn.id == player1.id:
                            game.player_turn = player2
                        else:
                            game.player_turn = player1
                        game.question = None

                    game.save()

                    return Response({"message":"wrong"}, status=HTTP_200_OK)
            else:
                user = self.request.user
                if user.username != None:
                    game = Game.objects.get(id=game_id)
                    question = game.question

                    if question.correct_choice == option_number:
                        game_progress = GameProgress.objects.get(game=game, player=game.player_turn)
                        category_id = game.question.category.id

                        print(category_id)

                        if category_id == 1:
                            if game_progress.category1 <3:
                                game_progress.category1 += 1
                        elif category_id == 2:
                            if game_progress.category2 <3:
                                game_progress.category2 += 1
                        elif category_id == 3:
                            if game_progress.category3 <3:
                                game_progress.category3 += 1
                        elif category_id == 4:
                            if game_progress.category4 <3:
                                game_progress.category4 += 1
                        elif category_id == 5:
                            if game_progress.category5 <3:
                                game_progress.category5 += 1
                        elif category_id == 6:
                            if game_progress.category6 <3:
                                game_progress.category6 += 1


                        points = game_progress.category1 + game_progress.category2 + game_progress.category3
                        points +=  game_progress.category4 + game_progress.category5 + game_progress.category6
                        if points == 18:
                            game.winner = self.request.user.username
                            game.in_progress = False
                            game.end_date = datetime.datetime.now()
                            game.player_turn = None

                            game.question = None
                            game_progress.save()
                            game.save()

                            return Response({"message":"winner"}, status=HTTP_200_OK)

                        game.question = None
                        game_progress.save()
                        game.save()
                        return Response({"message":"correct"}, status=HTTP_200_OK)
                    else:
                        if game.question.difficulty == 2:
                            game.question = Question.objects.get(category=game.question.category, difficulty=3)
                        else:
                            player_turn = game.player_turn
                            player1 = game.player1
                            player2 = game.player2

                            if player_turn.id == player1.id:
                                game.player_turn = player2
                            else:
                                game.player_turn = player1
                            game.question = None

                        game.save()

                        return Response({"message":"wrong"}, status=HTTP_200_OK)
                else:
                    return Response(status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)
