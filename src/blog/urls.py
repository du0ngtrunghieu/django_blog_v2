"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin 
from django.urls import path,include
from posts.views import HomePageView,logout_view,comment,signup,Signin,CategoryPageView,handler404view
from django.conf.urls.static import static
from django.conf import settings
from filebrowser.sites import site
from django import views
from django.conf.urls import handler400,handler500

site.directory = "uploads/"

urlpatterns = [
    path('admin/filebrowser/', site.urls),
    
    #path('froala_editor/', include('froala_editor.urls')),
    path('accounts/', include('allauth.urls')),
    path('jet/',include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  
    path('admin/', admin.site.urls),
    path('',HomePageView,name='home'),
    path('post/', include('posts.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('logout/',logout_view , name='logout'),
    path('signup/',signup,name='signup'),
    path('<slug:slug>/',CategoryPageView,name='category'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404=handler404view
handler500=handler500
