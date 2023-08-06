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
Module defining classes to represent the Result class and its
sub-classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2020 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List
from abc import ABCMeta, abstractmethod
from enum import Enum
import dateutil.parser

from sscws.coordinates import CoordinateSystem
from sscws.regions import Hemisphere, SpaceRegion


class ResultStatusCode(Enum):
    """
    Enumerations representing the ResultStatusCode defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    SUCCESS = 'Success'
    CONDITIONAL_SUCCESS = 'ConditionalSuccess'
    ERROR = 'Error'


class ResultStatusSubCode(Enum):
    """
    Enumerations representing the ResultStatusSubCode defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    SUCCESS = 'Success'
    MISSING_REQUEST = 'MissingRequest'
    MISSING_SATELLITES = 'MissingSatellites'
    INVALID_BEGIN_TIME = 'InvalidBeginTime'
    INVALID_END_TIME = 'InvalidEndTime'
    INVALID_SATELLITE = 'InvalidSatellite'
    INVALID_TIME_RANGE = 'InvalidTimeRange'
    INVALID_RESOLUTION_FACTOR = 'InvalidResolutionFactor'
    MISSING_OUTPUT_OPTIONS = 'MissingOutputOptions'
    MISSING_COORD_OPTIONS = 'MissingCoordOptions'
    MISSING_COORD_SYSTEM = 'MissingCoordSystem'
    INVALID_COORD_SYSTEM = 'InvalidCoordSystem'
    MISSING_COORD_COMPONENT = 'MissingCoordComponent'
    MISSING_GRAPH_OPTIONS = 'MissingGraphOptions'
    MISSING_COORDINATE_SYSTEM = 'MissingCoordinateSystem'
    MISSING_COORDINATE_COMPONENT = 'MissingCoordinateComponent'
    SERVER_ERROR = 'ServerError'


