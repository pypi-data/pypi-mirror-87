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
Module defining classes to represent the Request and its
sub-classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2020 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import xml.etree.ElementTree as ET
from typing import List

from sscws.coordinates import CoordinateSystem, CoordinateComponent
from sscws.regions import Hemisphere


class CoordinateOptions:
    """
    Class representing a CoordinateOptions from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Properties
    ----------
    coordinate_system
        Coordinate system.
    component
        Coordinate system component.
    """
    def __init__(self,
                 coordinate_system: CoordinateSystem,
                 component: CoordinateComponent):
        """
        Creates an object representing a CoordinateOptions from
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Parameters
        ----------
        coordinate_system
            Coordinate system.
        component
            Coordinate system component.
        """
        self._coordinate_system = coordinate_system
        self._component = component


    @property
    def coordinate_system(self):
        """
        Gets the coordinate_system value.

        Returns
        -------
        str
            coordinate_system value.
        """
        return self._coordinate_system


    @coordinate_system.setter
    def coordinate_system(self, value):
        """
        Sets the coordinate_system value.

        Parameters
        ----------
        value
            coordinate_system value.
        """
        self._coordinate_system = value


    @property
    def component(self):
        """
        Gets the component value.

        Returns
        -------
        str
            component value.
        """
        return self._component


    @component.setter
    def component(self, value):
        """
        Sets the component value.

        Parameters
        ----------
        value
            component value.
        """
        self._component = value


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        builder = ET.TreeBuilder()

        builder.start('CoordinateOptions', {})
        builder.start('CoordinateSystem', {})
        builder.data(self._coordinate_system.value)
        builder.end('CoordinateSystem')
        builder.start('Component', {})
        builder.data(self._component.value)
        builder.end('Component')
        builder.end('CoordinateOptions')

        return builder.close()


