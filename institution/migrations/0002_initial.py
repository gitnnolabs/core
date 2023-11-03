# Generated by Django 4.1.10 on 2023-10-17 19:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("location", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("institution", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="scimago",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="location.country",
            ),
        ),
        migrations.AddField(
            model_name="scimago",
            name="creator",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_creator",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Creator",
            ),
        ),
        migrations.AddField(
            model_name="scimago",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_last_mod_user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Updater",
            ),
        ),
        migrations.AddField(
            model_name="publisherhistoryitem",
            name="creator",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_creator",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Creator",
            ),
        ),
        migrations.AddField(
            model_name="publisherhistoryitem",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_last_mod_user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Updater",
            ),
        ),
        migrations.AddField(
            model_name="ownerhistoryitem",
            name="creator",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_creator",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Creator",
            ),
        ),
        migrations.AddField(
            model_name="ownerhistoryitem",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_last_mod_user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Updater",
            ),
        ),
        migrations.AddField(
            model_name="institutionhistory",
            name="institution",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="institution.institution",
            ),
        ),
        migrations.AddField(
            model_name="institution",
            name="creator",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_creator",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Creator",
            ),
        ),
        migrations.AddField(
            model_name="institution",
            name="location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="location.location",
            ),
        ),
        migrations.AddField(
            model_name="institution",
            name="official",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="institution.institution",
                verbose_name="Institution",
            ),
        ),
        migrations.AddField(
            model_name="institution",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_last_mod_user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Updater",
            ),
        ),
        migrations.AddField(
            model_name="editorialmanagerhistoryitem",
            name="creator",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_creator",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Creator",
            ),
        ),
        migrations.AddField(
            model_name="editorialmanagerhistoryitem",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_last_mod_user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Updater",
            ),
        ),
        migrations.AddField(
            model_name="copyrightholderhistoryitem",
            name="creator",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_creator",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Creator",
            ),
        ),
        migrations.AddField(
            model_name="copyrightholderhistoryitem",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_last_mod_user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Updater",
            ),
        ),
        migrations.AddField(
            model_name="sponsorhistoryitem",
            name="institution",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="institution.sponsor",
            ),
        ),
        migrations.AddIndex(
            model_name="scimago",
            index=models.Index(
                fields=["institution"], name="institution_institu_0444aa_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="scimago",
            index=models.Index(fields=["url"], name="institution_url_eca05b_idx"),
        ),
        migrations.AddField(
            model_name="publisherhistoryitem",
            name="institution",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="institution.publisher",
            ),
        ),
        migrations.AddField(
            model_name="ownerhistoryitem",
            name="institution",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="institution.owner",
            ),
        ),
        migrations.AddIndex(
            model_name="institution",
            index=models.Index(fields=["name"], name="institution_name_955317_idx"),
        ),
        migrations.AddIndex(
            model_name="institution",
            index=models.Index(
                fields=["institution_type"], name="institution_institu_598c48_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="institution",
            index=models.Index(
                fields=["acronym"], name="institution_acronym_bacdf0_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="institution",
            index=models.Index(fields=["url"], name="institution_url_8f7c3c_idx"),
        ),
        migrations.AddField(
            model_name="editorialmanagerhistoryitem",
            name="institution",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="institution.editorialmanager",
            ),
        ),
        migrations.AddField(
            model_name="copyrightholderhistoryitem",
            name="institution",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="institution.copyrightholder",
            ),
        ),
    ]