# Generated by Django 3.1.7 on 2021-04-02 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='dimension',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.dimension'),
        ),
    ]