# Generated by Django 4.2.4 on 2023-08-11 20:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customer",
            options={"ordering": ["user__first_name", "user__last_name"]},
        ),
        migrations.RemoveIndex(
            model_name="customer",
            name="store_custo_first_n_8f83e0_idx",
        ),
        migrations.RemoveField(
            model_name="customer",
            name="email",
        ),
        migrations.RemoveField(
            model_name="customer",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="customer",
            name="last_name",
        ),
        migrations.AddField(
            model_name="customer",
            name="user",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
