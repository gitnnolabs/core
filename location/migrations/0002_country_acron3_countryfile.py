# Generated by Django 4.1.10 on 2023-09-04 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wagtaildocs", "0012_uploadeddocument"),
        ("location", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="country",
            name="acron3",
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
                verbose_name="Acronym to the Country (3 char)",
            ),
        ),
        migrations.CreateModel(
            name="CountryFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_valid",
                    models.BooleanField(
                        blank=True, default=False, null=True, verbose_name="Is valid?"
                    ),
                ),
                (
                    "line_count",
                    models.IntegerField(
                        blank=True, default=0, null=True, verbose_name="Number of lines"
                    ),
                ),
                (
                    "attachment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtaildocs.document",
                    ),
                ),
            ],
        ),
    ]
