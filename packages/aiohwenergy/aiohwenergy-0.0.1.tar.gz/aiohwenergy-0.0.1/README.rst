AIOHWENERGY
=============

Asyncio package to communicate with HomeWizard Energy devices
This package is aimed at basic control of the device. Initial setup and configuration is assumed to done with the official HomeWizard Energy app


Installation
============

.. code-block:: bash

    python3 -m pip install aiohwenergy


Usage
=====

Instantiate the HWEnergy class and access the API.

For more details on the API see the official API documentation on
https://energy.homewizard.net/en/support/solutions/articles/19000117051-homewizard-p1-meter-local-api-beta-

Example
=======

The example below is available as a runnable script in the repository.

from aiohwenergy import HomeWizardEnergy

.. code-block:: python
    
    # Make contact with a energy device
    device = HomeWizardEnergy(args.host)
    
    # Update device value
    await device.update()
    
    # Use the data
    print(device.device.product_name)
    print(device.device.serial)
    print(device.data.wifi_ssid)
    
    # Close connection
    await device.close()
    
Credits
=======
Thanks to @mvdwetering (https://github.com/mvdwetering/aiohuesyncbox) for having a good example ready for talking with a local API.