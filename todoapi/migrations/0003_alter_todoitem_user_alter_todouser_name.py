# Generated by Django 5.0 on 2023-12-16 19:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapi', '0002_alter_todoitem_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='todos', to='todoapi.todouser'),
        ),
        migrations.AlterField(
            model_name='todouser',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
