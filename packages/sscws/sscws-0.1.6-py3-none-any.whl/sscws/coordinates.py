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
Module defining classes to represent the coordinate related classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2020 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

from enum import Enum


class CoordinateSystem(Enum):
    """
    Enumerations representing the CoordinateSystem type defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    GEO = 'Geo'
    GM = 'Gm'
    GSE = 'Gse'
    GSM = 'Gsm'
    SM = 'Sm'
    GEI_TOD = 'GeiTod'
    GEI_J_2000 = 'GeiJ2000'


class CoordinateSystemType(Enum):
    """
    Enumerations representing the CoordinateSystemType defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    SPHERICAL = 'Spherical'
    CARTESIAN = 'Cartesian'


class CoordinateComponent(Enum):
    """
    Enumerations representing the CoordinateComponent defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    X = 'X'
    Y = 'Y'
    Z = 'Z'
    LAT = 'Lat'
    LON = 'Lon'
    LOCAL_TIME = 'Local_Time'


class ProjectionCoordinateSystem(Enum):
    """
    Enumerations representing the ProjectionCoordinateSystem defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    GEO = 'Geo'
    GM = 'Gm'
    SM = 'Sm'
