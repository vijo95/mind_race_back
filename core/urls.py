from django.urls import path
from . api import (
    CreateGuestProfileAPIView,
    SearchContenderAPIView,
    CreateGameAPIView,
    HomeAPIView,
    GameInfoAPIView,
    GenerateQuestionAPIView,
    PickQuestionAPIView,
    PickOptionAPIView
)


urlpatterns = [
    path('guest-create-profile/', CreateGuestProfileAPIView.as_view(), name="guest-create-profile"),
    path('search-contender/', SearchContenderAPIView.as_view(), name="search-contender"),
    path('create-game/', CreateGameAPIView.as_view(), name="create-game"),
    path('home/', HomeAPIView.as_view(), name="home"),
    path('game-info/', GameInfoAPIView.as_view(), name="game-info"),
    path('generate-question/', GenerateQuestionAPIView. as_view(), name="generate-question"),
    path('pick-question/', PickQuestionAPIView.as_view(), name="pick-question"),
    path('pick-option/', PickOptionAPIView.as_view(), name="pick-option")
]
