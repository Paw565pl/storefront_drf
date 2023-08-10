# Generated by Django 4.2.4 on 2023-08-09 17:23

from pathlib import Path
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            Path("sql/seed_store.sql").read_text(),
            Path("sql/reverse_seed_store.sql").read_text(),
        )
    ]