class Result(metaclass=ABCMeta):
    """
    Class representing a Result from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Notes
    -----
    Although this class is essentially a dictionary, it was defined as a
    class to make certain that it matched the structure and key names
    of a Request from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    It also needs to function as a base class for the concrete
    sub-classes of a Request.

    Properties
    ----------
    status_code
        Result status code.
    status_sub_code
        Result status sub-code.
    status_text
        Result status text.
    """
    @abstractmethod
    def __init__(
            self,
            status_code: ResultStatusCode,
            status_sub_code: ResultStatusSubCode,
            status_text: List[str]):
        """
        Creates an object representing a Result from
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Parameters
        ----------
        status_code
            Result status code value.
        status_sub_code
            Result status subcode value.
        status_text
            Status text.
        """
        self._status_code = status_code
        self._status_sub_code = status_sub_code
        self._status_text = status_text


    @property
    def status_code(self):
        """
        Gets the status_code value.

        Returns
        -------
        str
            status_code value.
        """
        return self._status_code


    @status_code.setter
    def status_code(self, value):
        """
        Sets the status_code value.

        Parameters
        ----------
        value
            status_code value.
        """
        self._status_code = value



    @property
    def status_sub_code(self):
        """
        Gets the status_sub_code value.

        Returns
        -------
        str
            status_sub_code value.
        """
        return self._status_sub_code


    @status_sub_code.setter
    def status_sub_code(self, value):
        """
        Sets the status_sub_code value.

        Parameters
        ----------
        value
            status_sub_code value.
        """
        self._status_sub_code = value



    @property
    def status_text(self):
        """
        Gets the status_text value.

        Returns
        -------
        str
            status_text value.
        """
        return self._status_text


    @status_text.setter
    def status_text(self, value):
        """
        Sets the status_text value.

        Parameters
        ----------
        value
            status_text value.
        """
        self._status_text = value


    @staticmethod
    def get_result(
            result_element: ET
        ) -> Dict:
        """
        Produces a Result from the given xml representation of a Result.

        Parameters
        ----------
        result_element
            ElementTree representation of a Result from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Returns
        -------
        Dict
            Dict representation of the given ElementTree Result
            as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Raises
        ------
        ValueError
            If the given xml is not a valid XML representation of Result.
        """

        result_type = result_element.get(\
            '{http://www.w3.org/2001/XMLSchema-instance}type')

        if result_type == 'DataResult':
            return Result.get_data_result(result_element)

        if result_type == 'FileResult':
            return Result.get_file_result(result_element)

        raise ValueError('Unrecognized Result type = ' + result_type)


    @staticmethod
    def get_status(
            result_element: ET
        ) -> Dict:
        """
        Produces a Dict representation of a Result with the StatusCode and
        SubStatusCode values from the given xml representation of a Result.

        Parameters
        ----------
        result_element
            ElementTree representation of a Result from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Returns
        -------
        Dict
            Dict representation of the given ElementTree Result
            as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            containing the StatusCode and SubStatusCode values.

        Raises
        ------
        ValueError
            If the given xml is not a valid XML representation of a
            DataResult.
        """

        # should these be string or enum values ???
        return {
            'StatusCode': result_element.find(\
                   '{http://sscweb.gsfc.nasa.gov/schema}StatusCode').text,
            'StatusSubCode': result_element.find(\
                   '{http://sscweb.gsfc.nasa.gov/schema}StatusSubCode').text
        }


    # pylint: disable=too-many-locals,too-many-branches
    @staticmethod
    def get_data_result(
            data_result_element: ET
        ) -> Dict:
        """
        Produces a Dict representation of a DataResult from the given
        xml representation of a DataResult.

        Parameters
        ----------
        data_result_element
            ElementTree representation of a DataResult from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Returns
        -------
        Dict
            Dict representation of the given ElementTree DataResult
            as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Raises
        ------
        ValueError
            If the given xml is not a valid XML representation of a
            DataResult.
        """

        result = Result.get_status(data_result_element)
        result['Data'] = []

        data_i = -1

        for data_element in data_result_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}Data'):

            data_i += 1

            coords_element = data_element.find(\
                   '{http://sscweb.gsfc.nasa.gov/schema}Coordinates')

            if coords_element is None:
                # Is this the correct result for this case???
                result['Data'].append({
                    'Id': data_element.find(\
                              '{http://sscweb.gsfc.nasa.gov/schema}Id').text
                })
                continue

            coordinates = {
                'CoordinateSystem': CoordinateSystem(coords_element.find(\
                   '{http://sscweb.gsfc.nasa.gov/schema}CoordinateSystem').text),
                'X': [],
                'Y': [],
                'Z': [],
                'Latitude': [],
                'Longitude': [],
                'LocalTime': []
            }
            result['Data'].append({
                'Id': data_element.find(\
                          '{http://sscweb.gsfc.nasa.gov/schema}Id').text,
                'Coordinates': coordinates,
                'Time': [],
                'BTraceData': [],
                'RadialLength': [],
                'MagneticStrength': [],
                'NeutralSheetDistance': [],
                'BowShockDistance': [],
                'MagnetoPauseDistance': [],
                'DipoleLValue': [],
                'DipoleInvariantLatitude': [],
                'SpacecraftRegion': [],
                'RadialTracedFootpointRegions': [],
                'BGseX': [],
                'BGseY': [],
                'BGseZ': [],
                'NorthBTracedFootpointRegions': [],
                'SouthBTracedFootpointRegions': []
            })

            for x_coord in coords_element.findall(\
                    '{http://sscweb.gsfc.nasa.gov/schema}X'):

                result['Data'][data_i]['Coordinates']['X'].append(\
                    float(x_coord.text))

            for y_coord in coords_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}Y'):

                result['Data'][data_i]['Coordinates']['Y'].append(\
                    float(y_coord.text))

            for z_coord in coords_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}Z'):

                result['Data'][data_i]['Coordinates']['Z'].append(\
                    float(z_coord.text))

            for lat_coord in coords_element.findall(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Latitude'):

                result['Data'][data_i]['Coordinates']['Latitude'].append(\
                    float(lat_coord.text))

            for lon_coord in coords_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}Longitude'):

                result['Data'][data_i]['Coordinates']['Longitude'].append(\
                    float(lon_coord.text))

            for lt_coord in coords_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}LocalTime'):

                result['Data'][data_i]['Coordinates']['LocalTime'].append(\
                    float(lt_coord.text))

            for time in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}Time'):

                result['Data'][data_i]['Time'].append(\
                    dateutil.parser.parse(time.text))

            for b_trace_data in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}BTraceData'):

                result['Data'][data_i]['BTraceData'].append({
                    'CoordinateSystem': CoordinateSystem(b_trace_data.find(\
                         '{http://sscweb.gsfc.nasa.gov/schema}CoordinateSystem').text),
                    'Hemisphere': Hemisphere(b_trace_data.find(\
                         '{http://sscweb.gsfc.nasa.gov/schema}Hemisphere').text),
                    'Latitude': [],
                    'Longitude': [],
                    'ArcLength': []
                })
                for lat in b_trace_data.findall(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Latitude'):

                    result['Data'][data_i]['BTraceData'][-1]['Latitude'].append(\
                        float(lat.text))

                for lon in b_trace_data.findall(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Longitude'):

                    result['Data'][data_i]['BTraceData'][-1]['Longitude'].append(\
                        float(lon.text))

                for arc_length in b_trace_data.findall(\
                    '{http://sscweb.gsfc.nasa.gov/schema}ArcLength'):

                    result['Data'][data_i]['BTraceData'][-1]['ArcLength'].append(\
                         float(arc_length.text))

            for radial_length in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}RadialLength'):

                result['Data'][data_i]['RadialLength'].append(\
                    float(radial_length.text))

            for magnetic_strength in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}MagneticStrength'):

                result['Data'][data_i]['MagneticStrength'].append(\
                    float(magnetic_strength.text))

            for neutral_sheet_distance in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}NeutralSheetDistance'):

                result['Data'][data_i]['NeutralSheetDistance'].append(\
                    float(neutral_sheet_distance.text))

            for bow_shock_distance in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}BowShockDistance'):

                result['Data'][data_i]['BowShockDistance'].append(\
                    float(bow_shock_distance.text))

            for magneto_pause_distance in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}MagnetoPauseDistance'):

                result['Data'][data_i]['MagnetoPauseDistance'].append(\
                    float(magneto_pause_distance.text))

            for dipole_l_value in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}DipoleLValue'):

                result['Data'][data_i]['DipoleLValue'].append(\
                    float(dipole_l_value.text))

            for dipole_invariant_latitude in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}DipoleInvariantLatitude'):

                result['Data'][data_i]['DipoleInvariantLatitude'].append(\
                    float(dipole_invariant_latitude.text))

            for spacecraft_region in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}SpacecraftRegion'):

                result['Data'][data_i]['SpacecraftRegion'].append(\
                    SpaceRegion(spacecraft_region.text))

        return result
    # pylint: enable=too-many-locals,too-many-branches


    @staticmethod
    def get_file_result(
            file_result_element: ET
        ) -> Dict:
        """
        Produces a Dict representation of a FileResult from the given
        xml representation of a FileResult.

        Parameters
        ----------
        file_result_element
            ElementTree representation of a FileResult from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Returns
        -------
        Dict
            Dict representation of the given ElementTree FileResult
            as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Raises
        ------
        ValueError
            If the given xml is not a valid XML representation of a
            FileResult.
        """

        result = Result.get_status(file_result_element)
        result['Files'] = []

        for file_description in file_result_element.findall(\
                '{http://sscweb.gsfc.nasa.gov/schema}Files'):
            result['Files'].append({
                'Name': file_description.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Name').text,
                'MimeType': file_description.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}MimeType').text,
                'Length': int(file_description.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Length').text),
                'LastModified': dateutil.parser.parse(\
                    file_description.find(\
                        '{http://sscweb.gsfc.nasa.gov/schema}LastModified').text)
            })
        return result


