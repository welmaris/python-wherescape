# import logging
import hubspot

# import send_data
from .send_data import send_data
from .send_data import (
    send_company_object,
    send_contact_object,
    send_deal_object,
)

# from pprint import pprint
# from hubspot.crm.companies import SimplePublicObjectInput, ApiException

"""
module to 
"""


class Hubspot:
    def __init__(self, access_token):
        self.access_token = access_token
        self.client = hubspot.Client.create(access_token=access_token)

    def send_company_patch(self, **args):
        """
        method for sending patches for companies
        """
        inputs = args["inputs"]

        if len(inputs) == 1:
            id = inputs[0]["id"]
            properties = inputs[0]["properties"]
            send_company_object.patch_company_on_id(id, properties, self.client)
        elif len(inputs) > 1:
            send_company_object.patch_company_batch(inputs, self.client)

    def send_contact_patch(self, **args):
        """
        method for sending patches for contacts
        """
        inputs = args["inputs"]

        if len(inputs) == 1:
            id = inputs[0]["id"]
            properties = inputs[0]["properties"]
            send_contact_object.patch_company_on_id(id, properties, self.client)
        elif len(inputs) > 1:
            send_contact_object.patch_company_batch(inputs, self.client)

    def send_deal_patch(self, **args):
        """
        method for sending patches for deals
        """
        inputs = args["inputs"]

        if len(inputs) == 1:
            id = inputs[0]["id"]
            properties = inputs[0]["properties"]
            send_deal_object.patch_company_on_id(id, properties, self.client)
        elif len(inputs) > 1:
            send_deal_object.patch_company_batch(inputs, self.client)
