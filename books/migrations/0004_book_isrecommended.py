# Generated by Django 5.1.4 on 2025-01-10 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_book_isnew'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='isRecommended',
            field=models.BooleanField(default=False),
        ),
    ]
