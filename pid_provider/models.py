import json
import logging
import sys
from datetime import datetime

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _
from packtools.sps.pid_provider import v3_gen, xml_sps_adapter
from wagtail.admin.panels import FieldPanel
from wagtailautocomplete.edit_handlers import AutocompletePanel

from collection.models import Collection
from core.forms import CoreAdminModelForm
from core.models import CommonControlField
from pid_provider import exceptions
from tracker.models import UnexpectedEvent
from xmlsps.models import XMLVersion

LOGGER = logging.getLogger(__name__)
LOGGER_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def utcnow():
    return datetime.utcnow()
    # return datetime.utcnow().isoformat().replace("T", " ") + "Z"


def xml_directory_path(instance, subdir):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"xml_pid_provider/{subdir}/{instance.pid_v3[0]}/{instance.pid_v3[-1]}/{instance.pid_v3}/{instance.finger_print}"


class PidProviderConfig(CommonControlField):
    """
    Tem função de guardar XML que falhou no registro
    """

    pid_provider_api_post_xml = models.TextField(
        _("XML Post URI"), null=True, blank=True
    )
    pid_provider_api_get_token = models.TextField(
        _("Get Token URI"), null=True, blank=True
    )
    timeout = models.IntegerField(_("Timeout"), null=True, blank=True)
    api_username = models.TextField(_("API Username"), null=True, blank=True)
    api_password = models.TextField(_("API Password"), null=True, blank=True)

    def __unicode__(self):
        return f"{self.pid_provider_api_post_xml}"

    def __str__(self):
        return f"{self.pid_provider_api_post_xml}"

    @classmethod
    def get_or_create(
        cls,
        creator=None,
        pid_provider_api_post_xml=None,
        pid_provider_api_get_token=None,
        api_username=None,
        api_password=None,
        timeout=None,
    ):
        obj = cls.objects.first()
        if obj is None:
            obj = cls()
            obj.pid_provider_api_post_xml = pid_provider_api_post_xml
            obj.pid_provider_api_get_token = pid_provider_api_get_token
            obj.api_username = api_username
            obj.api_password = api_password
            obj.timeout = timeout
            obj.creator = creator
            obj.save()
        return obj

    panels = [
        FieldPanel("pid_provider_api_post_xml"),
        FieldPanel("pid_provider_api_get_token"),
        FieldPanel("api_username"),
        FieldPanel("api_password"),
        FieldPanel("timeout"),
    ]

    base_form_class = CoreAdminModelForm


