from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import SelectDateWidget
from django.utils import timezone
from datetime import time, datetime
from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['reservation_date', 'reservation_start', 'guests_amount', 'reservation_commentary']

        year = datetime.now().year
        current_month = datetime.now().month

        date = datetime.now().day

        widgets = {
            'reservation_date': SelectDateWidget(years=range(year, year+2)),
            'reservation_start': forms.Select(attrs={'id': 'id_time'}),
            'reservation_commentary': forms.Textarea(
                attrs={'rows': 3, 'style': 'width: 40%;', 'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Генерация временных интервалов с шагом в 30 минут
        time_choices = [
            (datetime.strptime(f"{hour}:{minute:02}", "%H:%M").time(),
             f"{hour}:{minute:02}")
            for hour in range(9, 23)  # Ограничение с 9:00 до 23:30
            for minute in (0, 30)
        ]
        self.fields['reservation_start'].widget = forms.Select(choices=time_choices)

    def clean_reservation_start(self):
        reservation_date = self.cleaned_data.get('reservation_date')
        reservation_start = self.cleaned_data.get('reservation_start')

        if reservation_date < timezone.localdate():
            raise ValidationError("Нельзя бронировать на прошедшие дни.")

        # Проверка на то, что время не меньше текущего, если дата сегодняшняя
        if reservation_date == timezone.localdate():
            if reservation_start <= timezone.localtime().time():
                raise ValidationError("Вы не можете выбрать время в прошлом.")

        # Проверка, что время в пределах рабочего времени ресторана (с 9 до 23)
        if not (time(9, 0) <= reservation_start <= time(23, 0)):
            raise ValidationError("Время резервирования должно быть в пределах с 9:00 до 23:00.")

        return reservation_start
