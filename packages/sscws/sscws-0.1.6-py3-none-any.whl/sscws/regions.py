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
Module defining classes to represent region classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2020 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import xml.etree.ElementTree as ET
from enum import Enum


class FootpointRegion(Enum):
    """
    Enumerations representing the FootpointRegion defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    NOT_APPLICABLE = 'NotApplicable'
    NORTH_CUSP = 'NorthCusp'
    SOUTH_CUSP = 'SouthCusp'
    NORTH_CLEFT = 'NorthCleft'
    SOUTH_CLEFT = 'SouthCleft'
    NORTH_AURORAL_OVAL = 'NorthAuroralOval'
    SOUTH_AURORAL_OVAL = 'SouthAuroralOval'
    NORTH_POLAR_CAP = 'NorthPolarCap'
    SOUTH_POLAR_CAP = 'SouthPolarCap'
    NORTH_MID_LATITUDE = 'NorthMidLatitude'
    SOUTH_MID_LATITUDE = 'SouthMidLatitude'
    LOW_LATITUDE = 'LowLatitude'


class Hemisphere(Enum):
    """
    Enumerations representing the Hemisphere defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    SOUTH = 'South'
    NORTH = 'North'


class HemisphereRegions:
    """
    Class representing a HemisphereRegions from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Properties
    ----------
    north
        Northern hemisphere region.
    south
        Southern hemisphere region.
    """
    def __init__(self,
                 north: bool,
                 south: bool):
        """
        Creates an object representing a HemisphereRegions from
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Parameters
        ----------
        north
            Northern hemisphere region.
        south
            Southern hemisphere region.
        """
        self._north = north
        self._south = south


    @property
    def north(self):
        """
        Gets the north value.

        Returns
        -------
        str
            north value.
        """
        return self._north


    @north.setter
    def north(self, value):
        """
        Sets the north value.

        Parameters
        ----------
        value
            north value.
        """
        self._north = value


    @property
    def south(self):
        """
        Gets the south value.

        Returns
        -------
        str
            south value.
        """
        return self._south


    @south.setter
    def south(self, value):
        """
        Sets the south value.

        Parameters
        ----------
        value
            south value.
        """
        self._south = value


    def xml_element(self,
                    name: str) -> ET:
        """
        Produces the XML Element representation of this object.

        Parameters
        ----------
        name
            Name of Region.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        builder = ET.TreeBuilder()

        builder.start(name, {})
        builder.start('North', {})
        builder.data(str(self._north).lower())
        builder.end('North')
        builder.start('South', {})
        builder.data(str(self._south).lower())
        builder.end('South')
        builder.end(name)

        return builder.close()


class SpaceRegion(Enum):
    """
    Enumerations representing the SpaceRegion defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    INTERPLANETARY_MEDIUM = 'InterplanetaryMedium'
    DAYSIDE_MAGNETOSHEATH = 'DaysideMagnetosheath'
    NIGHTSIDE_MAGNETOSHEATH = 'NightsideMagnetosheath'
    DAYSIDE_MAGNETOSPHERE = 'DaysideMagnetosphere'
    NIGHTSIDE_MAGNETOSPHERE = 'NightsideMagnetosphere'
    PLASMA_SHEET = 'PlasmaSheet'
    TAIL_LOBE = 'TailLobe'
    LOW_LATITUDE_BOUNDARY_LAYER = 'LowLatitudeBoundaryLayer'
    HIGH_LATITUDE_BOUNDARY_LAYER = 'HighLatitudeBoundarLayer'
    DAYSIDE_PLASMASPHERE = 'DaysidePlasmasphere'
    NIGHTSIDE_PLASMASPHERE = 'NightsidePlasmasphere'


class SpaceRegionType(Enum):
    """
    Enumerations representing the SpaceRegionType defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    INTERPLANETARY_MEDIUM = 'InterplanetaryMedium'
    DAYSIDE_MAGNETOSHEATH = 'DaysideMagnetosheath'
    NIGHTSIDE_MAGNETOSHEATH = 'NightsideMagnetosheath'
    DAYSIDE_MAGNETOSPHERE = 'DaysideMagnetosphere'
    NIGHTSIDE_MAGNETOSPHERE = 'NightsideMagnetosphere'
    PLASMA_SHEET = 'PlasmaSheet'
    TAIL_LOBE = 'TailLobe'
    LOW_LATITUDE_BOUNDARY_LAYER = 'LowLatitudeBoundaryLayer'
    HIGH_LATITUDE_BOUNDARY_LAYER = 'HighLatitudeBoundarLayer'
    DAYSIDE_PLASMASPHERE = 'DaysidePlasmasphere'
    NIGHTSIDE_PLASMASPHERE = 'NightsidePlasmasphere'
