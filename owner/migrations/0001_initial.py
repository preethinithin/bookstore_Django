# Generated by Django 4.0.5 on 2022-06-11 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=120, unique=True)),
                ('author', models.CharField(max_length=120)),
                ('amount', models.PositiveIntegerField()),
                ('copies', models.PositiveIntegerField()),
                ('image', models.ImageField(null=True, upload_to='images')),
            ],
        ),
    ]
