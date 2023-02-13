# Generated by Django 3.2.12 on 2023-02-01 10:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Last update date')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Vocabulary name')),
                ('acronym', models.CharField(blank=True, max_length=10, null=True, verbose_name='Vocabulary acronym')),
                ('creator', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vocabulary_creator', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vocabulary_last_mod_user', to=settings.AUTH_USER_MODEL, verbose_name='Updater')),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Last update date')),
                ('text', models.CharField(blank=True, max_length=255, null=True, verbose_name='Texto')),
                ('language', models.CharField(blank=True, choices=[('aa', 'Afar'), ('af', 'Afrikaans'), ('ak', 'Akan'), ('sq', 'Albanian'), ('am', 'Amharic'), ('ar', 'Arabic'), ('an', 'Aragonese'), ('hy', 'Armenian'), ('as', 'Assamese'), ('av', 'Avaric'), ('ae', 'Avestan'), ('ay', 'Aymara'), ('az', 'Azerbaijani'), ('bm', 'Bambara'), ('ba', 'Bashkir'), ('eu', 'Basque'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('bi', 'Bislama'), ('bs', 'Bosnian'), ('br', 'Breton'), ('bg', 'Bulgarian'), ('my', 'Burmese'), ('ca', 'Catalan, Valencian'), ('ch', 'Chamorro'), ('ce', 'Chechen'), ('ny', 'Chichewa, Chewa, Nyanja'), ('zh', 'Chinese'), ('cu', 'Church Slavic, Old Slavonic, Church Slavonic, Old Bulgarian, Old Church Slavonic'), ('cv', 'Chuvash'), ('kw', 'Cornish'), ('co', 'Corsican'), ('cr', 'Cree'), ('hr', 'Croatian'), ('cs', 'Czech'), ('da', 'Danish'), ('dv', 'Divehi, Dhivehi, Maldivian'), ('nl', 'Dutch, Flemish'), ('dz', 'Dzongkha'), ('en', 'English'), ('eo', 'Esperanto'), ('et', 'Estonian'), ('ee', 'Ewe'), ('fo', 'Faroese'), ('fj', 'Fijian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Western Frisian'), ('ff', 'Fulah'), ('gd', 'Gaelic, Scottish Gaelic'), ('gl', 'Galician'), ('lg', 'Ganda'), ('ka', 'Georgian'), ('de', 'German'), ('el', 'Greek, Modern (1453–)'), ('kl', 'Kalaallisut, Greenlandic'), ('gn', 'Guarani'), ('gu', 'Gujarati'), ('ht', 'Haitian, Haitian Creole'), ('ha', 'Hausa'), ('he', 'Hebrew'), ('hz', 'Herero'), ('hi', 'Hindi'), ('ho', 'Hiri Motu'), ('hu', 'Hungarian'), ('is', 'Icelandic'), ('io', 'Ido'), ('ig', 'Igbo'), ('id', 'Indonesian'), ('ia', 'Interlingua (International Auxiliary Language Association)'), ('ie', 'Interlingue, Occidental'), ('iu', 'Inuktitut'), ('ik', 'Inupiaq'), ('ga', 'Irish'), ('it', 'Italian'), ('ja', 'Japanese'), ('jv', 'Javanese'), ('kn', 'Kannada'), ('kr', 'Kanuri'), ('ks', 'Kashmiri'), ('kk', 'Kazakh'), ('km', 'Central Khmer'), ('ki', 'Kikuyu, Gikuyu'), ('rw', 'Kinyarwanda'), ('ky', 'Kirghiz, Kyrgyz'), ('kv', 'Komi'), ('kg', 'Kongo'), ('ko', 'Korean'), ('kj', 'Kuanyama, Kwanyama'), ('ku', 'Kurdish'), ('lo', 'Lao'), ('la', 'Latin'), ('lv', 'Latvian'), ('li', 'Limburgan, Limburger, Limburgish'), ('ln', 'Lingala'), ('lt', 'Lithuanian'), ('lu', 'Luba-Katanga'), ('lb', 'Luxembourgish, Letzeburgesch'), ('mk', 'Macedonian'), ('mg', 'Malagasy'), ('ms', 'Malay'), ('ml', 'Malayalam'), ('mt', 'Maltese'), ('gv', 'Manx'), ('mi', 'Maori'), ('mr', 'Marathi'), ('mh', 'Marshallese'), ('mn', 'Mongolian'), ('na', 'Nauru'), ('nv', 'Navajo, Navaho'), ('nd', 'North Ndebele'), ('nr', 'South Ndebele'), ('ng', 'Ndonga'), ('ne', 'Nepali'), ('no', 'Norwegian'), ('nb', 'Norwegian Bokmål'), ('nn', 'Norwegian Nynorsk'), ('ii', 'Sichuan Yi, Nuosu'), ('oc', 'Occitan'), ('oj', 'Ojibwa'), ('or', 'Oriya'), ('om', 'Oromo'), ('os', 'Ossetian, Ossetic'), ('pi', 'Pali'), ('ps', 'Pashto, Pushto'), ('fa', 'Persian'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pa', 'Punjabi, Panjabi'), ('qu', 'Quechua'), ('ro', 'Romanian, Moldavian, Moldovan'), ('rm', 'Romansh'), ('rn', 'Rundi'), ('ru', 'Russian'), ('se', 'Northern Sami'), ('sm', 'Samoan'), ('sg', 'Sango'), ('sa', 'Sanskrit'), ('sc', 'Sardinian'), ('sr', 'Serbian'), ('sn', 'Shona'), ('sd', 'Sindhi'), ('si', 'Sinhala, Sinhalese'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('so', 'Somali'), ('st', 'Southern Sotho'), ('es', 'Spanish, Castilian'), ('su', 'Sundanese'), ('sw', 'Swahili'), ('ss', 'Swati'), ('sv', 'Swedish'), ('tl', 'Tagalog'), ('ty', 'Tahitian'), ('tg', 'Tajik'), ('ta', 'Tamil'), ('tt', 'Tatar'), ('te', 'Telugu'), ('th', 'Thai'), ('bo', 'Tibetan'), ('ti', 'Tigrinya'), ('to', 'Tonga (Tonga Islands)'), ('ts', 'Tsonga'), ('tn', 'Tswana'), ('tr', 'Turkish'), ('tk', 'Turkmen'), ('tw', 'Twi'), ('ug', 'Uighur, Uyghur'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('uz', 'Uzbek'), ('ve', 'Venda'), ('vi', 'Vietnamese'), ('vo', 'Volapük'), ('wa', 'Walloon'), ('cy', 'Welsh'), ('wo', 'Wolof'), ('xh', 'Xhosa'), ('yi', 'Yiddish'), ('yo', 'Yoruba'), ('za', 'Zhuang, Chuang'), ('zu', 'Zulu')], max_length=2, null=True, verbose_name='Idioma')),
                ('creator', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='keyword_creator', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='keyword_last_mod_user', to=settings.AUTH_USER_MODEL, verbose_name='Updater')),
                ('vocabulary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vocabulary.vocabulary', verbose_name='Vocabulary')),
            ],
        ),
        migrations.AddIndex(
            model_name='vocabulary',
            index=models.Index(fields=['name'], name='vocabulary__name_c567ee_idx'),
        ),
        migrations.AddIndex(
            model_name='vocabulary',
            index=models.Index(fields=['acronym'], name='vocabulary__acronym_5db9d3_idx'),
        ),
        migrations.AddIndex(
            model_name='keyword',
            index=models.Index(fields=['text'], name='vocabulary__text_492e2a_idx'),
        ),
        migrations.AddIndex(
            model_name='keyword',
            index=models.Index(fields=['language'], name='vocabulary__languag_a11f3d_idx'),
        ),
        migrations.AddIndex(
            model_name='keyword',
            index=models.Index(fields=['vocabulary'], name='vocabulary__vocabul_ff8b36_idx'),
        ),
    ]