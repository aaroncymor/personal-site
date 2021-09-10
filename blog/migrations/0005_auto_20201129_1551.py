# Generated by Django 3.1.3 on 2020-11-29 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20201129_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='decipher',
            name='clue_photo',
        ),
        migrations.AddField(
            model_name='decipher',
            name='clue_photo_filename',
            field=models.CharField(default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='decipher',
            name='clue_photo_fullpath',
            field=models.CharField(default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='decipher',
            name='clue_photo_url',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]