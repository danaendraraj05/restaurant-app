# Generated by Django 5.0.6 on 2024-07-02 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_remove_restaurant_reviews_remove_restaurant_timings_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='static/restaurant_photos/'),
        ),
    ]
