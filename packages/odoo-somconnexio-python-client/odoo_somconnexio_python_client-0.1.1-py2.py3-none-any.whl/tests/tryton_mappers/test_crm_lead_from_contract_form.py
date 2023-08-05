from __future__ import unicode_literals  # support both Python2 and 3

import unittest2 as unittest

from odoo_somconnexio_python_client.tryton_mappers.crm_lead_from_contract_form import (
    CRMLeadFromContractForm,
)

from .tryton_factories import FakeContractForm


class CRMLeadFromContractFormTests(unittest.TestCase):
    def test_mobile_contract_new(self):
        contract_data = FakeContractForm().data

        # Mobile
        contract_data["service"] = "mobile"
        # New
        contract_data["mobile_option"] = "new"
        # No Delivery
        contract_data["mobile_delivery_street"] = None

        subscription_request_id = 123

        sr_data = CRMLeadFromContractForm(
            contract_data,
            subscription_request_id=subscription_request_id,
        ).to_dict()

        self.assertEqual(sr_data["iban"], contract_data.get("bank_iban_service"))
        self.assertEqual(sr_data["subscription_request_id"], subscription_request_id)
        self.assertEqual(len(sr_data["lead_line_ids"]), 1)

        lead_line = sr_data["lead_line_ids"][0]

        mobile_isp_info = lead_line["mobile_isp_info"]

        self.assertEqual(mobile_isp_info["type"], "new")
        self.assertEqual(lead_line["product_code"], contract_data["product_mobile"])

    def test_mobile_contract_new_delivery(self):
        contract_data = FakeContractForm().data

        # Mobile
        contract_data["service"] = "mobile"
        # New
        contract_data["mobile_option"] = "new"

        subscription_request_id = 123

        sr_data = CRMLeadFromContractForm(
            contract_data,
            subscription_request_id=subscription_request_id,
        ).to_dict()

        lead_line = sr_data["lead_line_ids"][0]
        mobile_isp_info = lead_line["mobile_isp_info"]
        delivery_address = mobile_isp_info["delivery_address"]

        self.assertEqual(
            delivery_address["street"], contract_data.get("mobile_delivery_street")
        )
        self.assertEqual(
            delivery_address["city"], contract_data.get("mobile_delivery_city")
        )
        self.assertEqual(
            delivery_address["zip_code"], contract_data.get("mobile_delivery_zip")
        )
        self.assertEqual(
            delivery_address["state"], contract_data.get("mobile_delivery_subdivision")
        )
        self.assertEqual(
            delivery_address["country"], contract_data.get("mobile_delivery_country")
        )

    def test_mobile_contract_portability(self):
        contract_data = FakeContractForm().data

        # Mobile
        contract_data["service"] = "mobile"
        # New
        contract_data["mobile_option"] = "portability"

        subscription_request_id = 123

        sr_data = CRMLeadFromContractForm(
            contract_data,
            subscription_request_id=subscription_request_id,
        ).to_dict()

        lead_line = sr_data["lead_line_ids"][0]
        mobile_isp_info = lead_line["mobile_isp_info"]

        self.assertEqual(mobile_isp_info["type"], "portability")
        self.assertEqual(
            mobile_isp_info["previous_provider"],
            contract_data.get("mobile_telecom_company"),
        )
        self.assertEqual(
            mobile_isp_info["previous_owner_vat_number"],
            contract_data.get("mobile_vat_number"),
        )
        self.assertEqual(
            mobile_isp_info["previous_owner_name"], contract_data.get("mobile_surname")
        )
        self.assertEqual(
            mobile_isp_info["previous_owner_first_name"],
            contract_data.get("mobile_name"),
        )
        self.assertEqual(
            mobile_isp_info["icc_donor"], contract_data.get("mobile_icc_number")
        )
        self.assertEqual(
            mobile_isp_info["previous_contract_type"],
            contract_data.get("mobile_previous_contract_type"),
        )

    def test_mobile_contract_portability_sc_icc(self):
        contract_data = FakeContractForm().data

        # Mobile
        contract_data["service"] = "mobile"
        # New
        contract_data["mobile_option"] = "portability"

        subscription_request_id = 123

        sr_data = CRMLeadFromContractForm(
            contract_data,
            subscription_request_id=subscription_request_id,
        ).to_dict()

        lead_line = sr_data["lead_line_ids"][0]
        mobile_isp_info = lead_line["mobile_isp_info"]

        self.assertEqual(mobile_isp_info["icc"], contract_data.get("mobile_sc_icc"))

    def test_broadband_contract_new(self):
        contract_data = FakeContractForm().data

        # Broadband
        contract_data["service"] = "adsl"
        # New
        contract_data["internet_now"] = ""

        contract_data["internet_delivery_street"] = ""

        subscription_request_id = 123

        sr_data = CRMLeadFromContractForm(
            contract_data,
            subscription_request_id=subscription_request_id,
        ).to_dict()

        self.assertEqual(len(sr_data["lead_line_ids"]), 1)

        lead_line = sr_data["lead_line_ids"][0]

        broadband_isp_info = lead_line["broadband_isp_info"]

        self.assertEqual(broadband_isp_info["type"], "new")
        self.assertEqual(lead_line["product_code"], contract_data["product_broadband"])

        service_address = broadband_isp_info["service_address"]

        self.assertEqual(
            service_address["street"], contract_data.get("internet_street")
        )
        self.assertEqual(service_address["city"], contract_data.get("internet_city"))
        self.assertEqual(service_address["zip_code"], contract_data.get("internet_zip"))
        self.assertEqual(
            service_address["state"], contract_data.get("internet_subdivision")
        )
        self.assertEqual(
            service_address["country"], contract_data.get("internet_country")
        )

    def test_broadband_contract_new_delivery(self):
        contract_data = FakeContractForm().data

        # Broadband
        contract_data["service"] = "adsl"
        # New
        contract_data["internet_now"] = ""

        subscription_request_id = 123

        sr_data = CRMLeadFromContractForm(
            contract_data,
            subscription_request_id=subscription_request_id,
        ).to_dict()

        lead_line = sr_data["lead_line_ids"][0]
        broadband_isp_info = lead_line["broadband_isp_info"]
        delivery_address = broadband_isp_info["delivery_address"]

        self.assertEqual(
            delivery_address["street"], contract_data.get("internet_delivery_street")
        )
        self.assertEqual(
            delivery_address["city"], contract_data.get("internet_delivery_city")
        )
        self.assertEqual(
            delivery_address["zip_code"], contract_data.get("internet_delivery_zip")
        )
        self.assertEqual(
            delivery_address["state"],
            contract_data.get("internet_delivery_subdivision"),
        )
        self.assertEqual(
            delivery_address["country"], contract_data.get("internet_delivery_country")
        )

    def test_broadband_contract_portability(self):
        contract_data = FakeContractForm().data

        # Broadband
        contract_data["service"] = "adsl"
        # New
        contract_data["internet_now"] = "adsl"
        contract_data["internet_phone_number"] = "current_number"

        subscription_request_id = 123

        sr_data = CRMLeadFromContractForm(
            contract_data,
            subscription_request_id=subscription_request_id,
        ).to_dict()

        lead_line = sr_data["lead_line_ids"][0]
        broadband_isp_info = lead_line["broadband_isp_info"]

        self.assertEqual(
            broadband_isp_info["phone_number"], contract_data.get("internet_phone_now")
        )
        self.assertEqual(
            broadband_isp_info["previous_provider"],
            contract_data.get("internet_telecom_company"),
        )
        self.assertEqual(
            broadband_isp_info["previous_owner_vat_number"],
            contract_data.get("internet_vat_number"),
        )
        self.assertEqual(
            broadband_isp_info["previous_owner_name"],
            contract_data.get("internet_surname"),
        )
        self.assertEqual(
            broadband_isp_info["previous_owner_first_name"],
            contract_data.get("internet_name"),
        )
        self.assertEqual(
            broadband_isp_info["previous_service"], contract_data.get("internet_now")
        )
        self.assertTrue(broadband_isp_info["keep_phone_number"])

    def test_two_services(self):
        contract_data = FakeContractForm().data

        # Broadband
        contract_data["service"] = "mobile_adsl"
        # New
        contract_data["internet_now"] = "adsl"

        subscription_request_id = 123

        sr_data = CRMLeadFromContractForm(
            contract_data,
            subscription_request_id=subscription_request_id,
        ).to_dict()

        self.assertEqual(len(sr_data["lead_line_ids"]), 2)
