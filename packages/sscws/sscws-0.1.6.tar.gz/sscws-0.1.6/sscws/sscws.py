#!/usr/bin/env python3

#
# NOSA HEADER START
#
# The contents of this file are subject to the terms of the NASA Open
# Source Agreement (NOSA), Version 1.3 only (the "Agreement").  You may
# not use this file except in compliance with the Agreement.
#
# You can obtain a copy of the agreement at
#   docs/NASA_Open_Source_Agreement_1.3.txt
# or
#   https://sscweb.gsfc.nasa.gov/WebServices/NASA_Open_Source_Agreement_1.3.txt.
#
# See the Agreement for the specific language governing permissions
# and limitations under the Agreement.
#
# When distributing Covered Code, include this NOSA HEADER in each
# file and include the Agreement file at
# docs/NASA_Open_Source_Agreement_1.3.txt.  If applicable, add the
# following below this NOSA HEADER, with the fields enclosed by
# brackets "[]" replaced with your own identifying information:
# Portions Copyright [yyyy] [name of copyright owner]
#
# NOSA HEADER END
#
# Copyright (c) 2013-2020 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Module for accessing the Satellite Situation Center (SSC) web services
https://sscweb.gsfc.nasa.gov/WebServices/REST/.
"""

import platform
import xml.etree.ElementTree as ET
import logging
from typing import Dict, List, Tuple, Union
import requests
import dateutil.parser

from sscws import __version__
from sscws.coordinates import CoordinateSystem, CoordinateComponent
from sscws.outputoptions import CoordinateOptions, OutputOptions
from sscws.request import DataRequest, SatelliteSpecification
from sscws.result import Result
from sscws.timeinterval import TimeInterval



class SscWs:
    """
    Class representing the web service interface to NASA's
    Satelite Situation Center (SSC) <https://sscweb.gsfc.nasa.gov/>.

    Notes
    -----
    The logger used by this class has the class' name (SscWs).  By default,
    it is configured with a NullHandler.  Users of this class may configure
    the logger to aid in diagnosing problems.

    This class is dependent upon xml.etree.ElementTree module which is
    vulnerable to an "exponential entity expansion" and "quadratic blowup
    entity expansion" XML attack.  However, this class only receives XML
    from the (trusted) SSC server so these attacks are not a threat.  See
    the xml.etree.ElementTree "XML vulnerabilities" documentation for
    more details
    <https://docs.python.org/3/library/xml.html#xml-vulnerabilities>.
    """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    def __init__(
            self,
            endpoint=None,
            timeout=None,
            proxy=None,
            ca_certs=None,
            disable_ssl_certificate_validation=False):
        """
        Creates an object representing the SSC web services.

        Parameters
        ----------
        endpoint
            URL of the SSC web service.  If None, the default is
            'https://sscweb.gsfc.nasa.gov/WS/sscr/2/'.
        timeout
            Number of seconds to wait for a response from the server.
        proxy
            HTTP proxy information.  For example,
            proxies = {
              'http': 'http://10.10.1.10:3128',
              'https': 'http://10.10.1.10:1080',
            }
            Proxy information can also be set with environment variables.
            For example,
            $ export HTTP_PROXY="http://10.10.1.10:3128"
            $ export HTTPS_PROXY="http://10.10.1.10:1080"
        ca_certs
            Path to certificate authority (CA) certificates that will
            override the default bundle.
        disable_ssl_certificate_validation
            Flag indicating whether to validate the SSL certificate.
        """

        self.logger = logging.getLogger(type(self).__name__)
        self.logger.addHandler(logging.NullHandler())

        self.retry_after_time = None

        self.logger.debug('endpoint = %s', endpoint)
        self.logger.debug('ca_certs = %s', ca_certs)
        self.logger.debug('disable_ssl_certificate_validation = %s',
                          disable_ssl_certificate_validation)

        if endpoint is None:
            self._endpoint = 'https://sscweb.gsfc.nasa.gov/WS/sscr/2/'
        else:
            self._endpoint = endpoint
        self._user_agent = 'sscws/' + __version__ + ' (' + \
            platform.python_implementation() + ' ' \
            + platform.python_version() + '; '+ platform.platform() + ')'
        self._request_headers = {
            'Content-Type' : 'application/xml',
            'Accept' : 'application/xml',
            'User-Agent' : self._user_agent
        }
        self._session = requests.Session()
        self._session.headers.update(self._request_headers)

        if ca_certs is not None:
            self._session.verify = ca_certs

        if disable_ssl_certificate_validation is True:
            self._session.verify = False

        if proxy is not None:
            self._proxy = proxy

        self._timeout = timeout

    # pylint: enable=too-many-arguments


    def __str__(self) -> str:
        """
        Produces a string representation of this object.

        Returns
        -------
        str
            A string representation of this object.
        """
        return 'SscWs(endpoint=' + self._endpoint + ', timeout=' + \
               str(self._timeout) + ')'


    def __del__(self):
        """
        Destructor.  Closes all network connections.
        """

        self.close()


    def close(self) -> None:
        """
        Closes any persistent network connections.  Generally, deleting
        this object is sufficient and calling this method is unnecessary.
        """
        self._session.close()


    def get_observatories(
            self
        ) -> Tuple[List[Dict], int]:
        """
        Gets a description of the available SSC observatories.

        Returns
        -------
        List
            An array of ObservatoryDescription dictionaries where the
            structure of the dictionary mirrors ObservatoryDescription in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        int
            HTTP status code (200 is successful).
        """
        url = self._endpoint + 'observatories'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return ([], response.status_code)

        observatory_response = ET.fromstring(response.text)

        observatories = []

        for observatory in observatory_response.findall(\
                '{http://sscweb.gsfc.nasa.gov/schema}Observatory'):

            observatories.append({
                'Id': observatory.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Id').text,
                'Name': observatory.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Name').text,
                'Resolution': int(observatory.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Resolution').text),
                'StartTime': dateutil.parser.parse(observatory.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}StartTime').text),
                'EndTime': dateutil.parser.parse(observatory.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}EndTime').text),
                'ResourceId': observatory.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}ResourceId').text
            })

        return (observatories, response.status_code)


    def get_ground_stations(
            self
        ) -> Tuple[List[Dict], int]:
        """
        Gets a description of the available SSC ground stations.

        Returns
        -------
        List
            An array of GroundStations dictionaries where the
            structure of the dictionary mirrors GroundStations in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        int
            HTTP status code (200 is successful).
        """
        url = self._endpoint + 'groundStations'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return ([], response.status_code)

        ground_station_response = ET.fromstring(response.text)

        ground_stations = []

        for ground_station in ground_station_response.findall(\
                '{http://sscweb.gsfc.nasa.gov/schema}GroundStation'):

            location = ground_station.find(\
                '{http://sscweb.gsfc.nasa.gov/schema}Location')
            latitude = float(location.find(\
                '{http://sscweb.gsfc.nasa.gov/schema}Latitude').text)
            longitude = float(location.find(\
                '{http://sscweb.gsfc.nasa.gov/schema}Longitude').text)

            ground_stations.append({
                'Id': ground_station.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Id').text,
                'Name': ground_station.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Name').text,
                'Location': {
                    'Latitude': latitude,
                    'Longitude': longitude
                }
            })

        return (ground_stations, response.status_code)


    def get_locations(
            self,
            param1: Union[List[str], DataRequest],
            time_range: Union[List[str], TimeInterval] = None,
            coords: List[CoordinateSystem] = None
        ) -> Tuple[Dict, int]:
        """
        Gets the specified locations.  Complex requests (requesting
        magnetic field model values) require a single DataRequest
        parameter.  Simple requests (for only x, y, z, lat, lon,
        local_time) require at least the first two paramters.

        Parameters
        ----------
        param1
            A locations DataRequest or a list of observatory identifier
            (returned by get_observatories).
        time_range
            A TimeInterval or two element array of ISO 8601 string
            values of the start and stop time of requested data.
        coords
            Array of CoordinateSystem values that location information
            is to be in.  If None, default is CoordinateSystem.GSE.
        Returns
        -------
        Dict
            Dictionary whose struture mirrors Result from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        int
            HTTP status code (200 is successful).
        Raises
        ------
        ValueError
            If param1 is not a DataRequest and time_range is missing or
            time_range does not contain valid values.
        """

        if isinstance(param1, DataRequest):
            request = param1
        else:
            sats = []
            for sat in param1:
                sats.append(SatelliteSpecification(sat, 1))

            if time_range is None:
                raise ValueError('time_range value is required when ' +
                                 '1st is not a DataRequest')

            if isinstance(time_range, list):
                time_interval = TimeInterval(time_range[0], time_range[1])
            else:
                time_interval = time_range

            if coords is None:
                coords = [CoordinateSystem.GSE]

            coord_options = []
            for coord in coords:
                coord_options.append(
                    CoordinateOptions(coord, CoordinateComponent.X))
                coord_options.append(
                    CoordinateOptions(coord, CoordinateComponent.Y))
                coord_options.append(
                    CoordinateOptions(coord, CoordinateComponent.Z))
                coord_options.append(
                    CoordinateOptions(coord, CoordinateComponent.LAT))
                coord_options.append(
                    CoordinateOptions(coord, CoordinateComponent.LON))
                coord_options.append(
                    CoordinateOptions(coord, CoordinateComponent.LOCAL_TIME))

            request = DataRequest(None, time_interval, sats, None,
                                  OutputOptions(coord_options), None, None)

        result, status = self.__get_locations(request)

        return (result, status)


    def __get_locations(
            self,
            request: DataRequest
        ) -> Tuple[Dict, int]:
        """
        Gets the given locations DataRequest.

        Parameters
        ----------
        request
            A locations DataRequest.
        Returns
        -------
        Dict
            Dictionary whose struture mirrors Result from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        int
            HTTP status code (200 is sucessful).
        """
        url = self._endpoint + 'locations'

        self.logger.debug('request url = %s', url)

        xml_data_request = request.xml_element()

        response = self._session.post(url,
                                      data=ET.tostring(xml_data_request),
                                      timeout=self._timeout)
        if response.status_code != 200:

            try:
                # requires version 3.9
                ET.indent(xml_data_request)
            except AttributeError:
                pass
            self.logger.debug('request XML = %s', ET.tostring(xml_data_request))

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return ({}, response.status_code)

        result_element = ET.fromstring(response.text).find(\
                             '{http://sscweb.gsfc.nasa.gov/schema}Result')

        return (self.__get_result(result_element), response.status_code)


    def __get_result(
            self,
            result_element: ET
        ) -> Dict:
        """
        Creates a dict representation of a DataResult from an ElementTree
        representation.

        Parameters
        ----------
        result_element
            ElementTree representation of a DataResult from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Returns
        -------
        Dict
            Dict representation of the given ElementTree DataResult
            as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        """

        try:
            # requires version 3.9
            ET.indent(result_element)
        except AttributeError:
            pass
        self.logger.debug('result_element XML = %s',
                          ET.tostring(result_element))

        return Result.get_result(result_element)
