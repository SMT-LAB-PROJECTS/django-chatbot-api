# Generated by Django 5.0.4 on 2024-05-02 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('answers', '0001_initial'),
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='options',
            field=models.ManyToManyField(blank=True, related_name='options', to='questions.qustion'),
        ),
    ]