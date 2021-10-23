# Generated by Django 3.0.14 on 2021-10-22 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0007_auto_20210905_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogimage',
            name='blog',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='blog_app.Post'),
            preserve_default=False,
        ),
    ]