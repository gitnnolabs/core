# Generated by Django 4.2.6 on 2023-11-03 15:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("xmlsps", "0002_alter_xmljournal_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="xmljournal",
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name="xmlsps",
            name="creator",
        ),
        migrations.RemoveField(
            model_name="xmlsps",
            name="updated_by",
        ),
        migrations.RemoveField(
            model_name="xmlsps",
            name="xml_issue",
        ),
        migrations.RemoveField(
            model_name="xmlsps",
            name="xml_journal",
        ),
        migrations.RemoveField(
            model_name="xmlsps",
            name="xml_version",
        ),
        migrations.DeleteModel(
            name="XMLIssue",
        ),
        migrations.DeleteModel(
            name="XMLJournal",
        ),
        migrations.DeleteModel(
            name="XMLSPS",
        ),
    ]