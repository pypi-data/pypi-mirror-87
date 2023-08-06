from .helpers import generate_attribute_string

class Device():
    """Represent Device config."""

    def __init__(self, raw, request):
        self._raw = raw
        self._request = request

    def __str__(self):
        attributes = ["product_name", "product_type", "serial", "api_version", "firmware_version"]
        return generate_attribute_string(self, attributes)

    def __eq__(self, other: object) -> bool:
        return self._raw == other._raw

    @property
    def product_name(self):
        """Friendly name of the device."""
        return self._raw['product_name']

    @property
    def product_type(self):
        """Device Type identifier."""
        return self._raw['product_type']

    @property
    def serial(self):
        """hex string of the 6 byte / 12 characters device id without delimiters."""
        return self._raw['serial']

    @property
    def api_version(self):
        """API version of the device."""
        return self._raw['api_version']

    @property
    def firmware_version(self):
        """User readable version of the device firmware, starting with decimal major .minor format e.g. 2.03"""
        return self._raw['firmware_version']

    async def update(self):
        response = await self._request('get', 'api')
        if response:
            self._raw = response