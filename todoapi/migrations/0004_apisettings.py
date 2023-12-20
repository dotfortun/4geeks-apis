# Generated by Django 5.0 on 2023-12-19 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapi', '0003_alter_todoitem_user_alter_todouser_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=128, unique=True)),
                ('value', models.JSONField()),
            ],
        ),
    ]
