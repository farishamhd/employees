# Generated by Django 4.2.6 on 2023-11-07 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
