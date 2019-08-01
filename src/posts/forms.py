from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.forms.widgets import PasswordInput, TextInput,EmailInput
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Comment
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

User = get_user_model()
class FormLogin(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'frm-input','placeholder': 'UserName'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'frm-input','placeholder':'Password'}))
    

class FormRegister(forms.Form):
    username = forms.CharField(label='UserName',widget=TextInput(attrs={'class': 'frm-input','placeholder': 'UserName'}))
    password1 = forms.CharField(label='Mật khẩu',widget=PasswordInput(attrs={'class': 'frm-input','placeholder':'Password'}))
    password2 = forms.CharField(label='Mật khẩu xác minh',widget=PasswordInput(attrs={'class': 'frm-input','placeholder':'Nhập Lại Mật Khẩu'}))
    email =forms.EmailField(widget=forms.EmailInput(attrs={'class': 'frm-input','placeholder':'Email'}))
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
          
            raise  ValidationError(_("Username này đã được sử dụng .Vui lòng nhập lại !"),code='invalid')
        return username
 
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email này đã được sử dụng . Vui lòng nhập lại")
        return email
 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
 
        if password1 and password2 and password1 != password2:
            raise ValidationError("Mật khẩu xác minh không khớp !")
 
        return password2
 
    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


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