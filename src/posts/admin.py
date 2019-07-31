from django.contrib import admin
from .models import Author,Category ,Post,Comment,Button_Post
from filebrowser.settings import ADMIN_THUMBNAIL
from filebrowser.base import FileObject
from django.utils.html import mark_safe
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin
from mptt.admin import TreeRelatedFieldListFilter
from django.utils.html import format_html
class CommentAdmin(admin.StackedInline):
    model = Comment
    extra = 0
    readonly_fields = ('body', 'post','reply','user')
class ButtonAdmin(admin.StackedInline):
    model = Button_Post
    extra = 0
       
class PageAdminPost(admin.ModelAdmin):
    
    def categories_display(self, obj):
        return " | ".join([
            f.nameCat for f in obj.categories.all()
        ])
    categories_display.short_description = "Thể Loại"
    def image_thumbnail(self, obj):
        if obj.thumbnail and obj.thumbnail.filetype == "Image":
            return mark_safe('<img src="%s" />' % obj.thumbnail.version_generate(ADMIN_THUMBNAIL).url)
        else:
            return ""
    image_thumbnail.allow_tags = True
    image_thumbnail.short_description = "Thumbnail"
    list_display= ('title','slug','author','comment_count','categories_display' ,'timestamp','image_thumbnail')
    # image_display = AdminThumbnail(image_field=cached_admin_thumb)
    # image_display.short_description = 'Avatar'
    inlines = (ButtonAdmin,CommentAdmin,)
    search_fields =['title' , 'author']
    list_filter = ['timestamp','author',]
    list_per_page =5
    
    
    
    

class PageAdminCategory(DraggableMPTTAdmin):
    list_display = ('tree_actions','indented_title')
    list_filter =(
        ('parent', TreeRelatedFieldListFilter),
                 )
    list_display_links=(
        'indented_title',
                        )


    
    mptt_level_indent = 20
class PageAdminAuthor(admin.ModelAdmin):
    pass
    

    
   
admin.site.register(Post, PageAdminPost)
admin.site.register(Category,PageAdminCategory)    
admin.site.register(Author,PageAdminAuthor)    
