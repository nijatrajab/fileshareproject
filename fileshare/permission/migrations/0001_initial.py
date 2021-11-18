# Generated by Django 3.2.7 on 2021-09-08 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BigUserObjectPermission',
            fields=[
                ('object_pk', models.CharField(max_length=255, verbose_name='object ID')),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.permission')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='biguserobjectpermission',
            index=models.Index(fields=['content_type', 'object_pk'], name='permission__content_87bb89_idx'),
        ),
        migrations.AddIndex(
            model_name='biguserobjectpermission',
            index=models.Index(fields=['content_type', 'object_pk', 'user'], name='permission__content_d394b4_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='biguserobjectpermission',
            unique_together={('user', 'permission', 'object_pk')},
        ),
    ]