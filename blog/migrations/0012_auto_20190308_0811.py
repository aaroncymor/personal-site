# Generated by Django 2.0.10 on 2019-03-08 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20190306_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decipher',
            name='code',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
