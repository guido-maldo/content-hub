# Generated by Django 5.0.1 on 2024-04-13 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_youtube_reddit'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='guid',
            field=models.CharField(default='N/A', max_length=50),
        ),
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.URLField(default='hyperlink_icon', null=True),
        ),
        migrations.AddField(
            model_name='news',
            name='link',
            field=models.URLField(default='N/A'),
        ),
        migrations.AddField(
            model_name='news',
            name='pub_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='news',
            name='source',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AddField(
            model_name='news',
            name='source_homepage',
            field=models.URLField(default='N/A'),
        ),
        migrations.AddField(
            model_name='news',
            name='title',
            field=models.CharField(default='N/A', max_length=200),
        ),
    ]
