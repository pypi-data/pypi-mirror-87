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
Module defining classes to represent tracing classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2020 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

from enum import Enum


class BFieldTraceDirection(Enum):
    """
    Enumerations representing the BFieldTraceDirection defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    SAME_HEMISPHERE = 'SameHemisphere'
    OPPOSITE_HEMISPHERE = 'OppositeHemisphere'
    NORTH_HEMISPHERE = 'NorthHemisphere'
    SOUTH_HEMISPHERE = 'SouthHemisphere'
    EITHER_HEMISPHERE = 'EitherHemisphere'


class TraceCoordinateSystem(Enum):
    """
    Enumerations representing the TraceCoordinateSystem defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    GEO = 'Geo'
    GM = 'Gm'


class TraceType(Enum):
    """
    Enumerations representing the TraceType defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    B_FIELD = 'BField'
    RADIAL = 'Radial'
