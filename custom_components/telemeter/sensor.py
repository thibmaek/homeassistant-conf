"""
Shows the amount of usage in your Telenet Telemeter.
"""
from datetime import timedelta
import logging

import requests
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

RESOURCE_URL = 'https://api.prd.telenet.be/ocapi/public/?p=internetusage'

SCAN_INTERVAL = timedelta(minutes=10)

DEFAULT_NAME = 'Telemeter'

CONF_COOKIE = 'cookie'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_COOKIE): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})


def get_telemeter_usage(response, headers):
    """Map and transform received JSON data from API to a dict."""
    try:
        usage_data = response["internetusage"][0]['availableperiods'][0]['usages'][0]

        spec_url = usage_data["specurl"]
        spec_request = requests.Request(
            "GET", spec_url, headers=headers).prepare()
        with requests.Session() as sess:
            spec_response = sess.send(spec_request, timeout=10)
        spec_data = spec_response.json()['product']['characteristics']
        limit = int(spec_data['service_category_limit']['value'])
        limit_unit = spec_data['service_category_limit']['unit']

        if limit_unit == 'MB':
            limit /= 1000
        elif limit_unit == 'TB':
            limit *= 1000

        usage_peak = int(usage_data['totalusage']['peak'])
        usage_offpeak = int(usage_data['totalusage']['offpeak'])

        return {
            'usage': ((usage_offpeak / 1E6) + (usage_peak / 1E6)),
            'limit': [limit, limit_unit],
            'last_updated': response['internetusage'][0]['lastupdated'],
            'subscription_type': usage_data['producttype'],
            'alert_threshold': int(spec_data['alert_threshold']['value'])
        }
    except requests.exceptions.RequestException:
        raise RuntimeError(
            "Connection timed out, possibly due to bad credentials")
    except KeyError as ex:
        _LOGGER.error('KeyError occured in get_telemeter_usage: %s', ex)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Telemeter sensor."""
    name = config.get(CONF_NAME)
    cookie = config[CONF_COOKIE]

    add_entities([TelemeterSensor(name, cookie)], True)


class TelemeterSensor(Entity):
    """Create the Telemeter sensor."""

    def __init__(self, name, cookie):
        self._name = name
        self._cookie = cookie
        self._state = None
        self._attrs = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        return round(self._state, 2)

    @property
    def device_state_attributes(self):
        """Return attributes for sensor."""
        if self._state is None or self._attrs is None:
            return None

        return {
            'max_usage': self._attrs['limit'][0],
            'last_updated': self._attrs['last_updated'],
            'used_percentage': self.percentage_used,
            'subscription_type': self._attrs['subscription_type'],
            'alert_threshold': self._attrs['alert_threshold']
        }

    @property
    def unit_of_measurement(self):
        """Return unit of measurement."""
        if self._state is None or self._attrs is None:
            return None

        return self._attrs['limit'][1]

    @property
    def percentage_used(self):
        """Return the usage in percentage."""
        max_usage = self._attrs['limit'][0]
        return round((self._state / max_usage) * 100, 2)

    def make_request(self):
        """Perform the API request to OCAPI (Telenet)"""
        headers = {'cookie': self._cookie}
        request = requests.Request(
            "GET", RESOURCE_URL, headers=headers).prepare()

        try:
            with requests.Session() as sess:
                response = sess.send(request, timeout=10)
            data = response.json()

            return get_telemeter_usage(data, headers)
        except requests.exceptions.RequestException as ex:
            _LOGGER.error("Error fetching data: %s from %s failed with %s",
                          request, request.url, ex)

    def update(self):
        """Update sensor state."""
        try:
            response = self.make_request()

            _LOGGER.debug(response)
            self._attrs = response
            self._state = response['usage']
        except KeyError as ex:
            _LOGGER.error('Could not retrieve usage data: %s', ex)
