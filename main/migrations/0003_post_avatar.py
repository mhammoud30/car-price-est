# Generated by Django 4.0.4 on 2022-06-05 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_user_buyer_user_name_user_phonenum_user_seller_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='avatar',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]