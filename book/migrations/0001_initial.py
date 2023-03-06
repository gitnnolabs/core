# Generated by Django 4.1.6 on 2023-02-21 22:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("institution", "0002_alter_institution_creator_and_more"),
        ("location", "0002_alter_city_creator_alter_city_updated_by_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
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
                    "isbn",
                    models.CharField(
                        blank=True, max_length=13, null=True, verbose_name="ISBN"
                    ),
                ),
                (
                    "eisbn",
                    models.CharField(
                        blank=True,
                        max_length=13,
                        null=True,
                        verbose_name="Electronic ISBN",
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("aa", "Afar"),
                            ("af", "Afrikaans"),
                            ("ak", "Akan"),
                            ("sq", "Albanian"),
                            ("am", "Amharic"),
                            ("ar", "Arabic"),
                            ("an", "Aragonese"),
                            ("hy", "Armenian"),
                            ("as", "Assamese"),
                            ("av", "Avaric"),
                            ("ae", "Avestan"),
                            ("ay", "Aymara"),
                            ("az", "Azerbaijani"),
                            ("bm", "Bambara"),
                            ("ba", "Bashkir"),
                            ("eu", "Basque"),
                            ("be", "Belarusian"),
                            ("bn", "Bengali"),
                            ("bi", "Bislama"),
                            ("bs", "Bosnian"),
                            ("br", "Breton"),
                            ("bg", "Bulgarian"),
                            ("my", "Burmese"),
                            ("ca", "Catalan, Valencian"),
                            ("ch", "Chamorro"),
                            ("ce", "Chechen"),
                            ("ny", "Chichewa, Chewa, Nyanja"),
                            ("zh", "Chinese"),
                            (
                                "cu",
                                "Church Slavic, Old Slavonic, Church Slavonic, Old Bulgarian, Old Church Slavonic",
                            ),
                            ("cv", "Chuvash"),
                            ("kw", "Cornish"),
                            ("co", "Corsican"),
                            ("cr", "Cree"),
                            ("hr", "Croatian"),
                            ("cs", "Czech"),
                            ("da", "Danish"),
                            ("dv", "Divehi, Dhivehi, Maldivian"),
                            ("nl", "Dutch, Flemish"),
                            ("dz", "Dzongkha"),
                            ("en", "English"),
                            ("eo", "Esperanto"),
                            ("et", "Estonian"),
                            ("ee", "Ewe"),
                            ("fo", "Faroese"),
                            ("fj", "Fijian"),
                            ("fi", "Finnish"),
                            ("fr", "French"),
                            ("fy", "Western Frisian"),
                            ("ff", "Fulah"),
                            ("gd", "Gaelic, Scottish Gaelic"),
                            ("gl", "Galician"),
                            ("lg", "Ganda"),
                            ("ka", "Georgian"),
                            ("de", "German"),
                            ("el", "Greek, Modern (1453–)"),
                            ("kl", "Kalaallisut, Greenlandic"),
                            ("gn", "Guarani"),
                            ("gu", "Gujarati"),
                            ("ht", "Haitian, Haitian Creole"),
                            ("ha", "Hausa"),
                            ("he", "Hebrew"),
                            ("hz", "Herero"),
                            ("hi", "Hindi"),
                            ("ho", "Hiri Motu"),
                            ("hu", "Hungarian"),
                            ("is", "Icelandic"),
                            ("io", "Ido"),
                            ("ig", "Igbo"),
                            ("id", "Indonesian"),
                            (
                                "ia",
                                "Interlingua (International Auxiliary Language Association)",
                            ),
                            ("ie", "Interlingue, Occidental"),
                            ("iu", "Inuktitut"),
                            ("ik", "Inupiaq"),
                            ("ga", "Irish"),
                            ("it", "Italian"),
                            ("ja", "Japanese"),
                            ("jv", "Javanese"),
                            ("kn", "Kannada"),
                            ("kr", "Kanuri"),
                            ("ks", "Kashmiri"),
                            ("kk", "Kazakh"),
                            ("km", "Central Khmer"),
                            ("ki", "Kikuyu, Gikuyu"),
                            ("rw", "Kinyarwanda"),
                            ("ky", "Kirghiz, Kyrgyz"),
                            ("kv", "Komi"),
                            ("kg", "Kongo"),
                            ("ko", "Korean"),
                            ("kj", "Kuanyama, Kwanyama"),
                            ("ku", "Kurdish"),
                            ("lo", "Lao"),
                            ("la", "Latin"),
                            ("lv", "Latvian"),
                            ("li", "Limburgan, Limburger, Limburgish"),
                            ("ln", "Lingala"),
                            ("lt", "Lithuanian"),
                            ("lu", "Luba-Katanga"),
                            ("lb", "Luxembourgish, Letzeburgesch"),
                            ("mk", "Macedonian"),
                            ("mg", "Malagasy"),
                            ("ms", "Malay"),
                            ("ml", "Malayalam"),
                            ("mt", "Maltese"),
                            ("gv", "Manx"),
                            ("mi", "Maori"),
                            ("mr", "Marathi"),
                            ("mh", "Marshallese"),
                            ("mn", "Mongolian"),
                            ("na", "Nauru"),
                            ("nv", "Navajo, Navaho"),
                            ("nd", "North Ndebele"),
                            ("nr", "South Ndebele"),
                            ("ng", "Ndonga"),
                            ("ne", "Nepali"),
                            ("no", "Norwegian"),
                            ("nb", "Norwegian Bokmål"),
                            ("nn", "Norwegian Nynorsk"),
                            ("ii", "Sichuan Yi, Nuosu"),
                            ("oc", "Occitan"),
                            ("oj", "Ojibwa"),
                            ("or", "Oriya"),
                            ("om", "Oromo"),
                            ("os", "Ossetian, Ossetic"),
                            ("pi", "Pali"),
                            ("ps", "Pashto, Pushto"),
                            ("fa", "Persian"),
                            ("pl", "Polish"),
                            ("pt", "Portuguese"),
                            ("pa", "Punjabi, Panjabi"),
                            ("qu", "Quechua"),
                            ("ro", "Romanian, Moldavian, Moldovan"),
                            ("rm", "Romansh"),
                            ("rn", "Rundi"),
                            ("ru", "Russian"),
                            ("se", "Northern Sami"),
                            ("sm", "Samoan"),
                            ("sg", "Sango"),
                            ("sa", "Sanskrit"),
                            ("sc", "Sardinian"),
                            ("sr", "Serbian"),
                            ("sn", "Shona"),
                            ("sd", "Sindhi"),
                            ("si", "Sinhala, Sinhalese"),
                            ("sk", "Slovak"),
                            ("sl", "Slovenian"),
                            ("so", "Somali"),
                            ("st", "Southern Sotho"),
                            ("es", "Spanish, Castilian"),
                            ("su", "Sundanese"),
                            ("sw", "Swahili"),
                            ("ss", "Swati"),
                            ("sv", "Swedish"),
                            ("tl", "Tagalog"),
                            ("ty", "Tahitian"),
                            ("tg", "Tajik"),
                            ("ta", "Tamil"),
                            ("tt", "Tatar"),
                            ("te", "Telugu"),
                            ("th", "Thai"),
                            ("bo", "Tibetan"),
                            ("ti", "Tigrinya"),
                            ("to", "Tonga (Tonga Islands)"),
                            ("ts", "Tsonga"),
                            ("tn", "Tswana"),
                            ("tr", "Turkish"),
                            ("tk", "Turkmen"),
                            ("tw", "Twi"),
                            ("ug", "Uighur, Uyghur"),
                            ("uk", "Ukrainian"),
                            ("ur", "Urdu"),
                            ("uz", "Uzbek"),
                            ("ve", "Venda"),
                            ("vi", "Vietnamese"),
                            ("vo", "Volapük"),
                            ("wa", "Walloon"),
                            ("cy", "Welsh"),
                            ("wo", "Wolof"),
                            ("xh", "Xhosa"),
                            ("yi", "Yiddish"),
                            ("yo", "Yoruba"),
                            ("za", "Zhuang, Chuang"),
                            ("zu", "Zulu"),
                        ],
                        max_length=256,
                        null=True,
                        verbose_name="Idioma",
                    ),
                ),
                (
                    "synopsis",
                    models.TextField(blank=True, null=True, verbose_name="Synopsis"),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=256, null=True, verbose_name="Título"
                    ),
                ),
                (
                    "year",
                    models.IntegerField(blank=True, null=True, verbose_name="Year"),
                ),
                (
                    "doi",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="DOI"
                    ),
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
                    "institution",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="institution.institution",
                        verbose_name="Publisher",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="location.location",
                        verbose_name="Localization",
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
            options={
                "verbose_name": "SciELO Book",
                "verbose_name_plural": "SciELO Books",
            },
        ),
        migrations.AddIndex(
            model_name="book",
            index=models.Index(fields=["isbn"], name="book_book_isbn_6f139e_idx"),
        ),
        migrations.AddIndex(
            model_name="book",
            index=models.Index(fields=["title"], name="book_book_title_b5b75a_idx"),
        ),
        migrations.AddIndex(
            model_name="book",
            index=models.Index(
                fields=["synopsis"], name="book_book_synopsi_3faa60_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="book",
            index=models.Index(fields=["doi"], name="book_book_doi_3c6aea_idx"),
        ),
    ]