# Generated by Django 2.0.10 on 2019-01-28 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together={('name', 'post')},
        ),
    ]