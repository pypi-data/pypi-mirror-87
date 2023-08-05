class CRMLeadFromContractForm:
    """Mapping class to convert the ContractForm of Tryton in a CRMLead dict expected in the API.
        * Contract data dict:

    ```
            {
              "service": "mobile",
              "bank_iban_service": "",

              # Internet
              "internet_surname": "",
              "internet_name": "",
              "internet_lastname": "",
              "internet_vat_number": "",
              "internet_phone_number": "current_number",
              "internet_country": "64",
              "internet_street": "",
              "internet_zip": "",
              "internet_city": "",
              "internet_now": "",
              "internet_phone_now": "",
              "internet_delivery_zip": "",
              "internet_delivery_country": "64",
              "internet_delivery_street": "",
              "internet_delivery_city": "",

              # Internet Unused
              "internet_delivery_name": "",
              "internet_delivery_phone": "",
              "internet_delivery_surname": "",
              "internet_delivery_lastname": "",
              "internet_speed": "60MB",
              "internet_phone": "phone",
              "internet_phone_minutes": "100+",
              "internet_contract": "adsl",

              # Mobile
              "mobile_surname": "",
              "mobile_lastname": "",
              "mobile_name": "",
              "mobile_vat_number": "",
              "mobile_phone_number": "",
              "mobile_previous_contract_type": "",
              "mobile_option": "new",
              "mobile_icc_number": "",
              "mobile_sc_icc": ""
              "mobile_delivery_city": "",
              "mobile_delivery_zip": "",
              "mobile_delivery_country": "64",
              "mobile_delivery_street": "",

              # Mobile Unused
              "mobile_delivery_surname": "",
              "mobile_delivery_name": "",
              "mobile_delivery_lastname": "",
              "mobile_min": "unlimited",
              "mobile_internet": "1GB",

              # Unused
              "partner": 1118,
              "bank_owner_service_name": "",
            }
    ```

        * CRMLead:

        Attributes:
            contract_form: ContractForm from SomConnexio Tryton Galatea module
            contract_internet_form: ContractInternetForm from SomConnexio Tryton Galatea module
            contract_mobile_form: ContractMobileForm from SomConnexio Tryton Galatea module
    """

    def __init__(
        self,
        contract_data,
        subscription_request_id=None,
        partner_id=None,
    ):
        self.contract_data = contract_data
        self.partner_id = partner_id
        self.subscription_request_id = subscription_request_id

    def to_dict(self):
        base = {
            "iban": self.contract_data.get("bank_iban_service"),
            "lead_line_ids": [],
        }
        if self.partner_id:
            base.update(
                {
                    "partner_id": self.partner_id,
                }
            )
        if self.subscription_request_id:
            base.update(
                {
                    "subscription_request_id": self.subscription_request_id,
                }
            )

        if self.contract_data.get("service") in ["mobile", "mobile_adsl"]:
            base["lead_line_ids"].append(
                {
                    "product_code": self.contract_data.get("product_mobile"),
                    "mobile_isp_info": self._mobile_isp_info(),
                }
            )
        if self.contract_data.get("service") in ["adsl", "mobile_adsl"]:
            base["lead_line_ids"].append(
                {
                    "product_code": self.contract_data.get("product_broadband"),
                    "broadband_isp_info": self._broadband_isp_info(),
                }
            )
        return base

    def _mobile_isp_info(self):
        mobile_isp_info_data = {"type": self.contract_data.get("mobile_option")}

        if self.contract_data.get("mobile_option") == "portability":
            mobile_isp_info_data.update(
                {
                    "phone_number": self.contract_data.get("mobile_phone_number"),
                    "previous_provider": self.contract_data.get(
                        "mobile_telecom_company"
                    ),
                    "previous_owner_vat_number": self.contract_data.get(
                        "mobile_vat_number"
                    ),
                    "previous_owner_name": self.contract_data.get("mobile_surname"),
                    "previous_owner_first_name": self.contract_data.get("mobile_name"),
                    "icc_donor": self.contract_data.get("mobile_icc_number"),
                    "previous_contract_type": self.contract_data.get(
                        "mobile_previous_contract_type"
                    ),
                }
            )
            if self.contract_data.get("mobile_sc_icc"):
                mobile_isp_info_data.update(
                    {
                        "icc": self.contract_data.get("mobile_sc_icc"),
                    }
                )
        if self.contract_data.get("mobile_delivery_street"):
            mobile_isp_info_data.update(
                {
                    "delivery_address": {
                        "street": self.contract_data.get("mobile_delivery_street"),
                        "zip_code": self.contract_data.get("mobile_delivery_zip"),
                        "city": self.contract_data.get("mobile_delivery_city"),
                        "state": self.contract_data.get("mobile_delivery_subdivision"),
                        "country": self.contract_data.get("mobile_delivery_country"),
                    }
                }
            )
        return mobile_isp_info_data

    def _keep_phone_number(self):
        if self.contract_data.get("internet_phone_number") == "current_number":
            return True
        else:
            return False

    def _broadband_isp_info(self):
        broadband_isp_info_data = {
            "type": "portability" if self.contract_data.get("internet_now") else "new",
            "service_address": {
                "street": self.contract_data.get("internet_street"),
                "zip_code": self.contract_data.get("internet_zip"),
                "city": self.contract_data.get("internet_city"),
                "state": self.contract_data.get("internet_subdivision"),
                "country": self.contract_data.get("internet_country"),
            },
        }

        if self.contract_data.get("internet_now"):
            broadband_isp_info_data.update(
                {
                    "phone_number": self.contract_data.get("internet_phone_now"),
                    "previous_provider": self.contract_data.get(
                        "internet_telecom_company"
                    ),
                    "previous_owner_vat_number": self.contract_data.get(
                        "internet_vat_number"
                    ),
                    "previous_owner_name": self.contract_data.get("internet_surname"),
                    "previous_owner_first_name": self.contract_data.get(
                        "internet_name"
                    ),
                    "previous_service": self.contract_data.get("internet_now"),
                    "keep_phone_number": self._keep_phone_number()
                }
            )
        if self.contract_data.get("internet_delivery_street"):
            broadband_isp_info_data.update(
                {
                    "delivery_address": {
                        "street": self.contract_data.get("internet_delivery_street"),
                        "zip_code": self.contract_data.get("internet_delivery_zip"),
                        "city": self.contract_data.get("internet_delivery_city"),
                        "state": self.contract_data.get(
                            "internet_delivery_subdivision"
                        ),
                        "country": self.contract_data.get("internet_delivery_country"),
                    }
                }
            )
        return broadband_isp_info_data
