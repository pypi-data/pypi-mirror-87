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
# Copyright (c) 2013-2019 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Example Satellite Situation Center (SSC) web services client.
https://sscweb.gsfc.nasa.gov/WebServices/REST/.

Copyright &copy; 2013-2020 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import sys
import getopt
import json
import xml.etree.ElementTree as ET
import logging
import logging.config
from typing import Dict, List
import urllib3

#import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D  # pylint: disable=unused-import
import matplotlib.pyplot as plt

from sscws.sscws import SscWs
from sscws.bfieldmodels import BFieldModel, Tsyganenko89cBFieldModel
from sscws.coordinates import CoordinateComponent, CoordinateSystem
from sscws.filteroptions import LocationFilterOptions,\
    MappedRegionFilterOptions, RegionFilterOptions,\
    SpaceRegionsFilterOptions
from sscws.formatoptions import CdfFormatOptions
from sscws.outputoptions import CoordinateOptions, BFieldTraceOptions,\
    DistanceFromOptions, LocationFilter, OutputOptions, RegionOptions,\
    ValueOptions
from sscws.regions import Hemisphere, HemisphereRegions
from sscws.request import DataRequest, SatelliteSpecification
from sscws.timeinterval import TimeInterval


logging.basicConfig()
LOGGING_CONFIG_FILE = 'logging_config.json'
try:
    with open(LOGGING_CONFIG_FILE, 'r') as fd:
        logging.config.dictConfig(json.load(fd))
except BaseException as exc:    # pylint: disable=broad-except
    if not isinstance(exc, FileNotFoundError):
        print('Logging configuration failed')
        print('Exception: ', exc)
        print('Ignoring failure')
        print()


#ENDPOINT = "https://sscweb.sci.gsfc.nasa.gov/WS/sscr/2/"
ENDPOINT = "http://sscweb-dev.sci.gsfc.nasa.gov/WS/sscr/2/"
#ENDPOINT = "http://localhost:8383/WS/sscr/2/"
#CA_CERTS = '/etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt'


def print_usage(
        name: str
    ) -> None:
    """
    Prints program usage information to stdout.

    Parameters
    ----------
    name
        name of this program

    Returns
    -------
    None
    """
    print('USAGE: {name} [-e url][-d][-c cacerts][-h]'.format(name=name))
    print('WHERE: url = SSC web service endpoint URL')
    print('       -d disables TLS server certificate validation')
    print('       cacerts = CA certificate filename')


# pylint: disable=too-many-locals,too-many-branches
def example(
        argv: List[str]
    ) -> None:
    """
    Example Coordinate Data Analysis System (CDAS) web service client.
    Includes example calls to most of the web services.

    Parameters
    ----------
    argv
        Command-line arguments.<br>
        -e url or --endpoint=url where url is the cdas web service endpoint
            URL to use.<br>
        -c url or --cacerts=filename where filename is the name of the file
            containing the CA certificates to use.<br>
        -d or --disable-cert-check to disable verification of the server's
            certificate
        -h or --help prints help information.
    """

    try:
        opts = getopt.getopt(argv[1:], 'he:c:d',
                             ['help', 'endpoint=', 'cacerts=',
                              'disable-cert-check'])[0]
    except getopt.GetoptError:
        print('ERROR: invalid option')
        print_usage(argv[0])
        sys.exit(2)

    endpoint = ENDPOINT
    ca_certs = None
    disable_ssl_certificate_validation = False

    for opt, arg in opts:
        if opt in ('-e', '--endpoint'):
            endpoint = arg
        elif opt in ('-c', '--cacerts'):
            ca_certs = arg
        elif opt in ('-d', '--disable-cert-check'):
            disable_ssl_certificate_validation = True
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        elif opt in ('-h', '--help'):
            print_usage(argv[0])
            sys.exit()

    ssc = SscWs(endpoint=endpoint, ca_certs=ca_certs,
                disable_ssl_certificate_validation=
                disable_ssl_certificate_validation)

#    print('SSC Observatories:')
#    for observatory in ssc.get_observatories():
#
#        # this needs to be prettier
#        print(observatory['Id'], observatory['Name'],
#              observatory['StartTime'])
#
#    print('SSC Ground Stations:')
#    for ground_station in ssc.get_ground_stations():
#
#        location = ground_station['Location']
#
#        # this needs to be prettier
#        print(ground_station['Id'], ground_station['Name'],
#              location['Latitude'], location['Longitude'])

    # A simple request.
    result, status = ssc.get_locations(['iss'],
                                       ['2020-01-01T00:00:00Z',
                                        '2020-01-01T01:00:00Z'])
    print(result)
    if status == 200:

        figure = plt.figure()
        axis = figure.gca(projection='3d')
        data = result['Data'][0]
        coords = data['Coordinates']
        title = data['Id'] + ' Orbit (' + \
            coords['CoordinateSystem'].value.upper() + ')'
        axis.plot(coords['X'], coords['Y'], coords['Z'], label=title)
        axis.legend()
        plt.show()
        print_locations_result(result)
    else:
        print('ssc.get_locations failed with status = ', status)
    #return

    # A complex request.
    example_request = create_example_request()
    #print('request:')
    #print(ET.tostring(example_request.xml_element()).decode('utf-8'))
    result, status = ssc.get_locations(example_request)

    if status == 200:

        print_locations_result(result)
    else:
        print('ssc.get_locations failed with status = ', status)
        print('request:')
        print(ET.tostring(example_request.xml_element()).decode('utf-8'))