class LocationFilter:
    """
    Class representing a LocationFilter from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Properties
    ----------
    minimum
        Specifies whether the minimum value is to be marked by a "v"
        in the listing.
    maximum
        Specifies whether the maximum value is to be marked by a "v"
        in the listing.
    lower_limit
        Specifies the lower limit of values that are to be included in
        the listing.  The value is kilometer or degrees as applicable.
    upper_limit
        Specifies the upper limit of values that are to be included in
        the listing.  The value is kilometer or degrees as applicable.
    """
    def __init__(self,
                 lower_limit: float,
                 upper_limit: float,
                 minimum: bool = None,
                 maximum: bool = None):
        """
        Creates an object representing a LocationFilter from
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Parameters
        ----------
        minimum
            Specifies whether the minimum value is to be marked by a "v"
            in the listing.  If None, default is False.
        maximum
            Specifies whether the maximum value is to be marked by a "v"
            in the listing.  If None, default is False.
        lower_limit
            Specifies the lower limit of values that are to be included in
            the listing.  The value is kilometer or degrees as applicable.
        upper_limit
            Specifies the upper limit of values that are to be included in
            the listing.  The value is kilometer or degrees as applicable.
        """

        if minimum is None:
            self._minimum = False
        else:
            self._minimum = minimum

        if maximum is None:
            self._maximum = False
        else:
            self._maximum = maximum

        self._lower_limit = lower_limit
        self._upper_limit = upper_limit


    @property
    def minimum(self):
        """
        Gets the minimum value.

        Returns
        -------
        str
            minimum value.
        """
        return self._minimum


    @minimum.setter
    def minimum(self, value):
        """
        Sets the minimum value.

        Parameters
        ----------
        value
            minimum value.
        """
        self._minimum = value


    @property
    def maximum(self):
        """
        Gets the maximum value.

        Returns
        -------
        str
            maximum value.
        """
        return self._maximum


    @maximum.setter
    def maximum(self, value):
        """
        Sets the maximum value.

        Parameters
        ----------
        value
            maximum value.
        """
        self._maximum = value


    @property
    def lower_limit(self):
        """
        Gets the lower_limit value.

        Returns
        -------
        str
            lower_limit value.
        """
        return self._lower_limit


    @lower_limit.setter
    def lower_limit(self, value):
        """
        Sets the lower_limit value.

        Parameters
        ----------
        value
            lower_limit value.
        """
        self._lower_limit = value


    @property
    def upper_limit(self):
        """
        Gets the upper_limit value.

        Returns
        -------
        str
            upper_limit value.
        """
        return self._upper_limit


    @upper_limit.setter
    def upper_limit(self, value):
        """
        Sets the upper_limit value.

        Parameters
        ----------
        value
            upper_limit value.
        """
        self._upper_limit = value


    def xml_element(self,
                    name: str) -> ET:
        """
        Produces the XML Element representation of this object.

        Parameters
        ----------
        name
            Name of this LocationFilter.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        builder = ET.TreeBuilder()

        builder.start(name, {})
        builder.start('Minimum', {})
        builder.data(str(self._minimum).lower())
        builder.end('Minimum')
        builder.start('Maximum', {})
        builder.data(str(self._maximum).lower())
        builder.end('Maximum')
        builder.start('LowerLimit', {})
        builder.data(str(self._lower_limit))
        builder.end('LowerLimit')
        builder.start('UpperLimit', {})
        builder.data(str(self._upper_limit))
        builder.end('UpperLimit')
        builder.end(name)

        return builder.close()


class FilteredCoordinateOptions(CoordinateOptions):
    """
    Class representing a FilteredCoordinateOptions from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Properties
    ----------
    location_filter
        Filter criteria.
    """
    def __init__(self,
                 coordinate_system: CoordinateSystem,
                 component: CoordinateComponent,
                 location_filter: LocationFilter = None):
        """
        Creates an object representing a FilteredCoordinateOptions from
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Parameters
        ----------
        coordinate_system
            Coordinate system.
        component
            Coordinate system component.
        location_filter
            Location filter listing options.
        """

        super().__init__(coordinate_system, component)
        self._location_filter = location_filter


    @property
    def location_filter(self):
        """
        Gets the location_filter value.

        Returns
        -------
        str
            location_filter value.
        """
        return self._location_filter


    @location_filter.setter
    def location_filter(self, value):
        """
        Sets the location_filter value.

        Parameters
        ----------
        value
            location_filter value.
        """
        self._location_filter = value


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        xml_element = super().xml_element()

        if self._location_filter is not None:
            xml_element.append(self._location_filter.xml_element())

        return xml_element


class RegionOptions:
    """
    Class representing a RegionOptions from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Properties
    ----------
    spacecraft
        Specifies whether the spacecraft regions are to be included
        in the listing.
    radial_traced_footpoint
        Specifies whether the radial traced footpoint values are to be
        included in the listing.
    north_b_traced_footpoint
        Specifies the north B-field traced footpoint values that are to be
        included in the listing.
    south_b_traced_footpoint
        Specifies the south B-field traced footpoint values that are to be
        included in the listing.
    """
    def __init__(self,
                 spacecraft: bool = None,
                 radial_traced_footpoint: bool = None,
                 north_b_traced_footpoint: bool = None,
                 south_b_traced_footpoint: bool = None):
        """
        Creates an object representing a RegionOptions from
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Parameters
        ----------
        spacecraft
            Specifies whether the spacecraft regions are to be included
            in the listing.  If None, default is False.
        radial_traced_footpoint
            Specifies whether the radial traced footpoint values are to be
            included in the listing.  If None, default is False.
        north_b_traced_footpoint
            Specifies the north B-field traced footpoint values that are
            to be included in the listing.  If None, default is False.
        south_b_traced_footpoint
            Specifies the south B-field traced footpoint values that are
            to be included in the listing.  If None, default is False.
        """

        if spacecraft is None:
            self._spacecraft = False
        else:
            self._spacecraft = spacecraft

        if radial_traced_footpoint is None:
            self._radial_traced_footpoint = False
        else:
            self._radial_traced_footpoint = radial_traced_footpoint

        if north_b_traced_footpoint is None:
            self._north_b_traced_footpoint = False
        else:
            self._north_b_traced_footpoint = north_b_traced_footpoint

        if south_b_traced_footpoint is None:
            self._south_b_traced_footpoint = False
        else:
            self._south_b_traced_footpoint = south_b_traced_footpoint


    @property
    def spacecraft(self):
        """
        Gets the spacecraft value.

        Returns
        -------
        str
            spacecraft value.
        """
        return self._spacecraft


    @spacecraft.setter
    def spacecraft(self, value):
        """
        Sets the spacecraft value.

        Parameters
        ----------
        value
            spacecraft value.
        """
        self._spacecraft = value


    @property
    def radial_traced_footpoint(self):
        """
        Gets the radial_traced_footpoint value.

        Returns
        -------
        str
            radial_traced_footpoint value.
        """
        return self._radial_traced_footpoint


    @radial_traced_footpoint.setter
    def radial_traced_footpoint(self, value):
        """
        Sets the radial_traced_footpoint value.

        Parameters
        ----------
        value
            radial_traced_footpoint value.
        """
        self._radial_traced_footpoint = value


    @property
    def north_b_traced_footpoint(self):
        """
        Gets the north_b_traced_footpoint value.

        Returns
        -------
        str
            north_b_traced_footpoint value.
        """
        return self._north_b_traced_footpoint


    @north_b_traced_footpoint.setter
    def north_b_traced_footpoint(self, value):
        """
        Sets the north_b_traced_footpoint value.

        Parameters
        ----------
        value
            north_b_traced_footpoint value.
        """
        self._north_b_traced_footpoint = value


    @property
    def south_b_traced_footpoint(self):
        """
        Gets the south_b_traced_footpoint value.

        Returns
        -------
        str
            south_b_traced_footpoint value.
        """
        return self._south_b_traced_footpoint


    @south_b_traced_footpoint.setter
    def south_b_traced_footpoint(self, value):
        """
        Sets the south_b_traced_footpoint value.

        Parameters
        ----------
        value
            south_b_traced_footpoint value.
        """
        self._south_b_traced_footpoint = value


    def xml_element(
            self
        ) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        builder = ET.TreeBuilder()

        builder.start('RegionOptions', {})
        builder.start('Spacecraft', {})
        builder.data(str(self._spacecraft).lower())
        builder.end('Spacecraft')
        builder.start('RadialTracedFootpoint', {})
        builder.data(str(self._radial_traced_footpoint).lower())
        builder.end('RadialTracedFootpoint')
        builder.start('NorthBTracedFootpoint', {})
        builder.data(str(self._north_b_traced_footpoint).lower())
        builder.end('NorthBTracedFootpoint')
        builder.start('SouthBTracedFootpoint', {})
        builder.data(str(self._south_b_traced_footpoint).lower())
        builder.end('SouthBTracedFootpoint')
        builder.end('RegionOptions')

        return builder.close()


class ValueOptions:
    """
    Class representing a ValueOptions from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Properties
    ----------
    radial_distance
        Specifies whether the radial distance is to be included
        in the listing.
    b_field_strength
        Specifies whether the B field strength values are to be
        included in the listing.
    dipole_l_value
        Specifies whether the dipole L values that are to be
        included in the listing.
    dipole_inv_lat
        Specifies whether the dipole invariant latitude values that
        are to be included in the listing.
    """
    def __init__(self,
                 radial_distance: bool = None,
                 b_field_strength: bool = None,
                 dipole_l_value: bool = None,
                 dipole_inv_lat: bool = None):
        """
        Creates an object representing a ValueOptions from
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Parameters
        ----------
        radial_distance
            Specifies whether the radial distance values are to be included
            in the listing.  If None, default is False.
        b_field_strength
            Specifies whether the B field strength values are to be
            included in the listing.  If None, default is False.
        dipole_l_value
            Specifies whether the dipole L values that are
            to be included in the listing.  If None, default is False.
        dipole_inv_lat
            Specifies whether the dipole invariant latitude values that
            are to be included in the listing.  If None, default is False.
        """

        if radial_distance is None:
            self._radial_distance = False
        else:
            self._radial_distance = radial_distance

        if b_field_strength is None:
            self._b_field_strength = False
        else:
            self._b_field_strength = b_field_strength

        if dipole_l_value is None:
            self._dipole_l_value = False
        else:
            self._dipole_l_value = dipole_l_value

        if dipole_inv_lat is None:
            self._dipole_inv_lat = False
        else:
            self._dipole_inv_lat = dipole_inv_lat


    @property
    def radial_distance(self):
        """
        Gets the radial_distance value.

        Returns
        -------
        str
            radial_distance value.
        """
        return self._radial_distance


    @radial_distance.setter
    def radial_distance(self, value):
        """
        Sets the radial_distance value.

        Parameters
        ----------
        value
            radial_distance value.
        """
        self._radial_distance = value


    @property
    def b_field_strength(self):
        """
        Gets the b_field_strength value.

        Returns
        -------
        str
            b_field_strength value.
        """
        return self._b_field_strength


    @b_field_strength.setter
    def b_field_strength(self, value):
        """
        Sets the b_field_strength value.

        Parameters
        ----------
        value
            b_field_strength value.
        """
        self._b_field_strength = value


    @property
    def dipole_l_value(self):
        """
        Gets the dipole_l_value value.

        Returns
        -------
        str
            dipole_l_value value.
        """
        return self._dipole_l_value


    @dipole_l_value.setter
    def dipole_l_value(self, value):
        """
        Sets the dipole_l_value value.

        Parameters
        ----------
        value
            dipole_l_value value.
        """
        self._dipole_l_value = value


    @property
    def dipole_inv_lat(self):
        """
        Gets the dipole_inv_lat value.

        Returns
        -------
        str
            dipole_inv_lat value.
        """
        return self._dipole_inv_lat


    @dipole_inv_lat.setter
    def dipole_inv_lat(self, value):
        """
        Sets the dipole_inv_lat value.

        Parameters
        ----------
        value
            dipole_inv_lat value.
        """
        self._dipole_inv_lat = value


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        builder = ET.TreeBuilder()

        builder.start('ValueOptions', {})
        builder.start('RadialDistance', {})
        builder.data(str(self._radial_distance).lower())
        builder.end('RadialDistance')
        builder.start('BFieldStrength', {})
        builder.data(str(self._b_field_strength).lower())
        builder.end('BFieldStrength')
        builder.start('DipoleLValue', {})
        builder.data(str(self._dipole_l_value).lower())
        builder.end('DipoleLValue')
        builder.start('DipoleInvLat', {})
        builder.data(str(self._dipole_inv_lat).lower())
        builder.end('DipoleInvLat')
        builder.end('ValueOptions')

        return builder.close()


class DistanceFromOptions:
    """
    Class representing a DistanceFromOptions from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Properties
    ----------
    neutral_sheet
        Specifies whether the distance to the neutral sheet values are
        to be included in the listing.
    bow_shock
        Specifies whether the distance to the bow shock values are to be
        included in the listing.
    m_pause
        Specifies whether the distance to the magneto pause values that
        are to be included in the listing.
    b_gse_xyz
        Specifies whether the magnetic field strength in the GSE XYZ
        directions that are to be included in the listing.
    """
    def __init__(self,
                 neutral_sheet: bool = None,
                 bow_shock: bool = None,
                 m_pause: bool = None,
                 b_gse_xyz: bool = None):
        """
        Creates an object representing a DistanceFromOptions from
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Parameters
        ----------
        neutral_sheet
            Specifies whether the distance to the neutral sheet values are
            to be included in the listing.  If None, default is False.
        bow_shock
            Specifies whether the distance to the bow shock values are to
            be included in the listing.  If None, default is False.
        m_pause
            Specifies whether the distance to the magneto pause values that
            are to be included in the listing.  If None, default is False.
        b_gse_xyz
            Specifies whether the magnetic field strength in the GSE XYZ
            directions that are to be included in the listing.  If None,
            default is False.
        """

        if neutral_sheet is None:
            self._neutral_sheet = False
        else:
            self._neutral_sheet = neutral_sheet

        if bow_shock is None:
            self._bow_shock = False
        else:
            self._bow_shock = bow_shock

        if m_pause is None:
            self._m_pause = False
        else:
            self._m_pause = m_pause

        if b_gse_xyz is None:
            self._b_gse_xyz = False
        else:
            self._b_gse_xyz = b_gse_xyz


    @property
    def neutral_sheet(self):
        """
        Gets the neutral_sheet value.

        Returns
        -------
        str
            neutral_sheet value.
        """
        return self._neutral_sheet


    @neutral_sheet.setter
    def neutral_sheet(self, value):
        """
        Sets the neutral_sheet value.

        Parameters
        ----------
        value
            neutral_sheet value.
        """
        self._neutral_sheet = value


    @property
    def bow_shock(self):
        """
        Gets the bow_shock value.

        Returns
        -------
        str
            bow_shock value.
        """
        return self._bow_shock


    @bow_shock.setter
    def bow_shock(self, value):
        """
        Sets the bow_shock value.

        Parameters
        ----------
        value
            bow_shock value.
        """
        self._bow_shock = value


    @property
    def m_pause(self):
        """
        Gets the m_pause value.

        Returns
        -------
        str
            m_pause value.
        """
        return self._m_pause


    @m_pause.setter
    def m_pause(self, value):
        """
        Sets the m_pause value.

        Parameters
        ----------
        value
            m_pause value.
        """
        self._m_pause = value


    @property
    def b_gse_xyz(self):
        """
        Gets the b_gse_xyz value.

        Returns
        -------
        str
            b_gse_xyz value.
        """
        return self._b_gse_xyz


    @b_gse_xyz.setter
    def b_gse_xyz(self, value):
        """
        Sets the b_gse_xyz value.

        Parameters
        ----------
        value
            b_gse_xyz value.
        """
        self._b_gse_xyz = value


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        builder = ET.TreeBuilder()

        builder.start('DistanceFromOptions', {})
        builder.start('NeutralSheet', {})
        builder.data(str(self._neutral_sheet).lower())
        builder.end('NeutralSheet')
        builder.start('BowShock', {})
        builder.data(str(self._bow_shock).lower())
        builder.end('BowShock')
        builder.start('MPause', {})
        builder.data(str(self._m_pause).lower())
        builder.end('MPause')
        builder.start('BGseXYZ', {})
        builder.data(str(self._b_gse_xyz).lower())
        builder.end('BGseXYZ')
        builder.end('DistanceFromOptions')

        return builder.close()


class BFieldTraceOptions:
    """
    Class representing a BFieldTraceOptions from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Properties
    ----------
    coordinate_system
        Specifies the coordinate system.
    hemisphere
        Specifies the hemisphere.
    footpoint_latitude
        Specifies whether to include footpoint latitude values in the
        listing.
    footpoint_longitude
        Specifies whether to include footpoint longitude values in the
        listing.
    field_line_length
        Specifies whether to include field line length values in the
        listing.
    """
    def __init__(self,
                 coordinate_system: bool = None,
                 hemisphere: Hemisphere = None,
                 footpoint_latitude: bool = None,
                 footpoint_longitude: bool = None,
                 field_line_length: bool = None
                 ):  # pylint: disable=too-many-arguments
        """
        Creates an object representing a BFieldTraceOptions from
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Parameters
        ----------
        coordinate_system
            Specifies the coordinate system.  If None, default is
            CoordinateSystem.GEO.
        hemisphere
            Specifies the hemisphere.  If None, default is Hemisphere.NORTH.
        footpoint_latitude
            Specifies whether to include footpoint latitude values in the
            listing.
        footpoint_longitude
            Specifies whether to include footpoint longitude values in the
            listing.
        field_line_length
            Specifies whether to include field line length values in the
            listing.
        """

        if coordinate_system is None:
            self._coordinate_system = CoordinateSystem.GEO
        else:
            self._coordinate_system = coordinate_system

        if hemisphere is None:
            self._hemisphere = Hemisphere.NORTH
        else:
            self._hemisphere = hemisphere

        if footpoint_latitude is None:
            self._footpoint_latitude = False
        else:
            self._footpoint_latitude = footpoint_latitude

        if footpoint_longitude is None:
            self._footpoint_longitude = False
        else:
            self._footpoint_longitude = footpoint_longitude

        if field_line_length is None:
            self._field_line_length = False
        else:
            self._field_line_length = field_line_length


    @property
    def coordinate_system(self):
        """
        Gets the coordinate_system value.

        Returns
        -------
        str
            coordinate_system value.
        """
        return self._coordinate_system


    @coordinate_system.setter
    def coordinate_system(self, value):
        """
        Sets the coordinate_system value.

        Parameters
        ----------
        value
            coordinate_system value.
        """
        self._coordinate_system = value


    @property
    def hemisphere(self):
        """
        Gets the hemisphere value.

        Returns
        -------
        str
            hemisphere value.
        """
        return self._hemisphere


    @hemisphere.setter
    def hemisphere(self, value):
        """
        Sets the hemisphere value.

        Parameters
        ----------
        value
            hemisphere value.
        """
        self._hemisphere = value


    @property
    def footpoint_latitude(self):
        """
        Gets the footpoint_latitude value.

        Returns
        -------
        str
            footpoint_latitude value.
        """
        return self._footpoint_latitude


    @footpoint_latitude.setter
    def footpoint_latitude(self, value):
        """
        Sets the footpoint_latitude value.

        Parameters
        ----------
        value
            footpoint_latitude value.
        """
        self._footpoint_latitude = value


    @property
    def footpoint_longitude(self):
        """
        Gets the footpoint_longitude value.

        Returns
        -------
        str
            footpoint_longitude value.
        """
        return self._footpoint_longitude


    @footpoint_longitude.setter
    def footpoint_longitude(self, value):
        """
        Sets the footpoint_longitude value.

        Parameters
        ----------
        value
            footpoint_longitude value.
        """
        self._footpoint_longitude = value


    @property
    def field_line_length(self):
        """
        Gets the field_line_length value.

        Returns
        -------
        str
            field_line_length value.
        """
        return self._field_line_length


    @field_line_length.setter
    def field_line_length(self, value):
        """
        Sets the field_line_length value.

        Parameters
        ----------
        value
            field_line_length value.
        """
        self._field_line_length = value


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        builder = ET.TreeBuilder()

        builder.start('BFieldTraceOptions', {})
        builder.start('CoordinateSystem', {})
        builder.data(self._coordinate_system.value)
        builder.end('CoordinateSystem')
        builder.start('Hemisphere', {})
        builder.data(self._hemisphere.value)
        builder.end('Hemisphere')
        builder.start('FootpointLatitude', {})
        builder.data(str(self._footpoint_latitude).lower())
        builder.end('FootpointLatitude')
        builder.start('FootpointLongitude', {})
        builder.data(str(self._footpoint_longitude).lower())
        builder.end('FootpointLongitude')
        builder.start('FieldLineLength', {})
        builder.data(str(self._field_line_length).lower())
        builder.end('FieldLineLength')
        builder.end('BFieldTraceOptions')

        return builder.close()


class OutputOptions:
    """
    Class representing a OutputOptions from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Properties
    ----------
    coordinate_options
        Coordinate options.
    all_location_filters
        All location filters flag.
    min_max_points
        Minimum/Maximum number of points.
    region_options
        Region options.
    value_options
        Value options.
    distance_from_options
        Distance-from options.
    b_field_trace_options
        B-field trace options.
    """
    def __init__(self,
                 coordinate_options: List[FilteredCoordinateOptions],
                 all_location_filters: bool = None,
                 min_max_points: int = None,
                 region_options: RegionOptions = None,
                 value_options: ValueOptions = None,
                 distance_from_options: DistanceFromOptions = None,
                 b_field_trace_options: List[BFieldTraceOptions] = None
                 ):  # pylint: disable=too-many-arguments
        """
        Creates an object representing a OutputOptions from
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Parameters
        ----------
        coordinate_options
            Coordinate options.
        all_location_filters
            All location filters flag.  If None, default is True.
        min_max_points
            Minimum/Maximum number of points.  If None, default is 2.
        region_options
            Region options.
        value_options
            Value options.
        distance_from_options
            Distance-from options.
        b_field_trace_options
            B-field trace options.
        """

        self._coordinate_options = coordinate_options
        if all_location_filters is None:
            self._all_location_filters = True
        else:
            self._all_location_filters = all_location_filters
        if min_max_points is None:
            self._min_max_points = 2
        else:
            self._min_max_points = min_max_points
        self._region_options = region_options
        self._value_options = value_options
        self._distance_from_options = distance_from_options

        if b_field_trace_options is None:
            self._b_field_trace_options = []
        else:
            self._b_field_trace_options = b_field_trace_options


    @property
    def coordinate_options(self):
        """
        Gets the coordinate_options value.

        Returns
        -------
        str
            coordinate_options value.
        """
        return self._coordinate_options


    @coordinate_options.setter
    def coordinate_options(self, value):
        """
        Sets the coordinate_options value.

        Parameters
        ----------
        value
            coordinate_options value.
        """
        self._coordinate_options = value


    @property
    def all_location_filters(self):
        """
        Gets the all_location_filters value.

        Returns
        -------
        str
            all_location_filters value.
        """
        return self._all_location_filters


    @all_location_filters.setter
    def all_location_filters(self, value):
        """
        Sets the all_location_filters value.

        Parameters
        ----------
        value
            all_location_filters value.
        """
        self._all_location_filters = value


    @property
    def min_max_points(self):
        """
        Gets the min_max_points value.

        Returns
        -------
        str
            min_max_points value.
        """
        return self._min_max_points


    @min_max_points.setter
    def min_max_points(self, value):
        """
        Sets the min_max_points value.

        Parameters
        ----------
        value
            min_max_points value.
        """
        self._min_max_points = value


    @property
    def region_options(self):
        """
        Gets the region_options value.

        Returns
        -------
        str
            region_options value.
        """
        return self._region_options


    @region_options.setter
    def region_options(self, value):
        """
        Sets the region_options value.

        Parameters
        ----------
        value
            region_options value.
        """
        self._region_options = value


    @property
    def value_options(self):
        """
        Gets the value_options value.

        Returns
        -------
        str
            value_options value.
        """
        return self._value_options


    @value_options.setter
    def value_options(self, value):
        """
        Sets the value_options value.

        Parameters
        ----------
        value
            value_options value.
        """
        self._value_options = value


    @property
    def distance_from_options(self):
        """
        Gets the distance_from_options value.

        Returns
        -------
        str
            distance_from_options value.
        """
        return self._distance_from_options


    @distance_from_options.setter
    def distance_from_options(self, value):
        """
        Sets the distance_from_options value.

        Parameters
        ----------
        value
            distance_from_options value.
        """
        self._distance_from_options = value


    @property
    def b_field_trace_options(self):
        """
        Gets the b_field_trace_options value.

        Returns
        -------
        str
            b_field_trace_options value.
        """
        return self._b_field_trace_options


    @b_field_trace_options.setter
    def b_field_trace_options(self, value):
        """
        Sets the b_field_trace_options value.

        Parameters
        ----------
        value
            b_field_trace_options value.
        """
        self._b_field_trace_options = value


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        builder = ET.TreeBuilder()
        builder.start('OutputOptions', {})
        builder.start('AllLocationFilters', {})
        builder.data(str(self._all_location_filters).lower())
        builder.end('AllLocationFilters')
        builder.start('MinMaxPoints', {})
        builder.data(str(self._min_max_points).lower())
        builder.end('MinMaxPoints')
        builder.end('OutputOptions')

        xml_element = builder.close()

        for coord_option in self._coordinate_options:
            xml_element.append(coord_option.xml_element())
        if self._region_options is not None:
            xml_element.append(self._region_options.xml_element())
        if self._value_options is not None:
            xml_element.append(self._value_options.xml_element())
        if self._distance_from_options is not None:
            xml_element.append(self._distance_from_options.xml_element())

        for b_trace_option in self._b_field_trace_options:
            xml_element.append(b_trace_option.xml_element())

        return xml_element
