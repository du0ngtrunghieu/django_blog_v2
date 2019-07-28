# Generated by Django 2.2.2 on 2019-07-28 13:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filebrowser.fields
import mptt.fields
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(upload_to='uploads/', verbose_name='Avatar')),
                ('body', models.CharField(max_length=500, verbose_name='Thông Tin Thêm')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameCat', models.CharField(max_length=50, unique=True, verbose_name='Tên Thể Loai')),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Ngày Tạo')),
                ('featured', models.BooleanField(default=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('mptt_level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='posts.Category', verbose_name='Thể Loại Cha')),
            ],
            options={
                'verbose_name_plural': 'Thể Loại',
                'unique_together': {('slug', 'parent')},
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Nhập tiêu đề', max_length=200, verbose_name='Tiêu Đề')),
                ('summary', models.TextField(verbose_name='Tóm Tắt')),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
                ('content', tinymce.models.HTMLField(verbose_name='Nội Dung')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('comment_count', models.IntegerField(default=0, editable=False)),
                ('view_count', models.IntegerField(default=0, editable=False)),
                ('thumbnail', filebrowser.fields.FileBrowseField(blank=True, max_length=500, verbose_name='Image')),
                ('featured', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Author')),
                ('categories', models.ManyToManyField(to='posts.Category')),
            ],
            options={
                'verbose_name_plural': 'Tất Cả Bài Viết',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.IntegerField(default=0, editable=False)),
                ('is_dislike', models.IntegerField(default=0, editable=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='posts.Post')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rep', to='posts.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Bình Luận',
                'verbose_name_plural': 'Comments',
                'ordering': ['-id'],
            },
        ),
    ]
