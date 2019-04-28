"""
Get the latest headline and breaking news from VRT NWS.

For more details about this platform, please refer to the documentation at
https://github.com/thibmaek/custom-components/
"""

import logging
from datetime import timedelta

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

__version__ = '1.0.3'

EXCLUDE_ITEMS = [
    "LIVE : Het Journaal 1", "Het Journaal Laat",
    "LIVE : Het Journaal met VGT", "Het Journaal 1",
    "De markt", "Het weer", "Villa Politica", "Terzake"
]
ATTRIBUTION = "Data provided by https://www.vrt.be/vrtnws/nl/"

DEFAULT_ICON = 'mdi:newspaper'
CONF_UPDATE_INTERVAL = 'update_interval'

REQUIREMENTS = ['xmltodict==0.11.0', 'requests_xml==0.2.3']

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    # TODO: should be scan interval from HA core
    vol.Optional(CONF_UPDATE_INTERVAL, default=timedelta(seconds=180)): (
        vol.All(cv.time_period, cv.positive_timedelta)),
})


async def async_setup_platform(hass, config,
                               async_add_entities, discovery_info=None):
    from requests_xml import XMLSession
    session = XMLSession()

    interval = config.get(CONF_UPDATE_INTERVAL)

    async_add_entities([
        VRTNWSFeedSensor(session, interval),
        VRTNWSBreakingSensor(session)
    ], True)


class VRTNWSBreakingSensor(Entity):
    """Create the VRT NWS breaking news sensor."""

    def __init__(self, session):
        """Set up the sensor."""
        self._session = session
        self._state = None
        self._data = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return "VRT NWS (Breaking)"

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return DEFAULT_ICON

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        if self._data is None:
            return {
                ATTR_ATTRIBUTION: ATTRIBUTION,
            }

        return {
            "details": self._data['summary'].get('#text'),
            ATTR_ATTRIBUTION: "Data provided by https://www.vrt.be/vrtnws/nl/",
        }

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    def update(self):
        """Set the state equal to the latest breaking headline."""
        import xmltodict

        response = self._session.get(
            'https://www.vrt.be/vrtnws/nl.rss.breaking.xml')
        if response.xml is None:
            return _LOGGER.error("No data recevied from RSS feed")

        entries = xmltodict.parse(response.xml.xml).get('feed').get('entry')

        if entries is None:
            self._state = None
            self._data = None
        else:
            self._data = entries[0]
            self._state = entries[0]["summary"].get("#text")


class VRTNWSFeedSensor(Entity):
    """Create the VRT NWS headline sensor."""

    def __init__(self, session, interval):
        """Set up the headline sensor."""
        self._session = session
        self._state = None
        self._data = {}
        # TODO: decorate with throttle instead
        self.update = Throttle(interval)(self._update)

    @property
    def name(self):
        """Return the name of the sensor."""
        return "VRT NWS"

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return DEFAULT_ICON

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        if self._data is None:
            return {
                ATTR_ATTRIBUTION: ATTRIBUTION,
            }

        return {
            "details": self._data['summary'].get('#text'),
            "last_update": self._data['updated'],
            "link": self._data['id'],
            "picture": self.get_picture_url(self._data['link']),
            "published": self._data['published'],
            "tag": self._data['vrtns:nstag'].get('#text'),
            ATTR_ATTRIBUTION: "Data provided by https://www.vrt.be/vrtnws/nl/",
        }

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    def get_picture_url(self, links_dict):
        """Get the entry's picture from the links dictionary."""
        pic = list(filter(lambda x: (x['@type'] == "image/jpeg"), links_dict))
        return pic[0].get("@href")

    def _update(self):
        """Set the state equal to the latest headline, with some exclusions."""
        import xmltodict

        response = self._session.get(
            'https://www.vrt.be/vrtnws/nl.rss.articles.xml')
        if response.xml is None:
            return _LOGGER.error("No data recevied from RSS feed")

        entries = xmltodict.parse(response.xml.xml).get('feed').get('entry')
        title = entries[0]["title"].get("#text")

        # Don't include this in the state because it appears too often and is
        # not interesting
        if title in EXCLUDE_ITEMS:
            return

        self._data = entries[0]
        self._state = title
