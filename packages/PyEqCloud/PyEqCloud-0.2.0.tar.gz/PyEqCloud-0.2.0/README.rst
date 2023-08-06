
PyEqCloud
============

PyEqCloud is a Python module for data extraction with the EquipmentCloud of Kontron AIS GmbH using a REST connection.
PyEqCloud is distributed under the MIT license.

The project was started in April 2020 by Patrick Thiem and Maik Pertermann.

It is currently maintained by Patrick Thiem and Maik Pertermann.




Installation
------------


Requirements
~~~~~~~~~~~~

To be able to run this package, beside the package dependencies, a valid EquipmentCloud account (or demo account) is needed.

For more information visit the official EquipmentCloud website: https://kontron-ais.com/produkte/iiot-service-plattform/eq-cloud/

Dependencies
~~~~~~~~~~~~

PyEqCloud requires following packages:

- Python (>= 3.6)
- pandas (>= 0.25.3)
- requests (>= 2.22.0)
- tqdm (>= 4.39.0)

These packages will automatically be installed by installing PyEqCloud.

**support of PyEqCloud package on Python version below 3.6 cannot be assured**


User installation
~~~~~~~~~~~~~~~~~

The easiest way to install PyEqCloud is using ``pip``   ::

    pip install PyEqCloud

An Anaconda package is not yet supported.


Important links
~~~~~~~~~~~~~~~

- Official source code repo: https://github.com/AISAutomation/PyEqCloud
- Download releases: https://pypi.org/project/PyEqCloud/


Source code
~~~~~~~~~~~

You can check the latest sources with the command::

    git clone https://github.com/AISAutomation/PyEqCloud.git


Help and Support
----------------

How to use PyEqCloud?
~~~~~~~~~~~~~

The following credential informations are needed to make REST requests:

- Username (registred Email-adress)
- Account password
- Customer ID (usually this ID is handed to the costumer via Email)
--> If the user is logged into a valid EquipmentCloud Account, the customer ID can also be found in the URL (bold number in example) 
example: https:// eqcloud.ais-automation.com/**C168170000**/f?p=60000:LOGIN

For more details, please download or view the prepared jupyter notebook in the folder "Jupyter".


Communication
~~~~~~~~~~~~~

- Email: Patrick.Thiem@kontron-ais.com and Maik.Pertermann@kontron-ais.com
