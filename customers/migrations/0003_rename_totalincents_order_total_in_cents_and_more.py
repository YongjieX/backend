# Generated by Django 4.2.6 on 2023-11-22 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0002_order"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="totalInCents",
            new_name="total_in_cents",
        ),
        migrations.AlterField(
            model_name="order",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="customers.customer",
            ),
        ),
    ]
