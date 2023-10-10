# Generated by Django 4.2.6 on 2023-10-10 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True, default='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('model_version', models.CharField(blank=True, default='', max_length=255)),
                ('model_prediction', models.DecimalField(blank=True, decimal_places=4, default=None, max_digits=5, null=True)),
            ],
        ),
    ]
