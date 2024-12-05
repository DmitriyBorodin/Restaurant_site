from django.contrib import admin

from booking.models import Table, Reservation


@admin.register(Table)
class UserAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'table_status', 'table_size')


@admin.register(Reservation)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('reservation_date', 'reservation_start', 'owner', 'created_at', 'created_at')
