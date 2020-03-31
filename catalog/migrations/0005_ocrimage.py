# Generated by Django 3.0.4 on 2020-03-30 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20200328_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='OCRImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=1000)),
                ('photo', models.ImageField(upload_to='images')),
            ],
        ),
    ]
