from odoo_somconnexio_python_client.client import Client

from ..exceptions import ResourceNotFound


class Partner:
    _url_path = "/partner"

    # TODO: Add all the needed fields in the future...
    def __init__(
        self,
        id,
        name,
        firstname,
        lastname,
        ref,
        lang,
        vat,
        type,
        email,
        phone,
        mobile,
        birthdate_date,
        cooperator_register_number,
        cooperator_end_date,
        **kwargs
    ):
        self.id = id
        self.name = name
        self.firstname = firstname
        self.lastname = lastname
        self.ref = ref
        self.lang = lang
        self.vat = vat
        self.type = type
        self.email = email
        self.phone = phone
        self.mobile = mobile
        self.birthdate_date = birthdate_date
        self.cooperator_register_number = cooperator_register_number
        self.cooperator_end_date = cooperator_end_date

    @classmethod
    def get(cls, ref):
        """
        Get ResPartner using the ref param.

        :return: Partner object if exists
        """
        return cls._get(id=int(ref))

    @classmethod
    def search_by_vat(cls, vat):
        """
        Search ResPartner in Odoo by VAT number.

        :return: Partner object if exists
        """
        return cls._get(
            params={
                "vat": vat,
            }
        )

    @classmethod
    def _get(cls, id=None, params={}):
        if id:
            url = "{}/{}".format(cls._url_path, id)
        else:
            url = cls._url_path

        response_data = Client().get(
            "{}".format(url),
            params=params,
        )
        if not response_data:
            raise ResourceNotFound(resource=cls.__name__, filter=params)

        return cls(**response_data)
