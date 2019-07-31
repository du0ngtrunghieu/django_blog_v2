from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Comment

User = get_user_model()
class FormLogin(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'frm-input','placeholder': 'UserName'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'frm-input','placeholder':'Password'}))

class FormRegister(UserCreationForm):
    class Meta:
        model = User
        fields =[
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'email',
        ]

    
    
    
    

class CommentForm(forms.ModelForm):
    body = forms.CharField( required=True,max_length=500 , widget=forms.Textarea(attrs={'class': "form-control pl-3 pt-3" ,'rows':4, 'cols':90, 'placeholder':"Nhập bình luận của bạn vào đây...",'id':"exampleFormControlTextarea1"}))
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        self.post = kwargs.pop('post', None)
        self.reply = kwargs.pop('reply', None)
        super().__init__(*args, **kwargs)
    def save(self, commit = True):
       
       comment = super().save(commit = False) # Call the real save() method
       comment.user = self.user
       comment.post = self.post
       comment.reply = self.reply 
       comment.save()
    class Meta:
        model= Comment
        fields = ('body',)