# Generated by Django 4.2 on 2024-05-04 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('species', models.CharField(max_length=100)),
                ('breed', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('description', models.TextField()),
                ('photo', models.ImageField(upload_to='animals')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'Available'), (1, 'Adopted'), (2, 'Fostered'), (3, 'On hold')], default=0)),
            ],
        ),
    ]
