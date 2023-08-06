import logging
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from flags.models import FlagState
from dnoticias_tables.abstract.relational.metronic_process import MetronicProcess

logger = logging.getLogger(__name__)

class FlagStateProcess(MetronicProcess):
    NAME_TEXT = _("Nome")
    CONDITION_TEXT = _("Condição")
    VALUE_TEXT = _("Valor")
    REQUIRED_TEXT = _("Obrigatório")

    CAN_EDIT_TEXT = _("Pode editar")
    EDIT_URL_TEXT = _("Hiperligação para editar instância")

    CAN_DELETE_TEXT = _("Pode eliminar")
    DELETE_URL_TEXT = _("Hiperligação para remover instância")

    POST_REDIRECT_URL_TEXT = _("Hiperligaçao após a chamada para eliminar a instância")

    def __init__(self, request):
        super(FlagStateProcess, self).__init__(request)
        self.on_click_url = 'flag-state-wildcard-view'
        self.extra_params = {
            "kwargs": {
                "pk": "pk"
            }
        }

    def get_table_id(self):
        return "kt_datatable_flag_state"

    def get_view_details(self):
        return "FlagStateProcess request"

    def set_thead(self):
        return [
            ["name", self.NAME_TEXT],
            ["condition", self.CONDITION_TEXT],
            ["value", self.VALUE_TEXT],
            ["required", self.REQUIRED_TEXT],
        ]

    def get_extra_thead(self):
        return [
            ["can_edit", self.CAN_EDIT_TEXT],
            ["edit_url", self.EDIT_URL_TEXT],

            ["can_delete", self.CAN_DELETE_TEXT],
            ["delete_url", self.DELETE_URL_TEXT],

            ["post_redirect_url", self.POST_REDIRECT_URL_TEXT],
        ]

    def set_orderable_fields(self):
        return [
            "name",
            "condition",
            "value",
            "required",
        ]

    def set_searchable(self):
        return [
            "name__icontains",
            "condition__icontains",
            "value__icontains",
            "required__icontains",
        ]

    def set_query_set(self):
        site_prefix = "SITE_{}".format(settings.SITE_ID)
        return FlagState.objects.filter(
            Q(name__istartswith=site_prefix) | ~Q(name__istartswith="SITE_")
        )

    def get_custom_post_redirect_url_value(self, instance):
        return reverse("flag-state-list-view")

    def get_custom_can_edit_value(self, instance):
        return self.request.user.has_perm("flags.change_flagstate")

    def get_custom_can_edit_value(self, instance):
        return self.request.user.has_perm("flags.change_flagstate")

    def get_custom_edit_url_value(self, instance):
        return reverse(
            "flag-state-wildcard-view",
            kwargs={
                "pk" : instance.pk
            }
        )

    def get_custom_can_delete_value(self, instance):
        return self.request.user.has_perm("flags.delete_flagstate")

    def get_custom_delete_url_value(self, instance):
        return reverse(
            "flag-state-delete-view",
            kwargs={
                "pk" : instance.pk
            }
        )
