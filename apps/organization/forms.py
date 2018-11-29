from django import forms
from operation.models import UserAsk


class UserAskForm(forms.Form):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']
