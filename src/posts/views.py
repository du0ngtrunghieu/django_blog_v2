from django.shortcuts import render, redirect
from django.views.generic import (TemplateView,DetailView,ListView)
from .models import Post,Category,Comment
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import (authenticate,get_user_model,login,logout)
from .forms import (FormLogin,CommentForm)
from django.contrib.auth.forms import AuthenticationForm ,UserCreationForm
from django.contrib import messages
from django.views import View
from django.http import HttpResponseRedirect
from django.db.models import F
# Dữ liệu Index Trang chủ
def Only_data(request):
    Num_Display_Page = 3
    dataTrend = Post.objects.filter(featured = True).order_by('-timestamp')[:3]
    dataCat = Category.objects.filter( featured = True)
    popuPost = Post.objects.filter( featured = True).order_by('-view_count','-comment_count')[:4]
    viewPost = Post.objects.filter( featured = True).order_by('-view_count')[:4]
    commentPost = Post.objects.filter( featured = True).order_by('-comment_count')[:3]
    all_post = Post.objects.get_queryset().order_by('-id')
        
    paginator = Paginator(all_post, Num_Display_Page)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    form = FormLogin()
    context = {
        "posts" : dataTrend,
        "cat" : dataCat,
        "all_post" : posts,
        "popuPost" : popuPost,
        "viewPost" : viewPost,
        "commentPost" : commentPost,
        "form" : form
    }
    return context
def data_form_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    form = AuthenticationForm(request=request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
                
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "Tài khoản hoặc mật khẩu không đúng !!.Vui lòng kiểm tra lại")
    else:
        messages.error(request, "Tài khoản hoặc mật khẩu không đúng !!.Vui lòng kiểm tra lại")
    form = AuthenticationForm()
    return form
class HomePageViewIndex(View):
    
    def get(self , request):
        context = Only_data(request)
        return render(request, "index.html", context)
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, "Tài khoản hoặc mật khẩu không đúng !!.Vui lòng kiểm tra lại")
        else:
            messages.error(request, "Tài khoản hoặc mật khẩu không đúng !!.Vui lòng kiểm tra lại")
        form = AuthenticationForm()
        context = Only_data(request)
        return render(request = request,template_name = "index.html",context= context)
# Dữ liệu Bài Viết   
def Only_data_Post(slug):
    dataCat = Category.objects.filter( featured = True)
    popuPost = Post.objects.filter( featured = True).order_by('-view_count','-comment_count')[:4]
    viewPost = Post.objects.filter( featured = True).order_by('-view_count')[:4]
    commentPost = Post.objects.filter( featured = True).order_by('-comment_count')[:3]
    
    arr = []
    dataPost = get_object_or_404(Post, slug=slug)
    for cat in dataPost.categories.all():
        arr.append(cat)
       
    same_Post = Post.objects.filter( featured = True, categories__in=arr ).distinct().order_by('-timestamp')
    form = FormLogin()
    context = {
        "cat": dataCat,
        "post": dataPost,
        "popuPost": popuPost,
        "viewPost" :viewPost,
        "commentPost": commentPost,
        "same_Post": same_Post,
        "form" : form
    }
    
    return context

class PostPageDetail(DetailView):
    model = Post
    template_name='post.html'
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, "Tài khoản hoặc mật khẩu không đúng !!.Vui lòng kiểm tra lại")
        else:
            messages.error(request, "Tài khoản hoặc mật khẩu không đúng !!.Vui lòng kiểm tra lại")
        form = AuthenticationForm()
        context = Only_data_Post(self.kwargs['slug'])
        return render(request = request,template_name = "post.html",context= context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dataCat = Category.objects.filter( featured = True)
        popuPost = Post.objects.filter( featured = True).order_by('-view_count','-comment_count')[:4]
        viewPost = Post.objects.filter( featured = True).order_by('-view_count')[:4]
        commentPost = Post.objects.filter( featured = True).order_by('-comment_count')[:3]
        context['cat'] = dataCat
        arr = []
        dataPost = get_object_or_404(Post, slug=self.kwargs['slug'])
        if dataPost:
            Post.objects.filter(slug =self.kwargs['slug']).update(view_count = F('view_count')+1)
        for cat in dataPost.categories.all():
            arr.append(cat)
       
        same_Post = Post.objects.filter( featured = True, categories__in=arr ).distinct().order_by('-timestamp')
        
        formcomment = CommentForm()
        comment_post = Comment.objects.filter(post__slug__contains =self.kwargs['slug'],reply__isnull = True).order_by('-id')
        paginator = Paginator(comment_post, 5)
        all_comment = self.request.GET.get('comment')
        try:
            all_comment = paginator.page(all_comment)
        except PageNotAnInteger:
            all_comment = paginator.page(1)
        except EmptyPage:
            all_comment = paginator.page(paginator.num_pages)
        form = FormLogin()
        context['post'] = dataPost
        context['popuPost'] = popuPost
        context['viewPost'] = viewPost
        context['commentPost'] = commentPost
        context['same_Post'] = same_Post
        context['form'] = form
        context['formcomment']=CommentForm
        context['all_comment']=all_comment
        return context
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def comment(request,slug):

    if slug is not None :
        if request.method == 'POST':
            post = get_object_or_404(Post,slug = slug)
            
            comment_form = CommentForm(request.POST,user= request.user , post = post,reply=None)
            if comment_form.is_valid():
                count_comment_update = Comment.objects.filter(post__slug__contains=slug).count()
                Post.objects.filter(slug = slug).update(comment_count = count_comment_update)
                comment_form.save()
                Post.objects.filter(slug = slug).update(comment_count = F('comment_count')+1)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            comment_form = CommentForm()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
def rep_comment(request, slug , id):
    if request.method == 'POST':
        post = get_object_or_404(Post,slug = slug)
        comment_main = get_object_or_404(Comment,id = id)
        if comment_main:
            comment_rep_form = CommentForm(request.POST,user= request.user , post = post,reply = comment_main)
            if comment_rep_form.is_valid():
                count_comment_update = Comment.objects.filter(post__slug__contains=slug).count()
                Post.objects.filter(slug = slug).update(comment_count = count_comment_update)
                comment_rep_form.save()
                Post.objects.filter(slug = slug).update(comment_count = F('comment_count')+1)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        comment_form = CommentForm()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 