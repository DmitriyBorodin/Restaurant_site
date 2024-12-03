from django.contrib import admin

from users.models import User, Feedback


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'first_name', 'last_name')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'message', 'created_at')