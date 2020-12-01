from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    won = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class GuestProfile(models.Model):
    username = models.CharField(max_length=64, blank=True, null=True)
    guest_id = models.CharField(max_length=64, blank=True, null=True)
    won = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Player(models.Model):
    username = models.CharField(max_length=64, blank=True, null=True)
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    guest_profile = models.ForeignKey(
        GuestProfile,
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    def __str__(self):
        if self.user_profile:
            return f"{self.user_profile.user.username}"
        else:
            return f"{self.guest_profile.username}"


class Category(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return f"{self.id} | {self.name}"


class Question(models.Model):
        category = models.ForeignKey(
            Category,
            on_delete=models.SET_NULL,
            blank=True, null=True
        )
        question = models.CharField(max_length=256, blank=True, null=True)
        choice1 = models.CharField(max_length=32, blank=True, null=True)
        choice2 = models.CharField(max_length=32, blank=True, null=True)
        choice3 = models.CharField(max_length=32, blank=True, null=True)
        correct_choice = models.IntegerField(blank=True, null=True)
        difficulty = models.IntegerField(blank=True, null=True)



class Game(models.Model):
    player1 = models.ForeignKey(
        Player,
        related_name="player1",
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    player2 = models.ForeignKey(
        Player,
        related_name="player2",
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    player_turn = models.ForeignKey(
        Player,
        related_name="player_turn",
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    player1_username = models.CharField(max_length=64, blank=True, null=True)
    player2_username = models.CharField(max_length=64, blank=True, null=True)
    winner = models.CharField(max_length=64, blank=True, null=True)
    in_progress = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.player1} | {self.player2}"

class GameProgress(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    category1 = models.IntegerField(default=0)
    category2 = models.IntegerField(default=0)
    category3 = models.IntegerField(default=0)
    category4 = models.IntegerField(default=0)
    category5 = models.IntegerField(default=0)
    category6 = models.IntegerField(default=0)

    def __str__(self):
        return self.player.username
