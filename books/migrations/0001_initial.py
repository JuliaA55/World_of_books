# Generated by Django 5.1.4 on 2025-01-07 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=100)),
                ('publication_year', models.IntegerField()),
                ('genre', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
                ('isNew', models.BooleanField(default=False)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
    ]
