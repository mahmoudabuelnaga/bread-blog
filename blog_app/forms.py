from django import forms
from . import models

class EmailPostForm(forms.Form):
    name    = forms.CharField(max_length=25)
    email   = forms.EmailField()
    to      = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('name','email','body')
    
class ContactForm(forms.Form):
    name    = forms.CharField(max_length=25)
    subject = forms.CharField(max_length=50)
    email   = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)