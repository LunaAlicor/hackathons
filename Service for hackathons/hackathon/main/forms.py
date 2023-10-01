from django import forms
from .models import News, Event, Team


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class NewsEditForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['photo'].widget.attrs.update({'class': 'form-control'})


class EditEventForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all().order_by('-id'),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': 5}),
        label='Teams',
        help_text='Чтобы выбрать несколько команд или тегов зажмите ctrl',
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'organizer', 'content', 'photo', 'status', 'tags', 'registration_date', 'teams']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
            'registration_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditEventForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['class'] = 'form-control'

    def clean_date(self):
        date = self.cleaned_data['date']

        return date

    def clean_registration_date(self):
        registration_date = self.cleaned_data['registration_date']

        return registration_date


class EventForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all().order_by('-id'),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': 5}),
        label='Teams',
        help_text='Чтобы выбрать несколько команд или тегов зажмите ctrl',
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'organizer', 'content', 'photo', 'status', 'tags', 'teams']


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'num_members']
