from __future__ import unicode_literals  # support both Python2 and 3

import pytest
import unittest2 as unittest

from odoo_somconnexio_python_client.exceptions import ResourceNotFound
from odoo_somconnexio_python_client.resources.partner import Partner


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Replace the API-KEY request header with "DUMMY" in cassettes
        "filter_headers": [("API-KEY", "DUMMY")],
    }


class PartnerTests(unittest.TestCase):
    @pytest.mark.vcr()
    def test_search_resource_not_found(self):
        self.assertRaises(
            ResourceNotFound,
            Partner.search_by_vat,
            vat=''
        )

    @pytest.mark.vcr()
    def test_search_by_vat(self):
        partner = Partner.search_by_vat(vat="55642302N")

        assert partner.ref, "1234"
        assert partner.vat, "55642302N"
        assert partner.name, "Felip Dara"

    @pytest.mark.vcr()
    def test_get_with_ref(self):
        ref = "1234"
        partner = Partner.get(ref)

        assert partner.ref, "1234"
        assert partner.vat, "55642302N"
        assert partner.name, "Felip Dara"
