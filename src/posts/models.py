from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from .untils import generate_unique_slug
from django.urls import reverse
from filebrowser.fields import FileBrowseField
from mptt.models import MPTTModel, TreeForeignKey
from tinymce import HTMLField
from django.conf import settings

# Create your models here.
User = get_user_model()


class Author(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   profile_pic = models.ImageField('Avatar',upload_to='uploads/' )
   body = models.CharField("Thông Tin Thêm", max_length=500)
   def __str__(self):
       return self.user.username
   

class Category(MPTTModel):
    nameCat = models.CharField('Tên Thể Loai',max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',verbose_name='Thể Loại Cha')
    slug = models.SlugField(unique=True,editable=False , blank = True)
    timestamp = models.DateTimeField('Ngày Tạo', auto_now=False, auto_now_add=True)
    featured = models.BooleanField(default = True)
    class MPTTMeta:
        
        level_attr = 'mptt_level'
        order_insertion_by = ['nameCat']
    class Meta:
        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "Thể Loại"
    def __str__(self):
        return self.nameCat
    
    def save(self, *args, **kwargs):
        if self.slug:  
            if slugify(self.nameCat) != self.slug:
                self.slug = generate_unique_slug(Category, self.nameCat)
        else: 
            self.slug = generate_unique_slug(Category, self.nameCat)
        super(Category, self).save(*args, **kwargs)
# class Category (models.Model):
#     nameCat = models.CharField(
#       'Tên Thể Loại', max_length=200, help_text='Vui lòng nhập Tên cho Thể Loại')
#     slug = models.SlugField(unique=True,editable=False , blank = True)
#     parent = models.ForeignKey('self',blank=True, null=True ,related_name='children',on_delete = models.CASCADE)
#     timestamp = models.DateTimeField('Ngày Tạo', auto_now=False, auto_now_add=True)
#     featured = models.BooleanField(default = True)
    
#     class Meta:
#         unique_together = ('slug', 'parent',)    
#         verbose_name_plural = "Thể Loại"
#     def __str__(self):                           
#         return self.nameCat
#     def save(self, *args, **kwargs):
       
#         if self.parent:
#             if self.parent.parent:
#                 self.parent = None
                
           
        

#         if self.slug:  
#             if slugify(self.nameCat) != self.slug:
#                 self.slug = generate_unique_slug(Category, self.nameCat)
#         else: 
#             self.slug = generate_unique_slug(Category, self.nameCat)
#         super(Category, self).save(*args, **kwargs)
    



class Post (models.Model):
    title = models.CharField('Tiêu Đề', max_length=200,
                            help_text='Nhập tiêu đề')
    summary = models.TextField(verbose_name='Tóm Tắt')
    slug = models.SlugField(unique=True,editable=False , blank = True)
    content = HTMLField('Nội Dung')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0 , editable = False)
    view_count = models.IntegerField(default=0 , editable = False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
   
    thumbnail = FileBrowseField("Image", max_length=500, directory="uploads/", extensions=[".jpg",".jpeg"], blank=True)
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default = True)
    class Meta:
        verbose_name_plural = "Tất Cả Bài Viết"
    def __str__(self):
       return self.title
    def save(self, *args, **kwargs):
        if self.slug:  
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Post, self.title)
        else: 
            self.slug = generate_unique_slug(Post, self.title)
        super(Post,self).save()
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)
    is_like = models.IntegerField(default=0,editable = False)
    is_dislike = models.IntegerField(default=0,editable = False)
    timestamp  = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', null=True, blank=True, related_name='rep',on_delete=models.CASCADE)
    body = models.TextField()
    
    class Meta:
        verbose_name = 'Bình Luận'
        verbose_name_plural = 'Comments'
        ordering = ['-id']

    def __str__(self):
        return self.body



 
    
    
    
  