# pylint: enable=too-many-locals,too-many-branches


def create_example_request(
    ) -> ET:
    """
    Create an example DataRequest.

    Returns
    -------
    ET
        ElementTree representation of an example DataRequest.
    """
    sats = [SatelliteSpecification('themisa', 2),
            SatelliteSpecification('themisb', 2)]
    b_field_model = BFieldModel(external=Tsyganenko89cBFieldModel())
    coord_options = [
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.X),
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.Y),
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.Z),
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.LAT),
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.LON),
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.LOCAL_TIME)
        ]
    b_field_trace_options = [
        BFieldTraceOptions(CoordinateSystem.GEO, Hemisphere.NORTH,
                           True, True, True),
        BFieldTraceOptions(CoordinateSystem.GEO, Hemisphere.SOUTH,
                           True, True, True)
        ]

    output_options = OutputOptions(
        coord_options,
        None, None,
        RegionOptions(True, True, True, True),
        ValueOptions(True, True, True, True),
        DistanceFromOptions(True, True, True, True),
        b_field_trace_options
        )
    loc_filter = LocationFilter(0, 100000, True, True)
    loc_filter_options = LocationFilterOptions(True, loc_filter,
                                               loc_filter, loc_filter,
                                               loc_filter, loc_filter,
                                               loc_filter, loc_filter)

    hemisphere_region = HemisphereRegions(True, True)
    trace_regions = MappedRegionFilterOptions(hemisphere_region,
                                              hemisphere_region,
                                              hemisphere_region,
                                              hemisphere_region,
                                              hemisphere_region,
                                              True)
    srfo = SpaceRegionsFilterOptions(True, True, True, True, True, True,
                                     True, True, True, True, True)

    rfo = RegionFilterOptions(srfo, trace_regions, trace_regions)

    format_options = CdfFormatOptions()
    #format_options = None

    loc_request = DataRequest('Example locator request.',
                              TimeInterval('2020-10-02T00:00:00Z',
                                           '2020-10-02T01:00:00Z'),
                              sats, b_field_model,
                              output_options, rfo,
                              None, format_options)
#                              loc_filter_options)
    return loc_request


def print_files_result(
        result: Dict):
    """
    Prints a Result containing files names document.

    Parameters
    ----------
    result
        Dict representation of Result as described
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    for file in result['Files']:
        print(file['Name'])


# pylint: disable=too-many-branches
def print_locations_result(
        result: Dict) -> None:
    """
    Prints a Result document.

    Parameters
    ----------
    result
        Dict representation of Result as described
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """

    #print('StatusCode:', result['StatusCode'],
    #      'StatusSubCode:', result['StatusSubCode'])
    #print(result)

    if 'Files' in result:
        print_files_result(result)
        return

    for data in result['Data']:
        if 'Coordinates' not in data:
            continue
        coords = data['Coordinates']
        print(data['Id'], coords['CoordinateSystem'].value)
        print('Time                     ', 'X                     ',
              'Y                     ', 'Z                     ')
        for index in range(min(len(data['Time']), len(coords['X']))):
            print(data['Time'][index], coords['X'][index],
                  coords['Y'][index], coords['Z'][index])

        for b_trace in data['BTraceData']:

            print(b_trace['CoordinateSystem'].value,
                  b_trace['Hemisphere'].value)
            print('Time                          ', 'Latitude        ',
                  'Longitude   ', 'Arc Length')
            for index in range(min(len(data['Time']),
                                   len(b_trace['Latitude']))):
                print(data['Time'][index],
                      '{:15.5f} {:15.5f} {:15.5f}'.format(\
                          b_trace['Latitude'][index],
                          b_trace['Longitude'][index],
                          b_trace['ArcLength'][index]))

        quantities = ['RadialLength', 'MagneticStrength',
                      'NeutralSheetDistance', 'BowShockDistance',
                      'MagnetoPauseDistance', 'DipoleLValue',
                      'DipoleInvariantLatitude', 'SpacecraftRegion',
                      'RadialTracedFootpointRegions']
        #quantities = ['RadialLength']

        for quantity in quantities:
            print_time_series(quantity, data)

        if 'BGseX' in data:

            min_len = min(len(data['Time']), len(data['BGseX']))
            if min_len > 0:
                print('Time                     ', 'B Strength GSE        ')
                print('                             X                     ',
                      'Y                     ', 'Z')
                for index in range(min_len):
                    print(data['Time'][index], data['BGseX'][index],
                          data['BGseY'][index],
                          data['BGseZ'][index])

        if 'NorthBTracedFootpointRegion' in data and \
           'SouthBTracedFootpointRegion' in data:

            min_len = min(len(data['Time']),
                          len(data['NorthBTracedFootpointRegion']))
            if min_len > 0:
                print('                 B-Traced Footpoint Region')
                print('Time                     ', 'North            ',
                      'South           ')
                for index in range(min_len):
                    print(data['Time'][index],
                          data['NorthBTracedFootpointRegion'][index].value,
                          data['SouthBTracedFootpointRegion'][index].value)
# pylint: enable=too-many-branches


def print_time_series(
        name: str,
        data: Dict
    ) -> None:
    """
    Prints the given time-series data.

    Parameters
    ----------
    name
        Name (key) of data to print.
    data
        Dict containing the values to print.
    """

    if name in data:
        min_len = min(len(data['Time']), len(data[name]))
        if min_len > 0:
            print('Time                     ', name)
            for index in range(min_len):
                print(data['Time'][index], data[name][index])


if __name__ == '__main__':
    example(sys.argv)
