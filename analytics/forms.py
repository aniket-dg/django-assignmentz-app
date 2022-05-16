from django import forms
from django.contrib.auth.forms import UserCreationForm


from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

from analytics.models import File
from users.models import User


class TeacherCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'name','phone_number','password1', 'password2']

    def clean(self):
        super(TeacherCreateForm, self).clean()
        phone_number = self.cleaned_data.get('phone_number')
        if len(str(phone_number)) != 10:
            raise ValidationError(
                _(f'{phone_number} is not an valid mobile number'))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'phone_number')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(
                _(f'{email} is not an valid email'))

        try:
            email = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('email "%s" is already in use.' % email)

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']