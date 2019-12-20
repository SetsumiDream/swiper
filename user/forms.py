from django.forms import ModelForm
from django.forms import ValidationError

from user.models import Profile


class ProfileModelForm(ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'

    def clean_max_distance(self):
        data = self.clean()
        min_distance = data['min_distance']
        max_distance = data['max_distance']
        print(min_distance, max_distance)
        if min_distance >= max_distance:
            raise ValidationError('min distance is gt max')
        return max_distance

    def clean_max_dating_age(self):
        data = self.clean()
        min_dating_age = data['min_dating_age']
        max_dating_age = data['max_dating_age']

        if min_dating_age >= max_dating_age:
            raise ValidationError('min dating_age is gt max')
        return max_dating_age
















# class UserForm(forms.Form):
#     # 用户名，常居地， 性别， 年龄
#     SEX = (
#         ('female', 'female'),
#         ('male', 'male'),
#     )
#
#     nickname = forms.CharField(max_length=128, min_length=6, label='昵称')
#     location = forms.CharField(max_length=128, label='常居地')
#     sex = forms.ChoiceField(choices=SEX)
#     age = forms.IntegerField(min_value=0, max_value=123)
#
