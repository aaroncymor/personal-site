# Generated by Django 3.1.3 on 2020-11-20 07:06

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('content', tinymce.models.HTMLField()),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='blog.category')),
            ],
            options={
                'db_table': 'post',
            },
        ),
        migrations.CreateModel(
            name='Decipher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('hidden_text', models.CharField(max_length=255)),
                ('name', models.CharField(default='', max_length=100, null=True)),
                ('clue_photo', models.ImageField(null=True, upload_to='')),
                ('clue', models.TextField()),
                ('code', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deciphers', to='blog.post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('tag', models.CharField(max_length=100)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='blog.post')),
            ],
            options={
                'db_table': 'tag',
                'unique_together': {('tag', 'post')},
            },
        ),
    ]
