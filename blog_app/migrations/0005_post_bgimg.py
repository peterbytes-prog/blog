# Generated by Django 3.0.14 on 2021-09-05 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0004_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='bgimg',
            field=models.ImageField(blank=True, upload_to='assets/%Y/%m/%d'),
        ),
    ]