# Generated by Django 2.0.2 on 2018-04-04 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sanskritannotator', '0005_auto_20180404_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordsinsentence',
            name='chunkno',
            field=models.IntegerField(default=0),
        ),
    ]
