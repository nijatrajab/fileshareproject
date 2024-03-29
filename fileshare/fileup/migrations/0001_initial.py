# Generated by Django 3.2.7 on 2021-09-08 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import fileup.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('browse_file', models.FileField(upload_to=fileup.models.user_directory_path)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('uploaded_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userfile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_userfile', 'Can view userfile'),),
                'get_latest_by': 'uploaded_at',
                'default_permissions': ('add', 'change', 'delete'),
            },
        ),
    ]