class PidRequest(CommonControlField):
    origin = models.CharField(
        _("Request origin"), max_length=124, null=True, blank=True
    )
    result_type = models.TextField(_("Result type"), null=True, blank=True)
    result_msg = models.TextField(_("Result message"), null=True, blank=True)
    xml_version = models.ForeignKey(
        XMLVersion, null=True, blank=True, on_delete=models.SET_NULL
    )
    detail = models.JSONField(_("Detail"), null=True, blank=True)
    origin_date = models.CharField(
        _("Origin date"), max_length=10, null=True, blank=True
    )
    v3 = models.CharField(_("PID v3"), max_length=23, null=True, blank=True)
    times = models.IntegerField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "result_type",
                ]
            ),
            models.Index(
                fields=[
                    "v3",
                ]
            ),
            models.Index(
                fields=[
                    "times",
                ]
            ),
            models.Index(
                fields=[
                    "detail",
                ]
            ),
        ]

    @property
    def data(self):
        _data = {
            "origin": self.origin,
            "v3": self.v3,
            "origin_date": self.origin_date,
            "result_type": self.result_type,
            "result_msg": self.result_msg,
            "detail": self.detail,
            "times": self.times,
        }
        return _data

    def __unicode__(self):
        return f"{self.origin}"

    def __str__(self):
        return f"{self.origin}"

    @classmethod
    def get(
        cls,
        origin=None,
    ):
        if origin:
            return cls.objects.get(origin=origin)
        raise ValueError("PidRequest.get requires parameters")

    @classmethod
    def create_or_update(
        cls,
        user=None,
        origin=None,
        result_type=None,
        result_msg=None,
        xml_version=None,
        detail=None,
        origin_date=None,
        v3=None,
    ):
        try:
            obj = cls.get(origin=origin)
            obj.updated_by = user
        except cls.DoesNotExist:
            obj = cls()
            obj.creator = user
            obj.origin = origin

        obj.v3 = v3 or obj.v3
        obj.result_type = result_type or obj.result_type
        obj.result_msg = result_msg or obj.result_msg
        obj.xml_version = xml_version or obj.xml_version
        obj.detail = detail or obj.detail
        obj.origin = origin or obj.origin
        obj.origin_date = origin_date or obj.origin_date
        if not obj.times:
            obj.times = 0
        obj.times += 1
        obj.save()
        return obj

    @classmethod
    def register_failure(
        cls,
        e,
        user=None,
        origin=None,
        message=None,
        detail=None,
        origin_date=None,
        v3=None,
    ):
        logging.exception(e)
        msg = str(e)
        if message:
            msg = f"{msg} {message}"
        return PidRequest.create_or_update(
            user=user,
            origin=origin,
            origin_date=origin_date,
            result_type=str(type(e)),
            result_msg=msg,
            detail=detail,
            v3=v3,
        )

    @classmethod
    def cancel_failure(
        cls, user=None, origin=None, v3=None, detail=None, origin_date=None
    ):
        try:
            PidRequest.get(origin)
        except cls.DoesNotExist:
            # nao é necessario atualizar o status de falha não registrada anteriormente
            pass
        else:
            return PidRequest.create_or_update(
                user=user,
                origin=origin,
                origin_date=origin_date,
                result_type="OK",
                result_msg="OK",
                detail=detail,
                v3=v3,
            )

    @property
    def created_updated(self):
        return self.updated or self.created

    @classmethod
    def items_to_retry(cls):
        # retorna os itens em que result_type é diferente de OK e a origem é URI
        return cls.objects.filter(~Q(result_type="OK"), origin__contains=":").iterator()

    panels = [
        # FieldPanel("origin", read_only=True),
        FieldPanel("origin_date", read_only=True),
        FieldPanel("result_type", read_only=True),
        FieldPanel("result_msg", read_only=True),
        # AutocompletePanel("xml_version", read_only=True),
        FieldPanel("detail", read_only=True),
    ]

    base_form_class = CoreAdminModelForm


class PidChange(CommonControlField):
    pkg_name = models.TextField(_("Package name"), null=True, blank=True)
    pid_type = models.CharField(_("PID type"), max_length=23, null=True, blank=True)
    pid_in_xml = models.CharField(
        _("PID pid_in_xml"), max_length=23, null=True, blank=True
    )
    pid_assigned = models.CharField(
        _("PID assigned"), max_length=23, null=True, blank=True
    )
    version = models.ForeignKey(
        XMLVersion, null=True, blank=True, on_delete=models.SET_NULL
    )

    panels = [
        # FieldPanel("pkg_name", read_only=True),
        FieldPanel("pid_type", read_only=True),
        FieldPanel("pid_in_xml", read_only=True),
        FieldPanel("pid_assigned", read_only=True),
        AutocompletePanel("version", read_only=True),
    ]

    class Meta:
        indexes = [
            models.Index(fields=["pid_in_xml"]),
            models.Index(fields=["pid_assigned"]),
            models.Index(fields=["pid_type"]),
            models.Index(fields=["version"]),
        ]

    def __str__(self):
        return f"{self.pid_type} {self.pid_in_xml} -> {self.pid_assigned}"

    @classmethod
    def get_or_create(cls, pid_type, pid_in_xml, pid_assigned, version, user, pkg_name):
        try:
            return cls.objects.get(
                pid_type=pid_type,
                pid_in_xml=pid_in_xml,
                pid_assigned=pid_assigned,
                version=version,
            )
        except cls.DoesNotExist:
            obj = cls()
            obj.creator = user
            obj.pkg_name = pkg_name
            obj.pid_type = pid_type
            obj.pid_in_xml = pid_in_xml
            obj.pid_assigned = pid_assigned
            obj.version = version
            obj.save()
            return obj

    @property
    def created_updated(self):
        return self.updated or self.created


