# Generated by Django 2.0.2 on 2018-04-08 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sanskritannotator', '0006_wordsinsentence_chunkno'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordoptions',
            name='children',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='wordoptions',
            name='parent',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='wordoptions',
            name='relation',
            field=models.CharField(default='', max_length=100),
        ),
    ]