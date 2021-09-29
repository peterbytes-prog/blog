from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=50,widget=forms.TextInput({'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput({'class': 'form-control'}))
    to = forms.EmailField(widget=forms.TextInput({'class': 'form-control'}))
    comment = forms.CharField(required=False, widget=forms.Textarea({'class': 'form-control','style':'height:15rem'}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control','style':'height:10rem'}),
        }
class ContactForm(forms.Form):
    name = forms.CharField(max_length=50,widget=forms.TextInput({'class': 'form-control'}))
    email = forms.EmailField(
        required=False,
        widget=forms.TextInput({'class': 'form-control'})
        )
    phone= forms.RegexField(
        required=False,
        regex=r'^\+?1?\d{9,15}$',
        widget=forms.TextInput({'class': 'form-control','type':'tel'}),
        )
    message = forms.CharField(required=True, widget=forms.Textarea({'class': 'form-control','style':'height:15rem'}))
