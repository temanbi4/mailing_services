from django import forms
from service.models import Mailing


class MailingForm(forms.ModelForm):
    """Класс-представление для создания рассылки."""

    # Поле для выбора даты и времени с виджетом, который подсказывает пользователю верный формат данных для ввода
    date_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите дату и время в формате ДД.ММ.ГГГГ ЧЧ:ММ'}))

    class Meta:
        model = Mailing
        fields = ('date_time', 'periodicity', 'client', 'message')

    def __init__(self, *args, **kwargs):
        """Стилизация формы."""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
