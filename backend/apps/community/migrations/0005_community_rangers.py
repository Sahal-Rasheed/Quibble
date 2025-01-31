# Generated by Django 5.1.5 on 2025-01-31 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_alter_community_avatar_alter_community_banner_and_more'),
        ('user', '0003_profile_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='rangers',
            field=models.ManyToManyField(
                blank=True,
                related_name='ranged_communities',
                to='user.profile',
                verbose_name='Rangers',
            ),
        ),
    ]
