# -*- coding: utf-8 -*-
#  _     _       _
# | |   (_)  _  (_)
# | |  _ _ _| |_ _  ____ _____
# | |_/ ) (_   _) |/ ___|____ |
# |  _ (| | | |_| ( (___/ ___ |
# |_| \_)_|  \__)_|\____)_____|
#
# kitica DevicePool API
# Created by    : Joshua Kim Rivera
# Date          : September 23 2020 15:16 UTC-8
# Company       : Spiralworks Technologies Inc.
#
from .service import Service
from webargs import fields, validate
from webargs.flaskparser import use_kwargs


class DeviceUtils(Service):
    """
    kitica Device Utilities Endpoint.

    ...

    Methods
    ----------
    post
        Handles the POST Requests.
        Adds new Device to the database.
    delete
        Handles the DELETE Requests.
        Accepts the deviceId as params to perform delete
        operation on the database.
    """

    args = {
        'deviceName': fields.String(requried=False),
        'platformName': fields.String(required=False,
                                      validate=validate.OneOf(Service.PLATFORMS)
                                      ),
        'server': fields.String(required=False,
                                validate=validate.OneOf(Service.CONFIG['hosts']['allowed'])
                                ),
        'port': fields.String(required=False),
        'udid': fields.String(required=False),
        'teamName': fields.String(required=False,
                                  validate=validate.OneOf(Service.CONFIG['teams'])
                                  ),
        'platformVersion': fields.String(required=False),
        'deviceId': fields.Int(required=False),
        'deviceType': fields.String(required=False,
                                    validate=validate.OneOf(Service.DEVICES_TYPES)
                                    ),
        'driverPath': fields.String(required=False),
        'status': fields.String(required=False,
                                validate=validate.OneOf(Service.STATUS)
                                ),
        'deleteKey': fields.String(required=False,
                                   validate=validate.OneOf(Service.CONFIG['admin'])
                                   )
    }

    @use_kwargs(args)
    def post(self,
             deviceName,
             server,
             port,
             udid,
             platformName=None,
             teamName=None,
             platformVersion=None,
             deviceType=None,
             driverPath=None
             ):
        """ Device Utils POST Request Handler.

        Handles POST Requests from /device/utils endpoint.

        Parameters
        ----------
        deviceName : str
            The name of the device.
        server : str
            The Appium server endpoint to which the device could be accessed.
        udid : str
            The Unique Device Identifier.
        platformName : str
            Device's platform name, should be one of the supported devices listed
            in the config.yaml. Defaults to Android if no value is provided.
        platformVersion : str
            The device's platform version.
        deviceType : str
            Indicates what is the type of device. Should be one of the device
            listed under the config.yaml.
            Defaults to Emulator when no value is provided.
        driverPath : str
            Indicates the PATH to where the device host would resolve the Chromedriver
            PATH. (Android Devices Only)

        Returns
        ----------
        data : str
            Returns the device data enrolled should the request be successful.
        """
        data = [deviceName,
                platformName,
                server,
                port,
                udid,
                teamName,
                platformVersion,
                deviceType,
                driverPath
                ]
        data = "\"" + "\",\"".join(data) + "\""
        query = \
            'INSERT INTO device (deviceName,platformName,server,port,udid,\
                teamName,platformVersion,deviceType,driverPath) '\
                     + 'VALUES ( ' + data + ')'
        self._update(query)
        return (str(deviceName) + " Enrolled.")

    @use_kwargs(args)
    def get(self, server):
        """Fetches all the devices affiliated with the server host.

        Host IP should be whitelisted in the config.yaml.
        """
        query = 'SELECT udid,server FROM device WHERE server IN(\"'\
            + str(server) + '\"' + ',"")'
        devices = self._fetch(query)
        if devices is not None:
            return devices
        return None

    @use_kwargs(args)
    def patch(self,
              udid,
              server,
              status,
              driverPath
              ):
        """Updates the specified device's server by udid.
        """
        device = self.get_device_by_udid(udid)
        if device is not None:
            self._set_device_server(udid,
                                    server,
                                    driverPath,
                                    status
                                    )
            return "Device's Server Update Successful."
        else:
            return "ERROR:No Device with such udid found in the pool."

    @use_kwargs(args)
    def delete(self, deviceId, deleteKey):
        """ Device Utils DELETE Request Handler.

        Handles DELETE Requests from /device/utils endpoint.

        Parameters
        ----------
        deviceId : str
            The device's Id given by the database.
        """
        deviceName = self.get_device_name(deviceId)
        self._update('DELETE FROM device WHERE deviceId=' + str(deviceId))
        return "Device " + deviceName + " has been deleted."
