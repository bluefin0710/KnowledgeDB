# Generated by Django 2.2.5 on 2019-11-11 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='url_link',
            field=models.URLField(blank=True, help_text='※任意', null=True, verbose_name='URLリンク'),
        ),
    ]