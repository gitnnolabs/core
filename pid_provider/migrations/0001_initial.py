# Generated by Django 4.1.7 on 2023-04-17 01:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("files_storage", "0001_initial"),
        (
            "article",
            "0003_rename_article_art_languag_5b1006_idx_article_art_languag_1293e9_idx_and_more",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PidProviderBadRequest",
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
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Creation date"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last update date"
                    ),
                ),
                (
                    "basename",
                    models.TextField(blank=True, null=True, verbose_name="Basename"),
                ),
                (
                    "finger_print",
                    models.CharField(blank=True, max_length=65, null=True),
                ),
                ("error_type", models.TextField(blank=True, null=True)),
                ("error_message", models.TextField(blank=True, null=True)),
                ("xml", models.FileField(upload_to="bad_request")),
            ],
        ),
        migrations.CreateModel(
            name="PidProviderXML",
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
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Creation date"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last update date"
                    ),
                ),
                (
                    "pkg_name",
                    models.TextField(
                        blank=True, null=True, verbose_name="Package name"
                    ),
                ),
                (
                    "v3",
                    models.CharField(
                        blank=True, max_length=23, null=True, verbose_name="v3"
                    ),
                ),
                (
                    "v2",
                    models.CharField(
                        blank=True, max_length=23, null=True, verbose_name="v2"
                    ),
                ),
                (
                    "aop_pid",
                    models.CharField(
                        blank=True, max_length=23, null=True, verbose_name="AOP PID"
                    ),
                ),
                (
                    "elocation_id",
                    models.TextField(
                        blank=True, null=True, verbose_name="elocation id"
                    ),
                ),
                (
                    "fpage",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="fpage"
                    ),
                ),
                (
                    "fpage_seq",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="fpage_seq"
                    ),
                ),
                (
                    "lpage",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="lpage"
                    ),
                ),
                (
                    "article_pub_year",
                    models.CharField(
                        blank=True,
                        max_length=4,
                        null=True,
                        verbose_name="Document Publication Year",
                    ),
                ),
                (
                    "main_toc_section",
                    models.TextField(
                        blank=True, null=True, verbose_name="main_toc_section"
                    ),
                ),
                (
                    "main_doi",
                    models.TextField(blank=True, null=True, verbose_name="DOI"),
                ),
                (
                    "z_article_titles_texts",
                    models.CharField(
                        blank=True,
                        max_length=64,
                        null=True,
                        verbose_name="article_titles_texts",
                    ),
                ),
                (
                    "z_surnames",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="surnames"
                    ),
                ),
                (
                    "z_collab",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="collab"
                    ),
                ),
                (
                    "z_links",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="links"
                    ),
                ),
                (
                    "z_partial_body",
                    models.CharField(
                        blank=True,
                        max_length=64,
                        null=True,
                        verbose_name="partial_body",
                    ),
                ),
                (
                    "synchronized",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SyncFailure",
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
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Creation date"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last update date"
                    ),
                ),
                (
                    "message",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Mensagem"
                    ),
                ),
                (
                    "exception_type",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Exception Type",
                    ),
                ),
                (
                    "exception_msg",
                    models.CharField(
                        blank=True,
                        max_length=555,
                        null=True,
                        verbose_name="Exception Msg",
                    ),
                ),
                ("traceback", models.JSONField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="XMLIssue",
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
                    "pub_year",
                    models.CharField(
                        blank=True, max_length=4, null=True, verbose_name="pub_year"
                    ),
                ),
                (
                    "volume",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="volume"
                    ),
                ),
                (
                    "number",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="number"
                    ),
                ),
                (
                    "suppl",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="suppl"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="XMLJournal",
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
                    "issn_electronic",
                    models.CharField(
                        blank=True, max_length=9, null=True, verbose_name="issn_epub"
                    ),
                ),
                (
                    "issn_print",
                    models.CharField(
                        blank=True, max_length=9, null=True, verbose_name="issn_ppub"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="XMLVersion",
            fields=[
                (
                    "miniofile_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="files_storage.miniofile",
                    ),
                ),
                (
                    "finger_print",
                    models.CharField(blank=True, max_length=65, null=True),
                ),
                (
                    "xml_doc_pid",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="pid_provider.pidproviderxml",
                    ),
                ),
            ],
            bases=("files_storage.miniofile",),
        ),
        migrations.CreateModel(
            name="XMLRelatedItem",
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
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Creation date"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last update date"
                    ),
                ),
                (
                    "main_doi",
                    models.TextField(blank=True, null=True, verbose_name="DOI"),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_creator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Creator",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_last_mod_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Updater",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="xmljournal",
            index=models.Index(
                fields=["issn_electronic"], name="pid_provide_issn_el_3663e3_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="xmljournal",
            index=models.Index(
                fields=["issn_print"], name="pid_provide_issn_pr_37880c_idx"
            ),
        ),
        migrations.AddField(
            model_name="xmlissue",
            name="journal",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="pid_provider.xmljournal",
            ),
        ),
        migrations.AddField(
            model_name="syncfailure",
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
            model_name="syncfailure",
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
            model_name="pidproviderxml",
            name="article",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="article.article",
            ),
        ),
        migrations.AddField(
            model_name="pidproviderxml",
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
            model_name="pidproviderxml",
            name="current_version",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="pid_provider.xmlversion",
            ),
        ),
        migrations.AddField(
            model_name="pidproviderxml",
            name="issue",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="pid_provider.xmlissue",
            ),
        ),
        migrations.AddField(
            model_name="pidproviderxml",
            name="journal",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="pid_provider.xmljournal",
            ),
        ),
        migrations.AddField(
            model_name="pidproviderxml",
            name="related_items",
            field=models.ManyToManyField(to="pid_provider.xmlrelateditem"),
        ),
        migrations.AddField(
            model_name="pidproviderxml",
            name="sync_failure",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="pid_provider.syncfailure",
            ),
        ),
        migrations.AddField(
            model_name="pidproviderxml",
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
            model_name="pidproviderbadrequest",
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
            model_name="pidproviderbadrequest",
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
        migrations.AddIndex(
            model_name="xmlversion",
            index=models.Index(
                fields=["finger_print"], name="pid_provide_finger__df9abb_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="xmlrelateditem",
            index=models.Index(
                fields=["main_doi"], name="pid_provide_main_do_8e0a2a_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="xmlissue",
            index=models.Index(
                fields=["journal"], name="pid_provide_journal_08103a_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="xmlissue",
            index=models.Index(fields=["volume"], name="pid_provide_volume_f39ee2_idx"),
        ),
        migrations.AddIndex(
            model_name="xmlissue",
            index=models.Index(fields=["number"], name="pid_provide_number_f36ebd_idx"),
        ),
        migrations.AddIndex(
            model_name="xmlissue",
            index=models.Index(fields=["suppl"], name="pid_provide_suppl_241841_idx"),
        ),
        migrations.AddIndex(
            model_name="xmlissue",
            index=models.Index(
                fields=["pub_year"], name="pid_provide_pub_yea_bcd879_idx"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="xmlissue",
            unique_together={("journal", "pub_year", "volume", "number", "suppl")},
        ),
        migrations.AddIndex(
            model_name="pidproviderxml",
            index=models.Index(
                fields=["pkg_name"], name="pid_provide_pkg_nam_009b25_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="pidproviderxml",
            index=models.Index(fields=["v3"], name="pid_provide_v3_e61beb_idx"),
        ),
        migrations.AddIndex(
            model_name="pidproviderxml",
            index=models.Index(
                fields=["journal"], name="pid_provide_journal_bef662_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="pidproviderxml",
            index=models.Index(fields=["issue"], name="pid_provide_issue_i_e27cba_idx"),
        ),
        migrations.AddIndex(
            model_name="pidproviderxml",
            index=models.Index(
                fields=["elocation_id"], name="pid_provide_elocati_088a9b_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="pidproviderxml",
            index=models.Index(fields=["fpage"], name="pid_provide_fpage_aa4aa3_idx"),
        ),
        migrations.AddIndex(
            model_name="pidproviderxml",
            index=models.Index(
                fields=["fpage_seq"], name="pid_provide_fpage_s_cd49cb_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="pidproviderxml",
            index=models.Index(fields=["lpage"], name="pid_provide_lpage_7a7852_idx"),
        ),
        migrations.AddIndex(
            model_name="pidproviderxml",
            index=models.Index(
                fields=["article_pub_year"], name="pid_provide_article_e25491_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="pidproviderxml",
            index=models.Index(
                fields=["main_doi"], name="pid_provide_main_do_7fb3c9_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="pidproviderxml",
            index=models.Index(
                fields=["z_article_titles_texts"], name="pid_provide_z_artic_a6a417_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="pidproviderxml",
            index=models.Index(
                fields=["z_surnames"], name="pid_provide_z_surna_2f3ee3_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="pidproviderxml",
            index=models.Index(
                fields=["z_collab"], name="pid_provide_z_colla_c14f41_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="pidproviderxml",
            index=models.Index(
                fields=["z_links"], name="pid_provide_z_links_ed20b4_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="pidproviderxml",
            index=models.Index(
                fields=["z_partial_body"], name="pid_provide_z_parti_6ab872_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="pidproviderxml",
            index=models.Index(
                fields=["synchronized"], name="pid_provide_synchro_598b7a_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="pidproviderbadrequest",
            index=models.Index(
                fields=["basename"], name="pid_provide_basenam_8cb8ac_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="pidproviderbadrequest",
            index=models.Index(
                fields=["finger_print"], name="pid_provide_finger__b3b19c_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="pidproviderbadrequest",
            index=models.Index(
                fields=["error_type"], name="pid_provide_error_t_b4eaa4_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="pidproviderbadrequest",
            index=models.Index(
                fields=["error_message"], name="pid_provide_error_m_ca5dbc_idx"
            ),
        ),
    ]