#
# If I continue to return Dict instead of class objects, then the rest of
# this file can be deleted.
#
class FileDescription:
    """
    Class representing a FileDescription from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Properties
    ----------
    name
        Name of file (usually a URL).
    mime_type
        MIME type of file.
    length
        Length of file in bytes.
    last_modified
        Time when file was last modified.
    """
    def __init__(
            self,
            name: str,
            mime_type: str,
            length: int,
            last_modified: datetime):
        """
        Creates a FileDescription object.

        Parameters
        ----------
        name
            Name of file (usually a URL).
        mime_type
            MIME type of file.
        length
            Length of file in bytes.
        last_modified
            Time when file was last modified.
        """
        self._name = name
        self._mime_type = mime_type
        self._length = length
        self._last_modified = last_modified

    @property
    def name(self):
        """
        Gets the name value.

        Returns
        -------
        str
            name value.
        """
        return self._name


    @name.setter
    def name(self, value):
        """
        Sets the name value.

        Parameters
        ----------
        value
            name value.
        """
        self._name = value


    @property
    def mime_type(self):
        """
        Gets the mime_type value.

        Returns
        -------
        str
            mime_type value.
        """
        return self._mime_type


    @mime_type.setter
    def mime_type(self, value):
        """
        Sets the mime_type value.

        Parameters
        ----------
        value
            mime_type value.
        """
        self._mime_type = value


    @property
    def length(self):
        """
        Gets the length value.

        Returns
        -------
        str
            length value.
        """
        return self._length


    @length.setter
    def length(self, value):
        """
        Sets the length value.

        Parameters
        ----------
        value
            length value.
        """
        self._length = value


    @property
    def last_modified(self):
        """
        Gets the last_modified value.

        Returns
        -------
        str
            last_modified value.
        """
        return self._last_modified


    @last_modified.setter
    def last_modified(self, value):
        """
        Sets the last_modified value.

        Parameters
        ----------
        value
            last_modified value.
        """
        self._last_modified = value


class FileResult(Result):
    """
    Class representing a FileResult from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Properties
    ----------
    files
        References to the files containing the requested data.
    """
    def __init__(
            self,
            status_code: ResultStatusCode,
            status_sub_code: ResultStatusSubCode,
            status_text: List[str],
            files: List[FileDescription]):
        """
        Creates an object representing a FileResult from
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Parameters
        ----------
        status_code
            Result status code value.
        status_sub_code
            Result status subcode value.
        status_text
            Status text.
        files
            List of files.
        """
        super().__init__(status_code, status_sub_code, status_text)
        self._files = files


    @property
    def files(self):
        """
        Gets the files value.

        Returns
        -------
        str
            files value.
        """
        return self._files


    @files.setter
    def files(self, value):
        """
        Sets the files value.

        Parameters
        ----------
        value
            files value.
        """
        self._files = value

#class CoordinateData:
#class BTraceData:
#class SatelliteData:
#class DataResult(Result):
#
