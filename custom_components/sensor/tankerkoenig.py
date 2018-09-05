"""
A component/platform which allows you to get fuel prices from tankerkoenig.

For more details about this component, please refer to the documentation at
https://github.com/panbachi/homeassistant-tankerkoenig
"""
import logging
from datetime import timedelta

from custom_components.tankerkoenig import TankerkoenigDevice, CONF_STATIONS

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['tankerkoenig']

SCAN_INTERVAL = timedelta(seconds=5)


def setup_platform(hass, config, add_entities, discovery_info=None):
    tankerkoenig_config = discovery_info

    sensors = []

    for station in tankerkoenig_config[CONF_STATIONS]:
        sensors.append(TankerkoenigSensor('E5', station, tankerkoenig_config))
        sensors.append(TankerkoenigSensor('E10', station, tankerkoenig_config))
        sensors.append(TankerkoenigSensor('Diesel', station, tankerkoenig_config))

    add_entities(sensors)


class TankerkoenigSensor(TankerkoenigDevice):
    """Implement an Tankerkoenig sensor for displaying fuel prices."""

    def __init__(self, fuel_type, station_config, config):
        """Initialize the sensor."""
        super().__init__(station_config, config)
        self._state = None
        self._fuel_type = fuel_type
        self._icon = 'mdi:gas-station'

    @property
    def name(self):
        """Return the name of the sensor."""
        return '{} {}'.format(self._name, self._fuel_type)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return '€'

    @property
    def icon(self):
        """Return the mdi icon of the sensor."""
        return self._icon

    def update(self):
        """Fetch new price from API."""
        self._state = self.api.get_inputs(self._id, self._fuel_type)
