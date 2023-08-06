=====
Usage
=====

To use ciscomobilityexpress in a project::

    from ciscomobilityexpress.ciscome import CiscoMobilityExpress
    controller = CiscoMobilityExpress('IP_OF_CONTROLLER', 'username', 'password')

    controller.get_associated_devices()
