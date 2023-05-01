import logging
from .hubspot_wrapper import Hubspot

# from helper_functions import compare_names

"""
This module processes the collected data so it can be send to the Hubspot Module
"""


def hubspot_process_results(
    api_key: str, results: list, column_names: list, table_name: str
):
    """
    function that handles the processing of the results for it to be send to Hubspot
    """
    hubspot_instance = Hubspot(api_key)
    properties = []

    object_name = get_object_name(table_name)
    request_type = get_http_request_type(table_name)
    property_names = hubspot_instance.get_company_properties()
    known_names = compare_names(column_names, property_names)

    for result in results:
        """Hubspot only accepts 100 items per call"""
        if len(properties) < 100:
            properties.append(create_data_dict(result, column_names, known_names))
        else:
            """
            send the collected data in patch, empty properties and start with the next results
            """
            logging.info("full batch ready")
            send_data(request_type, object_name, properties, hubspot_instance)
            properties.clear()
            properties.append(create_data_dict(result, column_names, known_names))

    if len(properties) > 0:
        logging.info("final batch ready")
        send_data("company", "patch", properties, hubspot_instance)


def send_data(
    object_type: str, change_type: str, properties: list, hubspot_instance: Hubspot
):
    """
    Method to send data in the correct direction for
    object_type (company, contact, deals) and
    change_type (patch)
    """
    if object_type == "companies":
        if change_type == "patch":
            logging.info("companies patch")
            hubspot_instance.send_company_patch(inputs=properties)
    if object_type == "contacts":
        if change_type == "patch":
            logging.info("contacts patch")
            hubspot_instance.send_contact_patch(inputs=properties)
    if object_type == "deals":
        if change_type == "patch":
            logging.info("deals patch")
            hubspot_instance.send_deal_patch(inputs=properties)


def create_data_dict(result: list, column_names: list, known_names: list):
    """
    Method to process a result list to a dict of keys id and properties.
    All elements besides hubspot_company_id are stored in a dict under properties
    The assumption is that the data per row is in the same order as the column names
    """
    result_dict = {}
    property_dict = {}

    for name in column_names:
        if name in known_names:
            """
            For 1-to-1 column_names and property_names
            """
            if name == "id":
                result_dict[name] = result[column_names.index(name)]
            else:
                property_dict["users"] = result[column_names.index(name)]
        else:
            # TODO: find more abstract way of doing this
            if name == "user_addition" and ("user_subtraction" in column_names):
                addition = result[column_names.index(name)]
                subtraction = result[column_names.index("user_subtraction")]

                if addition != None and subtraction != None:
                    property_dict["daily_user_change"] = addition + subtraction
                else:
                    property_dict["daily_user_change"] = (
                        subtraction if subtraction != None else addition
                    )

    result_dict.update({"properties": property_dict})

    return result_dict


def compare_names(source_names: list, destination_names: list):
    """
    This function compares source names with destiny names for one to one data transfer.
    It will give a warning for source names that do not appear in the list of destiny names
    """

    known_destination_names = []

    for name in source_names:
        if name not in destination_names:
            logging.warning("source name: %s does not exist in the dest" % name)
        else:
            known_destination_names.append(name)

    return known_destination_names


def get_object_name(table_name: str):
    """
    This function willreturn the name of the object the data will be send to
    """
    if "companies" in table_name:
        return "companies"
    elif "contacts" in table_name:
        return "contacts"
    elif "deals" in table_name:
        return "deals"
    elif "tickets" in table_name:
        return "tickets"
    else:
        # TODO: remove return statement when table name is correct
        return "companies"
        raise Exception("Could not find the specific hubspot object type in table name")


def get_http_request_type(table_name: str):
    """
    This function will return the request_type based on the table name
    """
    if "patch" in table_name:
        return "patch"
    # elif "post" in table_name:
    #     return "post"
    # elif "get" in table_name:
    #     return "get"
    # elif "delete" in table_name:
    #     return "delete"
    else:
        # TODO: remove return statement when tablename correct
        return "patch"
        raise Exception("Could not find the specific http request in table name")
    else:
        raise Exception("Coild not find the specific http request in table name")
