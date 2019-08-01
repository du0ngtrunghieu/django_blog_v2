from django.shortcuts import render, redirect
from django.views.generic import (TemplateView,DetailView,ListView)
from .models import Post,Category,Comment
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import (authenticate,get_user_model,login,logout)
from .forms import (FormLogin,CommentForm,FormRegister)
from django.contrib.auth.forms import AuthenticationForm ,UserCreationForm
from django.contrib import messages
from django.views import View
from django.http import HttpResponseRedirect
from django.db.models import F
from django.contrib.auth.decorators import login_required

# Dữ liệu Index Trang chủ

def data_category_base(request , slug):
    categories = get_object_or_404(Category,slug = slug)
    
    PostinCate = Post.objects.filter(featured = True ,categories= categories).order_by('-timestamp')
    Num_Display_Page = 1
    Trend_data = Post.objects.filter(featured = True).order_by('-timestamp')[:3]
    Cat_data = Category.objects.filter( featured = True)
    Postpopu_data = Post.objects.filter( featured = True).order_by('-view_count','-comment_count')[:4]
    Post_mostview_data = Post.objects.filter( featured = True).order_by('-view_count')[:4]
    Post_mostcomment_data = Post.objects.filter( featured = True).order_by('-comment_count')[:3]
    
        
    paginator = Paginator(PostinCate, Num_Display_Page)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        "posts" : Trend_data,
        "cat" : Cat_data,
        "PostinCate" : posts,
        "popuPost" : Postpopu_data,
        "viewPost" : Post_mostview_data,
        "commentPost" : Post_mostcomment_data,
        
        "title":categories.nameCat
    }
    return context
def data_base(request,fsignin,fsignup):
    Num_Display_Page = 3
    Trend_data = Post.objects.filter(featured = True).order_by('-timestamp')[:3]
    Cat_data = Category.objects.filter( featured = True)
    Postpopu_data = Post.objects.filter( featured = True).order_by('-view_count','-comment_count')[:4]
    Post_mostview_data = Post.objects.filter( featured = True).order_by('-view_count')[:4]
    Post_mostcomment_data = Post.objects.filter( featured = True).order_by('-comment_count')[:3]
    all_post = Post.objects.get_queryset().order_by('-id')
        
    paginator = Paginator(all_post, Num_Display_Page)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        "posts" : Trend_data,
        "cat" : Cat_data,
        "all_post" : posts,
        "popuPost" : Postpopu_data,
        "viewPost" : Post_mostview_data,
        "commentPost" : Post_mostcomment_data,
        "form" : fsignin,
        "form_reg":fsignup,
        
    }
    return context

# Dữ liệu Bài Viết   
def data_base_for_post(slug):
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
        
        
    }
    
    return context

def HomePageView(request):
    if request.POST.get('login') == 'login':
        formreg = FormRegister()
        if request.method =='POST':
           
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
            form = FormLogin()
        
            context = data_base(request,form,formreg)
            context.title="Trang Chủ"
            return render(request = request,template_name = "index.html",context= context)
        else:
            form = FormLogin()
            context = data_base(request,form,formreg)
        context['title']="Trang Chủ"
        return render(request, "index.html", context)
    elif request.POST.get('register') == 'register':
        form = FormLogin()
        if request.method == 'POST':
            formreg = FormRegister(request.POST)
            if formreg.is_valid():
                formreg.save()
                username = formreg.cleaned_data.get('username')
                raw_password = formreg.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

            context = data_base(request,form,formreg)
            return render(request, "index.html", context)
        else:
            formreg = FormRegister()
            context = data_base(request,form,formreg)
        return render(request, "index.html", context)
    else:
        form = FormLogin()
        form_reg = FormRegister()
        
        context = data_base(request,form,form_reg)
        context['title']="Trang Chủ"
        return render(request, "index.html", context)
    

def CategoryPageView(request,slug):
    if request.POST.get('login') == 'login':
        formreg = FormRegister()
        if request.method =='POST':
           
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
            form = FormLogin()
        
            context = data_category_base(request,slug)
            context['form'] =form
            context['form_reg'] =formreg
            
            return render(request = request,template_name = "category.html",context= context)
        else:
            form = FormLogin()
            context = data_category_base(request,slug)
            context['form'] =form
        
        return render(request, "category.html", context)
    elif request.POST.get('register') == 'register':
        form = FormLogin()
        if request.method == 'POST':
            formreg = FormRegister(request.POST)
            if formreg.is_valid():
                formreg.save()
                username = formreg.cleaned_data.get('username')
                raw_password = formreg.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

            context = data_category_base(request,slug)
            context['form_reg'] =formreg
            context['form'] =form
            return render(request, "category.html", context)
        else:
            context = data_category_base(request,slug)
            formreg = FormRegister()
            context['form_reg'] =formreg
            context['form'] =form
           
        return render(request, "category.html", context)

    else:
        context = data_category_base(request,slug)
        form = FormLogin()
        formreg = FormRegister()
        context['form_reg'] =formreg
        context['form'] =form
        
   
        return render(request, "category.html", context)


#dang nhap

def Signin(request):
    pass



class PostPageDetail(DetailView):
    model = Post
    template_name='post.html'
    def post(self, request, *args, **kwargs):
        pass

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
        array_comment =[]
        same_Post = Post.objects.filter( featured = True, categories__in=arr ).distinct().order_by('-timestamp')
        
        formcomment = CommentForm()
        comment_post = Comment.objects.filter(post__slug__contains =self.kwargs['slug'],reply__isnull = True).order_by('-id')
        comment_in_post = Comment.objects.filter(post__slug__contains =self.kwargs['slug']).order_by('-id')
        
        
        paginator = Paginator(comment_post, 5)
        all_comment = self.request.GET.get('comment')
        try:
            all_comment = paginator.page(all_comment)
        except PageNotAnInteger:
            all_comment = paginator.page(1)
        except EmptyPage:
            all_comment = paginator.page(paginator.num_pages)
        form = FormLogin()
        formreg = FormRegister()
        context['post'] = dataPost
        context['popuPost'] = popuPost
        context['viewPost'] = viewPost
        context['commentPost'] = commentPost
        context['same_Post'] = same_Post
        context['form'] = form
        context['form_reg'] = formreg
        context['formcomment']=CommentForm
        context['all_comment']=all_comment
        context['comment_in_post']=comment_in_post
        context['title'] = dataPost.title
        return context
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required
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
@login_required
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
# @login_required
# def reaction_post(request , slug, vote):
#     # 1: love
#     # 2: 
#     if request.method == 'POST':
#         post = get_object_or_404(Post,slug = slug)
#         if post:

def signup(request):
    if request.method == 'POST':
        form = FormRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 