# Generated by Django 2.2.5 on 2019-11-11 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_file_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='file_link',
            field=models.FilePathField(blank=True, help_text='※任意', max_length=512, null=True, path=None, verbose_name='ファイルサーバーPATH'),
        ),
    ]