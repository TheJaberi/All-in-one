# Generated by Django 5.1 on 2024-08-16 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
