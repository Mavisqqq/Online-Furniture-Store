from django.contrib.auth.forms import *
from furniture.models import *


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(required=True, label='Имя пользователя', min_length=5, max_length=50, help_text='Максимум 50 символов', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password1 = forms.CharField(required=True, label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required=True, label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label='E-Mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserForgotPasswordForm(PasswordResetForm):
    #Запрос на восстановление пароля
    def __init__(self, *args, **kwargs):
        #Обновление стилей формы
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class UserSetNewPasswordForm(SetPasswordForm):
    #Изменение пароля пользователя после подтверждения
    def __init__(self, *args, **kwargs):
       # Обновление стилей формы
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text', )