class PidProviderXML(CommonControlField):
    """
    Tem responsabilidade de garantir a atribuição do PID da versão 3,
    armazenando dados chaves que garantem a identificação do XML
    """

    issn_electronic = models.CharField(
        _("issn_epub"), max_length=9, null=True, blank=True
    )
    issn_print = models.CharField(_("issn_ppub"), max_length=9, null=True, blank=True)
    pub_year = models.CharField(_("pub_year"), max_length=4, null=True, blank=True)
    volume = models.CharField(_("volume"), max_length=10, null=True, blank=True)
    number = models.CharField(_("number"), max_length=10, null=True, blank=True)
    suppl = models.CharField(_("suppl"), max_length=10, null=True, blank=True)

    current_version = models.ForeignKey(
        XMLVersion, on_delete=models.SET_NULL, null=True, blank=True
    )

    pkg_name = models.TextField(_("Package name"), null=True, blank=True)
    v3 = models.CharField(_("v3"), max_length=23, null=True, blank=True)
    v2 = models.CharField(_("v2"), max_length=23, null=True, blank=True)
    aop_pid = models.CharField(_("AOP PID"), max_length=23, null=True, blank=True)

    elocation_id = models.TextField(_("elocation id"), null=True, blank=True)
    fpage = models.CharField(_("fpage"), max_length=10, null=True, blank=True)
    fpage_seq = models.CharField(_("fpage_seq"), max_length=10, null=True, blank=True)
    lpage = models.CharField(_("lpage"), max_length=10, null=True, blank=True)
    article_pub_year = models.CharField(
        _("Document Publication Year"), max_length=4, null=True, blank=True
    )
    main_toc_section = models.TextField(_("main_toc_section"), null=True, blank=True)
    main_doi = models.TextField(_("DOI"), null=True, blank=True)

    z_article_titles_texts = models.CharField(
        _("article_titles_texts"), max_length=64, null=True, blank=True
    )
    z_surnames = models.CharField(_("surnames"), max_length=64, null=True, blank=True)
    z_collab = models.CharField(_("collab"), max_length=64, null=True, blank=True)
    z_links = models.CharField(_("links"), max_length=64, null=True, blank=True)
    z_partial_body = models.CharField(
        _("partial_body"), max_length=64, null=True, blank=True
    )
    # data de atualização / criação do registro fonte
    origin_date = models.CharField(
        _("Origin date"), max_length=10, null=True, blank=True
    )
    # data de primeira publicação no site
    # evita que artigos WIP fique disponíveis antes de estarem públicos
    website_publication_date = models.CharField(
        _("Website publication date"), max_length=10, null=True, blank=True
    )

    base_form_class = CoreAdminModelForm

    panels = [
        FieldPanel("issn_electronic", read_only=True),
        FieldPanel("issn_print", read_only=True),
        FieldPanel("pub_year", read_only=True),
        FieldPanel("volume", read_only=True),
        FieldPanel("number", read_only=True),
        FieldPanel("suppl", read_only=True),
        # FieldPanel("pkg_name", read_only=True),
        # FieldPanel("v3", read_only=True),
        FieldPanel("v2", read_only=True),
        FieldPanel("aop_pid", read_only=True),
        FieldPanel("main_doi", read_only=True),
        FieldPanel("elocation_id", read_only=True),
        FieldPanel("fpage", read_only=True),
        FieldPanel("fpage_seq", read_only=True),
        FieldPanel("lpage", read_only=True),
        FieldPanel("website_publication_date", read_only=True),
        FieldPanel("main_toc_section", read_only=True),
        # FieldPanel("z_article_titles_texts", read_only=True),
        # FieldPanel("z_surnames", read_only=True),
        # FieldPanel("z_collab", read_only=True),
        # FieldPanel("z_links", read_only=True),
        # FieldPanel("z_partial_body", read_only=True),
        AutocompletePanel("current_version", read_only=True),
    ]

    class Meta:
        indexes = [
            models.Index(fields=["pkg_name"]),
            models.Index(fields=["v3"]),
            models.Index(fields=["issn_electronic"]),
            models.Index(fields=["issn_print"]),
            models.Index(fields=["pub_year"]),
            models.Index(fields=["volume"]),
            models.Index(fields=["number"]),
            models.Index(fields=["suppl"]),
            models.Index(fields=["elocation_id"]),
            models.Index(fields=["fpage"]),
            models.Index(fields=["fpage_seq"]),
            models.Index(fields=["lpage"]),
            models.Index(fields=["article_pub_year"]),
            models.Index(fields=["main_doi"]),
            models.Index(fields=["z_article_titles_texts"]),
            models.Index(fields=["z_surnames"]),
            models.Index(fields=["z_collab"]),
            models.Index(fields=["z_links"]),
            models.Index(fields=["z_partial_body"]),
        ]

    def __str__(self):
        return f"{self.pkg_name} {self.v3}"

    @classmethod
    def public_items(cls, from_date):
        now = datetime.utcnow().isoformat()[:10]
        return cls.objects.filter(
            Q(website_publication_date__lte=now)
            & (Q(created__gte=from_date) | Q(updated__gte=from_date)),
        ).iterator()

    @property
    def created_updated(self):
        return self.updated or self.created

    @property
    def data(self):
        _data = {
            "v3": self.v3,
            "v2": self.v2,
            "aop_pid": self.aop_pid,
            "pkg_name": self.pkg_name,
            "created": self.created and self.created.isoformat(),
            "updated": self.updated and self.updated.isoformat(),
            "record_status": "updated" if self.updated else "created",
        }
        return _data

    @classmethod
    def get_xml_with_pre(cls, v3):
        try:
            return cls.objects.get(v3=v3).xml_with_pre
        except:
            return None

    @property
    def xml_with_pre(self):
        return self.current_version and self.current_version.xml_with_pre

    @property
    def is_aop(self):
        return self.volume is None and self.number is None and self.suppl is None

    @classmethod
    def register(
        cls,
        xml_with_pre,
        filename,
        user,
        origin_date=None,
        force_update=None,
        is_published=False,
        website_publication_date=None,
        origin=None,
    ):
        """
        Evaluate the XML data and returns corresponding PID v3, v2, aop_pid

        Parameters
        ----------
        xml : XMLWithPre
        filename : str
        user : User

        Returns
        -------
            {
                "v3": self.v3,
                "v2": self.v2,
                "aop_pid": self.aop_pid,
                "xml_uri": self.xml_uri,
                "article": self.article,
                "created": self.created.isoformat(),
                "updated": self.updated.isoformat(),
                "xml_changed": boolean,
                "record_status": created | updated | retrieved
            }
            or
            {
                "error_type": self.error_type,
                "error_message": self.error_message,
                "id": self.finger_print,
                "filename": self.name,
            }

        """
        try:
            input_data = {}
            input_data["xml_with_pre"] = xml_with_pre
            input_data["filename"] = filename
            input_data["origin"] = origin

            logging.info(f"PidProviderXML.register ....  {origin or filename}")

            # adaptador do xml with pre
            xml_adapter = xml_sps_adapter.PidProviderXMLAdapter(xml_with_pre)

            # consulta se documento já está registrado
            registered = cls._query_document(xml_adapter)

            # analisa se aceita ou rejeita registro
            updated_data = cls.skip_registration(
                xml_adapter, registered, force_update, origin_date
            )
            if updated_data:
                return updated_data

            # verfica os PIDs encontrados no XML / atualiza-os se necessário
            changed_pids = cls._complete_pids(xml_adapter, registered)
            if not xml_adapter.v3:
                raise exceptions.InvalidPidError(
                    f"Unable to register {filename}, because v3 is invalid"
                )

            if not xml_adapter.v2:
                raise exceptions.InvalidPidError(
                    f"Unable to register {filename}, because v2 is invalid"
                )

            # cria ou atualiza registro
            registered = cls._save(
                registered, xml_adapter, user, changed_pids, origin_date
            )

            # TODO substituir is_published por website_publication_date
            # preencher self.website_publication_date = website_publication_date

            # data to return
            data = registered.data.copy()
            data["xml_changed"] = bool(changed_pids)

            pid_request = PidRequest.cancel_failure(
                user=user,
                origin=origin,
                origin_date=origin_date,
                v3=data.get("v3"),
                detail=data,
            )
            response = input_data
            response.update(data)
            return response

        except (exceptions.QueryDocumentMultipleObjectsReturnedError,) as e:
            data = json.loads(str(e))
            pid_request = PidRequest.create_or_update(
                user=user,
                origin=origin,
                origin_date=origin_date,
                result_type=str(type(e)),
                result_msg=_("Found {} records for {}").format(
                    len(data["items"]), data["params"]
                ),
                detail=data,
            )
            response = input_data
            response.update(pid_request.data)
            return response
        except Exception as e:
            # exceptions.ForbiddenPidProviderXMLRegistrationError,
            # exceptions.NotEnoughParametersToGetDocumentRecordError,
            # exceptions.InvalidPidError,
            # outras
            try:
                detail = {}
                if ":" not in origin:
                    detail["xml"] = xml_adapter.tostring()
            except Exception as x:
                pass
            pid_request = PidRequest.register_failure(
                e,
                user=user,
                origin_date=origin_date,
                origin=origin,
                detail=detail,
            )
            response = input_data
            response.update(pid_request.data)
            return response

    @classmethod
    def _save(
        cls,
        registered,
        xml_adapter,
        user,
        changed_pids,
        origin_date=None,
    ):
        if registered:
            registered.updated_by = user
            registered.updated = utcnow()
        else:
            registered = cls()
            registered.creator = user
            registered.created = utcnow()

        # evita que artigos WIP fique disponíveis antes de estarem públicos
        registered.website_publication_date = (
            xml_adapter.xml_with_pre.article_publication_date or origin_date
        )

        registered.origin_date = origin_date
        registered._add_data(xml_adapter, user)
        registered._add_journal(xml_adapter)
        registered._add_issue(xml_adapter)
        registered._add_current_version(xml_adapter, user)

        registered.save()

        registered._add_pid_changes(changed_pids, user)

        return registered

    @classmethod
    def skip_registration(cls, xml_adapter, registered, force_update, origin_date):
        """
        XML é versão AOP, mas
        documento está registrado com versão VoR (fascículo),
        então, recusar o registro,
        pois está tentando registrar uma versão desatualizada
        """
        logging.info("PidProviderXML.skip_registration")

        if force_update:
            return

        if not registered:
            return

        # verifica se é necessário atualizar
        if registered.is_equal_to(xml_adapter):
            # XML fornecido é igual ao registrado, não precisa continuar
            logging.info(f"Skip update: equal")
            return registered.data

        if xml_adapter.is_aop and registered and not registered.is_aop:
            logging.info(f"Skip update: forbidden")
            raise exceptions.ForbiddenPidProviderXMLRegistrationError(
                _(
                    "The XML content is an ahead of print version "
                    "but the document {} is already published in an issue"
                ).format(registered)
            )

        if (
            origin_date
            and registered.origin_date
            and registered.origin_date > origin_date
        ):
            # retorna item registrado que está mais atualizado
            logging.info(f"Skip update: is already up-to-date")
            return registered.data

    def is_equal_to(self, xml_adapter):
        return bool(
            self.current_version
            and self.current_version.finger_print == xml_adapter.finger_print
        )

    @classmethod
    def get_registered(cls, xml_with_pre, origin):
        """
        Get registered

        Parameters
        ----------
        xml_with_pre : XMLWithPre

        Returns
        -------
            None
            or
            {
                "v3": self.v3,
                "v2": self.v2,
                "aop_pid": self.aop_pid,
                "xml_uri": self.xml_uri,
                "article": self.article,
                "created": self.created.isoformat(),
                "updated": self.updated.isoformat(),
            }
            or
            {"error_msg": str(e), "error_type": str(type(e))}
        """
        try:
            xml_adapter = xml_sps_adapter.PidProviderXMLAdapter(xml_with_pre)
            registered = cls._query_document(xml_adapter)
            return registered.data
        except Exception as e:
            # except (
            #     exceptions.NotEnoughParametersToGetDocumentRecordError,
            #     exceptions.QueryDocumentMultipleObjectsReturnedError,
            # ) as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            UnexpectedEvent.create(
                exception=e,
                exc_traceback=exc_traceback,
                detail={
                    "operation": "PidProviderXML.get_registered",
                    "detail": dict(
                        origin=origin,
                    ),
                },
            )
            return {"error_msg": str(e), "error_type": str(type(e))}

    @classmethod
    def _query_document(cls, xml_adapter):
        """
        Query document

        Arguments
        ---------
        xml_adapter : PidProviderXMLAdapter

        Returns
        -------
        None or PidProviderXML

        Raises
        ------
        exceptions.QueryDocumentMultipleObjectsReturnedError
        exceptions.NotEnoughParametersToGetDocumentRecordError
        """
        LOGGER.info("_query_document")
        items = xml_adapter.query_list
        for params in items:
            cls.validate_query_params(params)

            adapted_params_ = xml_adapter.adapt_query_params(params)

            if adapted_params_.get("issue__isnull"):
                adapted_params_.pop("issue__isnull")
                adapted_params_["volume__isnull"] = True
                adapted_params_["number__isnull"] = True
                adapted_params_["suppl__isnull"] = True
            adapted_params = {
                name.replace("journal__", "").replace("issue__", ""): v
                for name, v in adapted_params_.items()
            }

            try:
                return cls.objects.get(**adapted_params)
            except cls.DoesNotExist:
                continue
            except cls.MultipleObjectsReturned as e:
                # seria inesperado já que os dados informados devem encontrar
                # ocorrência única ou None
                items = []
                for item in cls.objects.filter(**adapted_params).iterator():
                    items.append(item.data)
                # try:
                #     cls.objects.filter(**adapted_params).delete()
                #     deleted = True
                # except Exception as e:
                #     logging.exception(e)
                #     deleted = str(e)

                raise exceptions.QueryDocumentMultipleObjectsReturnedError(
                    str({"params": adapted_params, "items": items})
                )

    def _add_data(self, xml_adapter, user):
        self.pkg_name = xml_adapter.sps_pkg_name
        self.article_pub_year = xml_adapter.article_pub_year
        self.v3 = xml_adapter.v3
        self.v2 = xml_adapter.v2
        self.aop_pid = xml_adapter.aop_pid

        self.fpage = xml_adapter.fpage
        self.fpage_seq = xml_adapter.fpage_seq
        self.lpage = xml_adapter.lpage

        self.main_doi = xml_adapter.main_doi
        self.main_toc_section = xml_adapter.main_toc_section
        self.elocation_id = xml_adapter.elocation_id

        self.z_article_titles_texts = xml_adapter.z_article_titles_texts
        self.z_surnames = xml_adapter.z_surnames
        self.z_collab = xml_adapter.z_collab
        self.z_links = xml_adapter.z_links
        self.z_partial_body = xml_adapter.z_partial_body

    def _add_journal(self, xml_adapter):
        self.issn_electronic = xml_adapter.journal_issn_electronic
        self.issn_print = xml_adapter.journal_issn_print

    def _add_issue(self, xml_adapter):
        self.volume = xml_adapter.volume
        self.number = xml_adapter.number
        self.suppl = xml_adapter.suppl
        self.pub_year = xml_adapter.pub_year

    def _add_current_version(self, xml_adapter, user):
        self.current_version = XMLVersion.get_or_create(user, xml_adapter.xml_with_pre)

    def _add_pid_changes(self, changed_pids, user):
        # requires registered.current_version is set
        if not changed_pids:
            return
        if not self.current_version:
            raise ValueError(
                "PidProviderXML._add_pid_changes requires current_version is set"
            )
        for change_args in changed_pids:
            if change_args["pid_in_xml"]:
                # somente registra as mudanças de um pid_in_xml não vazio
                change_args["user"] = user
                change_args["version"] = self.current_version
                change_args["pkg_name"] = self.pkg_name
                PidChange.get_or_create(**change_args)

    @classmethod
    def _get_unique_v3(cls):
        """
        Generate v3 and return it only if it is new

        Returns
        -------
            str
        """
        while True:
            generated = v3_gen.generates()
            if not cls._is_registered_pid(v3=generated):
                return generated

    @classmethod
    def _is_registered_pid(cls, v2=None, v3=None, aop_pid=None):
        if v3:
            kwargs = {"v3": v3}
        elif v2:
            kwargs = {"v2": v2}
        elif aop_pid:
            kwargs = {"aop_pid": aop_pid}

        if kwargs:
            try:
                found = cls.objects.filter(**kwargs)[0]
            except IndexError:
                return False
            else:
                return True

    @classmethod
    def _v2_generates(cls, xml_adapter):
        # '2022-10-19T13:51:33.830085'
        h = utcnow()
        mm = str(h.month).zfill(2)
        dd = str(h.day).zfill(2)
        nnnnn = str(h.timestamp()).split(".")[0][-5:]
        return f"{xml_adapter.v2_prefix}{mm}{dd}{nnnnn}"

    @classmethod
    def _get_unique_v2(cls, xml_adapter):
        """
        Generate v2 and return it only if it is new

        Returns
        -------
            str
        """
        while True:
            generated = cls._v2_generates(xml_adapter)
            if not cls._is_registered_pid(v2=generated):
                return generated

    @classmethod
    def _complete_pids(cls, xml_adapter, registered):
        """
        No XML pode conter ou não os PIDS v2, v3 e aop_pid.
        Na base de dados o documento do XML pode ou não estar registrado.

        O resultado deste procedimento é que seja garantido que os
        valores dos PIDs no XML sejam inéditos ou recuperados da base de dados.

        Se no XML existir os PIDs, os valores são verificados na base de dados,
        se são inéditos, não haverá mudança no XML, mas se os PIDs do XML
        conflitarem com os PIDs registrados ou seus valores forem inválidos,
        haverá mudança nos PIDs.

        Parameters
        ----------
        xml_adapter: PidProviderXMLAdapter
        registered: XMLArticle

        Returns
        -------
        bool

        """
        before = dict(
            pid_v3=xml_adapter.v3,
            pid_v2=xml_adapter.v2,
            aop_pid=xml_adapter.aop_pid,
        )

        # garante que não há espaços extras
        if xml_adapter.v3:
            xml_adapter.v3 = xml_adapter.v3.strip()
        if xml_adapter.v2:
            xml_adapter.v2 = xml_adapter.v2.strip()
        if xml_adapter.aop_pid:
            xml_adapter.aop_pid = xml_adapter.aop_pid.strip()

        # adiciona os pids faltantes ao XML fornecido
        cls._add_pid_v3(xml_adapter, registered)
        cls._add_pid_v2(xml_adapter, registered)
        cls._add_aop_pid(xml_adapter, registered)

        after = dict(
            pid_v3=xml_adapter.v3,
            pid_v2=xml_adapter.v2,
            aop_pid=xml_adapter.aop_pid,
        )

        LOGGER.info("%s %s" % (before, after))

        # verifica se houve mudança nos PIDs do XML
        changes = []
        for k, v in before.items():
            if v and v != after[k]:
                changes.append(
                    dict(
                        pid_type=k,
                        pid_in_xml=v,
                        pid_assigned=after[k],
                    )
                )
        return changes

    @classmethod
    def _is_valid_pid(cls, value):
        return bool(value and len(value) == 23)

    @classmethod
    def _add_pid_v3(cls, xml_adapter, registered):
        """
        Atribui v3 ao xml_adapter,
        recuperando do registered ou obtendo um v3 inédito

        Arguments
        ---------
        xml_adapter: PidProviderXMLAdapter
        registered: XMLArticle
        """
        if registered:
            # recupera do registrado
            xml_adapter.v3 = registered.v3
        else:
            # se v3 de xml está ausente ou já está registrado para outro xml
            if not cls._is_valid_pid(xml_adapter.v3) or cls._is_registered_pid(
                v3=xml_adapter.v3
            ):
                # obtém um v3 inédito
                xml_adapter.v3 = cls._get_unique_v3()

    @classmethod
    def _add_aop_pid(cls, xml_adapter, registered):
        """
        Atribui aop_pid ao xml_adapter, recuperando do registered, se existir

        Arguments
        ---------
        xml_adapter: PidProviderXMLAdapter
        registered: XMLArticle
        """
        if registered and registered.aop_pid:
            xml_adapter.aop_pid = registered.aop_pid

    @classmethod
    def _add_pid_v2(cls, xml_adapter, registered):
        """
        Adiciona ou atualiza a xml_adapter, v2 recuperado de registered ou gerado

        Arguments
        ---------
        xml_adapter: PidProviderXMLAdapter
        registered: XMLArticle

        """
        if registered and registered.v2 and xml_adapter.v2 != registered.v2:
            xml_adapter.v2 = registered.v2
        if not cls._is_valid_pid(xml_adapter.v2):
            xml_adapter.v2 = cls._get_unique_v2(xml_adapter)

    @classmethod
    def validate_query_params(cls, query_params):
        """
        Validate query parameters

        Arguments
        ---------
        filter_by_issue: bool
        aop_version: bool

        Returns
        -------
        bool
        """
        _params = query_params
        if not any(
            [
                _params.get("journal__issn_print"),
                _params.get("journal__issn_electronic"),
            ]
        ):
            raise exceptions.NotEnoughParametersToGetDocumentRecordError(
                _("No attribute enough for disambiguations {}").format(
                    _params,
                )
            )

        if not any(
            [
                _params.get("article_pub_year"),
                _params.get("issue__pub_year"),
            ]
        ):
            raise exceptions.NotEnoughParametersToGetDocumentRecordError(
                _("No attribute enough for disambiguations {}").format(
                    _params,
                )
            )

        if any(
            [
                _params.get("main_doi"),
                _params.get("fpage"),
                _params.get("elocation_id"),
            ]
        ):
            return True

        if not any(
            [
                _params.get("z_surnames"),
                _params.get("z_collab"),
                _params.get("z_links"),
                _params.get("pkg_name"),
            ]
        ):
            raise exceptions.NotEnoughParametersToGetDocumentRecordError(
                _("No attribute enough for disambiguations {}").format(
                    _params,
                )
            )
        return True


class CollectionPidRequest(CommonControlField):
    collection = models.ForeignKey(
        Collection, on_delete=models.SET_NULL, null=True, blank=True
    )
    end_date = models.CharField(max_length=10, null=True, blank=True)

    def __unicode__(self):
        return f"{self.collection}"

    def __str__(self):
        return f"{self.collection}"

    @classmethod
    def get(
        cls,
        collection=None,
    ):
        if collection:
            return cls.objects.get(collection=collection)
        raise ValueError("PidRequest.get requires parameters")

    @classmethod
    def create_or_update(
        cls,
        user=None,
        collection=None,
        end_date=None,
    ):
        try:
            obj = cls.get(collection=collection)
            obj.updated_by = user
        except cls.DoesNotExist:
            obj = cls()
            obj.creator = user
            obj.collection = collection

        obj.end_date = end_date or obj.end_date
        obj.save()
        return obj

    panels = [
        FieldPanel("end_date"),
    ]

    base_form_class = CoreAdminModelForm
