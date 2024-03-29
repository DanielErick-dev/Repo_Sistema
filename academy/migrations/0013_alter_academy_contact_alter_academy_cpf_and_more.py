# Generated by Django 5.0 on 2024-03-04 18:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("academy", "0012_alter_academy_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="academy",
            name="contact",
            field=models.CharField(
                max_length=11,
                validators=[django.core.validators.MinLengthValidator(11)],
                verbose_name="contato",
            ),
        ),
        migrations.AlterField(
            model_name="academy",
            name="cpf",
            field=models.CharField(
                max_length=11,
                validators=[django.core.validators.MinLengthValidator(11)],
                verbose_name="cpf",
            ),
        ),
        migrations.AlterField(
            model_name="academy",
            name="lastname",
            field=models.CharField(
                max_length=100,
                validators=[django.core.validators.MinLengthValidator(3)],
                verbose_name="sobrenome",
            ),
        ),
    ]
