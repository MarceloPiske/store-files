# Generated by Django 4.0.3 on 2022-03-19 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leitor_arquivos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='diretorioss3',
            name='diretório',
            field=models.CharField(default='media/', max_length=150),
        ),
    ]
