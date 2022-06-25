# Generated by Django 4.0 on 2022-06-18 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_remove_follow_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='follows',
            field=models.ManyToManyField(null=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follow',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='network.user'),
        ),
    ]
