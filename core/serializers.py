from rest_framework import serializers

from . models import (
    UserProfile,
    GuestProfile,
    Player,
    Category,
    Question,
    Game,
    GameProgress
)

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserProfile
        fields = [
            'id','username',
            'won','lost',
        ]


class GuestProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestProfile
        fields = [
            'id','username',
            'won','lost'
        ]


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            'id','player1_username',
            'player2_username'
        ]


class GameProgressSerializer(serializers.ModelSerializer):
    player_username = serializers.ReadOnlyField(source='player.username')
    class Meta:
        model = GameProgress
        fields = [
            'player_username',
            'category1',
            'category2',
            'category3',
            'category4',
            'category5',
            'category6',
        ]

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            'id','username'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    category_id = serializers.ReadOnlyField(source='category.id')
    class Meta:
        model = Question
        fields = [
            'id','question',
            'choice1',
            'choice2',
            'choice3',
            'correct_choice',
            'difficulty',
            'category_id'
        ]
