# Generated by Django 4.2.2 on 2023-07-25 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_registry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('First_name', models.CharField(max_length=200)),
                ('Last_name', models.CharField(max_length=200)),
                ('Email', models.CharField(max_length=200, unique=True)),
                ('Password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'User_registry',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='user_registrt',
        ),
    ]
