from .helpers import generate_attribute_string

class Data():
    """Represent Device config."""

    def __init__(self, raw, request):
        self._raw = raw
        self._request = request

    def __str__(self):
        attributes = ["smr_version",
                      "wifi_ssid",
                      "wifi_strength",
                      "total_power_import_t1_kwh",
                      "total_power_import_t2_kwh",
                      "total_power_export_t1_kwh",
                      "total_power_export_t2_kwh",
                      "active_power_w",
                      "active_power_l1_w",
                      "active_power_l2_w",
                      "active_power_l3_w",
                      "total_gas_m3",
                      "gas_timestamp"]
                      
        return generate_attribute_string(self, attributes)

    def __eq__(self, other: object) -> bool:
        return self._raw == other._raw

    @property
    def smr_version(self):
        """
        SMR version of P1 meter
        Available for: HWE-P1
        """
        return self._raw['smr_version'] if 'smr_version' in self._raw else None
    
    @property
    def wifi_ssid(self):
        """
        Wi-fi SSID currently in use (string)
        Available for: HWE-P1, SDM230-wifi, SDM630-wifi
        """
        return self._raw['wifi_ssid'] if 'wifi_ssid' in self._raw else None
    
    @property
    def wifi_strength(self):
        """
        Wifi strength in percentage (number, 0-100), where 100 is best
        Available for: HWE-P1, SDM230-wifi, SDM630-wifi
        """
        return self._raw['wifi_strength'] if 'wifi_strength' in self._raw else None
    
    @property
    def total_power_import_t1_kwh(self):
        """
        Total power import value for counter 1 (number)
        Available for: HWE-P1, SDM230-wifi, SDM630-wifi
        """
        return self._raw['total_power_import_t1_kwh'] if 'total_power_import_t1_kwh' in self._raw else None
    
    @property
    def total_power_import_t2_kwh(self):
        """
        Total power import value for counter 2 (number)
        Available for: HWE-P1
        """
        return self._raw['total_power_import_t2_kwh'] if 'total_power_import_t2_kwh' in self._raw else None
    
    @property
    def total_power_export_t1_kwh(self):
        """
        Total power export value for counter 1 (number)
        Available for: HWE-P1, SDM230-wifi, SDM630-wifi
        """
        return self._raw['total_power_export_t1_kwh'] if 'total_power_export_t1_kwh' in self._raw else None
    
    @property
    def total_power_export_t2_kwh(self):
        """
        Total power export value for counter 2 (number)
        Available for: HWE-P1
        """
        return self._raw['total_power_export_t2_kwh'] if 'total_power_export_t2_kwh' in self._raw else None
    
    @property
    def active_power_w(self):
        """
        Active consumption in watts (number)
        Available for: HWE-P1, SDM230-wifi, SDM630-wifi
        """
        return self._raw['active_power_w'] if 'active_power_w' in self._raw else None
    
    @property
    def active_power_l1_w(self):
        """
        Active consumption in watts for line 1 (number)
        Available for: HWE-P1, SDM230-wifi, SDM630-wifi
        """
        return self._raw['active_power_l1_w'] if 'active_power_l1_w' in self._raw else None
    
    @property
    def active_power_l2_w(self):
        """
        Active consumption in watts for line 2 (number)
        Note: DSMR meters are available in single and three-phase variants. P1 meter supports both
              This data value will be 'None' when P1 meter is connected to single phase meter
        Available for: HWE-P1, SDM630-wifi
        """
        return self._raw['active_power_l2_w'] if 'active_power_l2_w' in self._raw else None
    
    @property
    def active_power_l3_w(self):
        """
        Active consumption in watts for line 3 (number)
        Note: DSMR meters are available in single and three-phase variants. P1 meter supports both
              This data value will be 'None' when P1 meter is connected to single phase meter
        Available for: HWE-P1, SDM630-wifi
        """
        return self._raw['active_power_l3_w'] if 'active_power_l3_w' in self._raw else None
    
    @property
    def total_gas_m3(self):
        """
        Total gas usage in m3 (number)
        Note: Not all DSMR meters are connected to a gas meter, so this value can be 'None'
        Available for: HWE-P1
        """
        return self._raw['total_gas_m3'] if 'total_gas_m3' in self._raw else None
    
    @property
    def gas_timestamp(self):
        """
        Latest gas timestamp (number)
        Note: Not all DSMR meters are connected to a gas meter, so this value can be 'None'
        Available for: HWE-P1
        """
        return self._raw['gas_timestamp'] if 'gas_timestamp' in self._raw else None

    async def update(self):
        response = await self._request('get', 'api/v1/data')
        if response:
            self._raw = response
