# Generated by Django 2.2.5 on 2019-11-15 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20191114_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentfile',
            name='file_type',
            field=models.CharField(blank=True, help_text='添付したファイルタイプ', max_length=10, null=True, verbose_name='ファイルタイプ'),
        ),
        migrations.AddField(
            model_name='post',
            name='evidence',
            field=models.TextField(blank=True, default='', help_text='（チェックリストのエビデンス登録）', verbose_name='エビデンス'),
        ),
    ]
