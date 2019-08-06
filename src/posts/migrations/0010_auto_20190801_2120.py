# Generated by Django 2.2.2 on 2019-08-01 14:20

from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20190801_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='body',
            field=models.CharField(max_length=5000, verbose_name='Thông Tin Thêm'),
        ),
        migrations.AlterField(
            model_name='author',
            name='profile_pic',
            field=filebrowser.fields.FileBrowseField(blank=True, max_length=5000, verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='button_post',
            name='button',
            field=models.CharField(choices=[('DW', 'Downloads'), ('LK', 'Links')], max_length=2000, verbose_name='Button'),
        ),
        migrations.AlterField(
            model_name='button_post',
            name='content',
            field=models.CharField(max_length=2000, verbose_name='Nội Dung'),
        ),
        migrations.AlterField(
            model_name='button_post',
            name='link',
            field=models.CharField(max_length=2000, verbose_name='Đường Dẫn'),
        ),
        migrations.AlterField(
            model_name='category',
            name='nameCat',
            field=models.CharField(max_length=5000, unique=True, verbose_name='Tên Thể Loai'),
        ),
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=filebrowser.fields.FileBrowseField(blank=True, max_length=5000, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(help_text='Nhập tiêu đề', max_length=2000, verbose_name='Tiêu Đề'),
        ),
    ]