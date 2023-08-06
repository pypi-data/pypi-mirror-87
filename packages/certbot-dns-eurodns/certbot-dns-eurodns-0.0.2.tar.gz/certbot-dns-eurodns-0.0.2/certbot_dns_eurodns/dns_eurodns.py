"""EuroDNS Certbot plugins.

For full examples, see `certbot.plugins`.

"""

import logging
import re

import requests
import json
import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)

# Documentation URL
ACCOUNT_URL = 'https://docapi.eurodns.com/'

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """Certbot Authenticator for EuroDNS."""

    description = "Certbot Authenticator plugin for EuroDNS"

    # Implement all methods from IAuthenticator, remembering to add
    # "self" as first argument, e.g. def prepare(self)...
    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds=30)
        add(
            "credentials",
            help="EuroDNS credentials INI file.",
            default="/etc/letsencrypt/eurodns.ini",
        )

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return (
            "This plugin configures a DNS CNAME record to respond to a dns-01 challenge using "
            + "the EuroDNS Remote REST API."
        )

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'EuroDNS credentials INI file',
            {
                "applicationId": "User access for EuroDNS v2 API. (See {0}.)" . format(ACCOUNT_URL),
                "apiKey": "Key access for EuroDNS v2 API. (See {0}.)" . format(ACCOUNT_URL),
                "endpoint": "URL of EuroDNS v2 API. (See {0}.)" . format(ACCOUNT_URL)
            }
        )
        logger.debug("endpoint: " + self.credentials.conf("endpoint"))
        logger.debug("appId: " + self.credentials.conf("applicationId"))
        logger.debug("apiKey: " + self.credentials.conf("apiKey"))

    def _perform(self, domain, validation_name, validation):
        logger.debug("domain: "+domain)
        logger.debug("validation_name: " + validation_name)
        logger.debug("validation: " + validation)
        clientRestAPI = self._get_RESTAPIconfig_client()
        clientRestAPI.addRecord(domain, validation_name, validation)
        return (
            "This plugin configures a DNS CNAME record to respond to a dns-01 challenge using "
            + "the EuroDNS Remote REST API."
        )

    def _cleanup(self, domain, validation_name, validation):
        clientRestAPI = self._get_RESTAPIconfig_client()
        clientRestAPI.delRecord(domain, validation_name, validation)
        return (
            "This plugin configures a DNS CNAME record to respond to a dns-01 challenge using "
            + "the EuroDNS Remote REST API."
        )

    def _get_RESTAPIconfig_client(self):
        return _RESTAPIConfigClient(
            self.credentials.conf("endpoint"),
            self.credentials.conf("applicationId"),
            self.credentials.conf("apiKey"),
        )

class _RESTAPIConfigClient(object):
    """
    Encapsulates all communication with the ISPConfig Remote REST API.
    """
    ttl = 600 # minimum valid value for EuroDNS
    type = 'TXT'
    insertRecord = False

    def __init__(self, endpoint, appId, apiKey):
        logger.debug("creating RESTAPIconfigclient")
        self.endpoint = endpoint
        self.authinfo = {"X-APP-ID": appId, "X-API-KEY": apiKey}

    def addRecord(self, domain, validation_name, validation):
        logger.debug('addRecord call')
        host = self._getHost(domain, validation_name)

        zoneJSON = self._getZone(domain)
        zoneJSON['records'].append({
                        'type': self.type,
                        'host': host,
                        'ttl': self.ttl,
                        'data': validation
                         })
        zoneJSONCheck = self._prepZone(domain, zoneJSON)
        logger.debug(zoneJSONCheck)
        if (zoneJSONCheck['report']['isValid'] is False):
            logger.debug('zone is not valid to addRecord')
            raise errors.PluginError(
                "EuroDNS API Error during addRecord: {0}".format(zoneJSONCheck['report']['recordErrors'][0]['messages'])
            )
        logger.debug('addRecord ok')
        self._setZone(domain, zoneJSON)
        self.insertRecord = True


    def delRecord(self, domain, validation_name, validation):
        logger.debug('delRecord call')

        if self.insertRecord is True:
            logger.debug('delRecord call 2')
            host = self._getHost(domain, validation_name)

            zoneJSON = self._getZone(domain)
            zoneJSON['records'] = list(filter(
                lambda record: record['type'] != self.type or record['host'] != host or record['ttl'] != self.ttl or record[
                    'data'] != validation, zoneJSON['records']))
            #logger.debug(json.dumps(zoneJSON))
            zoneJSONCheck = self._prepZone(domain, zoneJSON)

            if zoneJSONCheck['report']['isValid'] is False:
                logger.debug('zone is not valid to delRecord')
                raise errors.PluginError(
                    "EuroDNS API Error during delRecord: {0}".format(zoneJSONCheck['report']['recordErrors'][0]['messages'])
                )

            logger.debug('delRecord ok')
            self._setZone(domain, zoneJSON)

    def _getZone(self, domain):
        logger.debug('getZone call')
        resp = requests.get(self.endpoint + domain, headers=self.authinfo)
        if resp.status_code != 200:
            respJson = resp.json()
            raise errors.PluginError(
                "EuroDNS API Error during _getZone: {0}".format(respJson['errors'][0]['title'])
            )

        logger.debug('getZone ok')
        #logger.debug(json.dumps(resp.json()))
        return resp.json()

    def _prepZone(self, domain, zone):
        logger.debug('prepZone call')
        #logger.debug(json.dumps(zone))
        resp = requests.post(self.endpoint + domain + '/check', json.dumps(zone), headers=self.authinfo)

        if resp.status_code != 200:
            respJson = resp.json()
            raise errors.PluginError(
                "EuroDNS API Error during _prepZone: {0}".format(respJson['errors'][0]['title'])
            )

        logger.debug('prepZone ok')
        #logger.debug(json.dumps(resp.json()))
        return resp.json()

    def _setZone(self, domain, zone):
        logger.debug('_setZone call')
        #logger.debug(json.dumps(zone))
        resp = requests.put(self.endpoint + domain, json.dumps(zone), headers=self.authinfo)

        if resp.status_code != 204:
            respJson = resp.json()
            raise errors.PluginError(
                "EuroDNS API Error during _setZone {0}".format(respJson['errors'][0]['title'])
            )
        logger.debug('setZone ok')

    def _getHost(self, domain, validation_name):
        host = re.sub(r"{0}$".format(domain), "", validation_name)
        return re.sub(r"\.$", "", host)