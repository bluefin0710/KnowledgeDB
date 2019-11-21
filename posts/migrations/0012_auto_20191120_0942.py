# Generated by Django 2.2.5 on 2019-11-20 00:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20191115_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentfile',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Post'),
        ),
        migrations.AlterField(
            model_name='contentimage',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Post'),
        ),
    ]