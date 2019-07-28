from django.urls import path,include

from django.conf.urls.static import static
from django.conf import settings
from .views import (PostPageDetail,logout,comment,rep_comment)
urlpatterns = [
    path('<slug:slug>',PostPageDetail.as_view(),name='post-detail'),
    path('<slug:slug>/comment/',comment,name='comment'),
    path('<slug:slug>/comment-<int:id>/',rep_comment,name='comment-rep'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)