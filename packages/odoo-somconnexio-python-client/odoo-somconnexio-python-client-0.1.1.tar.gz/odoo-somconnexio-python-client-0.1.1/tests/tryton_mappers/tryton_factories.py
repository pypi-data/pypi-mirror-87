import factory
import random

factory.Faker._DEFAULT_LOCALE = "es_ES"


class TrytonModel(object):
    """ Represents Tryton's model """

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class TrytonFactory(factory.Factory):
    """ Generates Tryton's model instances """

    class Meta:
        abstract = True
        model = TrytonModel
        strategy = "build"

    id = factory.Sequence(lambda n: n)

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        return target_class(*args, **kwargs)


class SubdivisionFactory(TrytonFactory):
    name = factory.Faker("name")
    code = factory.Faker("country_code")


class CountryFactory(TrytonFactory):
    name = factory.Faker("country")
    code = factory.Faker("country_code")


class AddressFactory(TrytonFactory):
    street = factory.Faker("address")
    zip = factory.Faker("postcode")
    city = factory.Faker("city")
    subdivision = factory.SubFactory(SubdivisionFactory)
    country = factory.SubFactory(CountryFactory)


class FakePartnerForm(TrytonFactory):
    partner_do_option = random.choice(["do_by_partner", "do_partner"])
    type = random.choice(["do_by_partner", "do_partner"])
    surname = factory.Faker("last_name")
    lastname = factory.Faker("last_name")
    name = factory.Faker("name")
    tradename = factory.Faker("name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    street = factory.Faker("street_address")
    zip = factory.Faker("postcode")
    city = factory.Faker("city")
    subdivision = factory.SubFactory(SubdivisionFactory)
    country = factory.SubFactory(CountryFactory)
    lang = random.choice(["es", "ca"])
    vat_number = factory.Faker("doi")
    bank_iban = factory.Faker("iban")
    nationality = factory.SubFactory(CountryFactory)
    payment_10_terms = random.choice([True, False])
    partner_number = factory.Faker("doi")
    party_type = random.choice(["person", "organization"])

    birth_date_day = factory.Faker("day_of_month")
    birth_date_month = factory.Faker("month")
    birth_date_year = factory.Faker("year")

    @factory.lazy_attribute
    def data(self):
        return {
            "partner_do_option": self.partner_do_option,
            "partner_number": self.partner_number,
            "name": self.name,
            "lastname": self.lastname,
            "surname": self.surname,
            "tradename": self.tradename,
            "lang": self.lang,
            "birth_date": "{}-{}-{}".format(
                self.birth_date_year, self.birth_date_month, self.birth_date_day
            ),
            "vat_number": self.vat_number,
            "email": self.email,
            "phone": self.phone,
            "bank_iban": self.bank_iban,
            "street": self.street,
            "zip": self.zip,
            "city": self.city,
            "subdivision": self.subdivision.code,
            "country": self.country.code,
            "party_type": self.party_type,
            # To transform to models
            "nationality": self.country.code,
            # To investigate
            "contribute_somconnexio_option": "0",
            "sex": "male",
        }


class FakeContractMobileForm(TrytonFactory):
    mobile_option = random.choice(["new", "portability"])
    mobile_phone_number = factory.Faker("phone_number")
    mobile_sc_sim = random.choice([True, False])
    mobile_sc_icc = "1234567"
    mobile_icc_number = "1234567"
    mobile_telecom_company = 1
    mobile_vat_number = factory.Faker("doi")

    mobile_delivery = random.choice([True, False])
    mobile_delivery_street = factory.Faker("street_address")
    mobile_delivery_zip = factory.Faker("postcode")
    mobile_delivery_city = factory.Faker("city")
    mobile_delivery_subdivision = factory.SubFactory(SubdivisionFactory)
    mobile_delivery_country = factory.SubFactory(CountryFactory)
    mobile_previous_contract_type = random.choice(["contract", "prepaid"])

    mobile_lastname = factory.Faker("last_name")
    mobile_surname = factory.Faker("last_name")
    mobile_name = factory.Faker("name")

    @factory.lazy_attribute
    def data(self):
        return {
            "mobile_delivery_city": self.mobile_delivery_city,
            "mobile_delivery_zip": self.mobile_delivery_zip,
            "mobile_delivery_street": self.mobile_delivery_street,
            "mobile_delivery_country": self.mobile_delivery_country,
            "mobile_phone_number": self.mobile_phone_number,
            "mobile_lastname": self.mobile_lastname,
            "mobile_surname": self.mobile_surname,
            "mobile_name": self.mobile_name,
            "mobile_previous_contract_type": self.mobile_previous_contract_type,
            "mobile_option": self.mobile_option,
            "mobile_vat_number": self.mobile_vat_number,
            "mobile_icc_number": self.mobile_icc_number,
            "mobile_sc_icc": self.mobile_sc_icc,
            "product_mobile": "mobile_product",
        }


class FakeContractInternetForm(TrytonFactory):
    internet_now = random.choice(["adsl", "fibre", ""])
    internet_phone_now = factory.Faker("phone_number")
    internet_phone_number = random.choice(["current_phone", "new_phone"])
    internet_telecom_company = 1
    internet_vat_number = factory.Faker("doi")
    internet_name = factory.Faker("name")
    internet_surname = factory.Faker("last_name")
    internet_lastname = factory.Faker("last_name")

    internet_street = factory.Faker("street_address")
    internet_zip = factory.Faker("postcode")
    internet_city = factory.Faker("city")
    internet_subdivision = factory.SubFactory(SubdivisionFactory)
    internet_country = factory.SubFactory(CountryFactory)

    internet_delivery = random.choice([True, False])
    internet_delivery_street = factory.Faker("street_address")
    internet_delivery_zip = factory.Faker("postcode")
    internet_delivery_city = factory.Faker("city")
    internet_delivery_subdivision = factory.SubFactory(SubdivisionFactory)
    internet_delivery_country = factory.SubFactory(CountryFactory)

    @factory.lazy_attribute
    def data(self):
        return {
            "internet_vat_number": self.internet_vat_number,
            "internet_name": self.internet_name,
            "internet_lastname": self.internet_lastname,
            "internet_surname": self.internet_surname,
            "internet_zip": self.internet_zip,
            "internet_street": self.internet_street,
            "internet_country": self.internet_country.code,
            "internet_city": self.internet_city,
            "internet_phone_number": self.internet_phone_number,
            "internet_now": self.internet_now,
            "internet_phone_now": self.internet_phone_now,
            "internet_delivery_street": self.internet_delivery_street,
            "internet_delivery_city": self.internet_delivery_city,
            "internet_delivery_zip": self.internet_delivery_zip,
            "internet_delivery_country": self.internet_delivery_country.code,
            "product_broadband": "internet_product",
        }


class FakeContractForm(TrytonFactory):
    service = random.choice(["adsl", "mobile", "mobile_adsl"])
    bank_iban_service = factory.Faker("iban")
    mobile_contract = factory.SubFactory(FakeContractMobileForm)
    internet_contract = factory.SubFactory(FakeContractInternetForm)

    @factory.lazy_attribute
    def data(self):
        base = {
            "service": self.service,
            "bank_iban_service": self.bank_iban_service,
            "partner": None,
            "bank_owner_service_name": "",
        }
        base.update(self.mobile_contract.data)
        base.update(self.internet_contract.data)

        return base
