from __future__ import unicode_literals  # support both Python2 and 3

import unittest2 as unittest

from odoo_somconnexio_python_client.tryton_mappers.subscription_request_from_partner_form import (
    SubscriptionRequestFromPartnerForm,
)

from .tryton_factories import FakePartnerForm


class SubscriptionRequestFromPartnerFormTests(unittest.TestCase):
    def test_to_dict(self):
        partner_data = FakePartnerForm().data

        expected_payment_type = (
            "split" if partner_data.get("payment_10_terms") else "single"
        )
        expected__type = (
            "sponsorship"
            if partner_data.get("partner_do_option") == "do_by_partner"
            else "new"
        )
        expected_address = {
            "street": partner_data.get("street"),
            "zip_code": partner_data.get("zip"),
            "city": partner_data.get("city"),
            "state": partner_data.get("subdivision"),
            "country": partner_data.get("country"),
        }

        sr_data = SubscriptionRequestFromPartnerForm(partner_data).to_dict()

        self.assertEqual(sr_data["name"], partner_data.get("name"))
        self.assertEqual(sr_data["type"], expected__type)
        self.assertEqual(sr_data["email"], partner_data.get("email"))
        self.assertEqual(sr_data["address"], expected_address)
        self.assertEqual(sr_data["iban"], partner_data.get("bank_iban"))
        self.assertEqual(sr_data["vat"], partner_data.get("vat_number"))
        self.assertEqual(sr_data["payment_type"], expected_payment_type)
        self.assertEqual(sr_data["nationality"], partner_data.get("nationality"))
