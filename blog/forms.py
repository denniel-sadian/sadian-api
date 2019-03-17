from django import forms


class CommentForm(forms.Form):
    full_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    content = forms.CharField()
