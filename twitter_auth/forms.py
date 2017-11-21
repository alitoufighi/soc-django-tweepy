from .models import Post

from django import forms

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text', 'media',)

# class TelegramForm(forms.ModelForm):
#
#     class Meta:
#         model = TelegramInfo
#         fields = ('channel_id')

# class SignupForm(forms.)