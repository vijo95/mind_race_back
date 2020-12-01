from django.contrib import admin

from . models import (
    UserProfile,
    GuestProfile,
    Player,
    Category,
    Question,
    Game,
    GameProgress
)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'won',
        'lost'
    ]

class GuestProfileAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'guest_id',
        'won',
        'lost'
    ]

class PlayerAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'guest_profile',
        'user_profile'
    ]

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name','id'
    ]

class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'category',
        'question',
        'choice1',
        'choice2',
        'choice3',
        'correct_choice',
        'difficulty'
    ]

class GameAdmin(admin.ModelAdmin):
    list_display = [
        'player1',
        'player2',
        'player_turn',
        'in_progress',
        'start_date',
        'end_date'
    ]

class GameProgressAdmin(admin.ModelAdmin):
    list_display = [
        'game',
        'player',
        'category1',
        'category2',
        'category3',
        'category4',
        'category5',
        'category6',
    ]

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GuestProfile, GuestProfileAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(GameProgress, GameProgressAdmin)
