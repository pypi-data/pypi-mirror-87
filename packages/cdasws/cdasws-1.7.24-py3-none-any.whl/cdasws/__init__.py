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
#   https://cdaweb.gsfc.nasa.gov/WebServices/NASA_Open_Source_Agreement_1.3.txt.
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
# Copyright (c) 2018-2020 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#


"""
Package for accessing the Coordinate Data Analysis System (CDAS)
web services <https://cdaweb.gsfc.nasa.gov/WebServices/REST/>.<br>

Copyright &copy; 2018-2020 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""


import sys
import os
import platform
import logging
import urllib.parse
from urllib.parse import urlparse
import json
from operator import itemgetter
import time
from datetime import datetime, timedelta, timezone
from tempfile import mkstemp
from typing import Any, Callable, Dict, List, Tuple, Union

import requests
import dateutil.parser

from cdasws.datarequest import AudioRequest, DataRequest
from cdasws.datarequest import CdfFormat, CdfRequest, Compression
from cdasws.datarequest import ImageFormat, GraphOptions, GraphRequest
from cdasws.datarequest import TextFormat, TextRequest, ThumbnailRequest
from cdasws.timeinterval import TimeInterval


__version__ = "1.7.24"



def _get_data_progress(
        progress: float,
        msg: str,
        value: Dict) -> int:
    """
    A get_data progress callback which adjusts the progress value for
    the download portion of a larger operation and then calls the
    "real" progress callback function with this adjusted progress value.

    Parameters
    ----------
    progress
        Measure of progress.
    msg
        Message describing progress of get_data call.
    value
        Dictionary containing the function to call and values for
        computing the adjusted progress value.
    Returns
    -------
    int
        Flag indicating whether to continue with getting the data.
        0 to continue. 1 to abort getting the data.
    """
    progress_callback = value.get('progressCallback', None)
    progress_user_value = value.get('progressUserValue', None)
    adjusted_progress = value['progressStart'] + \
                        value['progressFraction'] * progress

    if progress_callback is not None:

        return progress_callback(adjusted_progress, msg,
                                 progress_user_value)
    return 0


class CdasWs:
    """
    Class representing the web service interface to NASA's
    Coordinated Data Analysis System (CDAS)
    <https://cdaweb.gsfc.nasa.gov>.

    Notes
    -----
    The logger used by this class has the class' name (CdasWs).  By default,
    it is configured with a NullHandler.  Users of this class may configure
    the logger to aid in diagnosing problems.
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
        Creates an object representing the CDAS web services.

        Parameters
        ----------
        endpoint
            URL of the CDAS web service.  If None, the default is
            'https://cdaweb.gsfc.nasa.gov/WS/cdasr/1/dataviews/sp_phys/'.
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
            self._endpoint = 'https://cdaweb.gsfc.nasa.gov/WS/cdasr/1/dataviews/sp_phys/'
        else:
            self._endpoint = endpoint

        self._user_agent = 'cdasws/' + __version__ + ' (' + \
            platform.python_implementation() + ' ' \
            + platform.python_version() + '; ' + platform.platform() + ')'

        self._request_headers = {
            'Content-Type' : 'application/json',
            'Accept' : 'application/json',
            'User-Agent' : self._user_agent,
            #'Accept-Encoding' : 'gzip'  # only beneficial for icdfml responses
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


    def get_observatory_groups(
            self,
            **keywords: str
        ) -> List[Dict]:
        """
        Gets descriptions of the observatory groups from the server.

        Parameters
        ----------
        keywords
            instrumentType value.
        Returns
        -------
        List
            An array of ObservatoryGroupDescription
            dictionaries where the structure of the dictionary mirrors
            ObservatoryGroupDescription in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        if 'instrumentType' in keywords:
            url = self._endpoint + 'observatoryGroups?instrumentType=' + \
                      urllib.parse.quote(keywords['instrumentType'])
        else:
            url = self._endpoint + 'observatoryGroups'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        observatory_groups = response.json()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('observatory_groups: %s',
                              json.dumps(observatory_groups,
                                         indent=4, sort_keys=True))

        if not observatory_groups:
            return []

        return observatory_groups['ObservatoryGroupDescription']


    def get_instrument_types(
            self,
            **keywords: str
        ) -> List[Dict]:
        """
        Gets descriptions of the instrument types from the server.

        Parameters
        ----------
        keywords
            observatory or observatoryGroup value.
        Returns
        -------
        List
            An array of InstrumentTypeDescription
            dictionaries where the structure of the dictionary mirrors
            InstrumentTypeDescription in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        if 'observatory' in keywords:
            url = self._endpoint + 'instrumentTypes?observatory=' \
                  + urllib.parse.quote(keywords['observatory'])
        elif 'observatoryGroup' in keywords:
            url = self._endpoint + 'instrumentTypes?observatoryGroup=' \
                  + urllib.parse.quote(keywords['observatoryGroup'])
        else:
            url = self._endpoint + 'instrumentTypes'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        instrument_types = response.json()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('instrument_types = %s',
                              json.dumps(instrument_types, indent=4,
                                         sort_keys=True))

        if not instrument_types:
            return []

        return instrument_types['InstrumentTypeDescription']


    def get_instruments(
            self,
            **keywords: str
        ) -> List[Dict]:
        """
        Gets descriptions of the instruments from the server.

        Parameters
        ----------
        keywords
            observatory or instrumentType value.
        Returns
        -------
        List
            An array of InstrumentDescription
            dictionaries where the structure of the dictionary mirrors
            InstrumentDescription in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        if 'observatory' in keywords:
            url = self._endpoint + 'instruments?observatory=' \
                  + urllib.parse.quote(keywords['observatory'])
        elif 'instrumentType' in keywords:
            url = self._endpoint + 'instruments?instrumentType=' \
                  + urllib.parse.quote(keywords['instrumentType'])
        else:
            url = self._endpoint + 'instruments'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        instruments = response.json()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('instruments = %s',
                              json.dumps(instruments, indent=4,
                                         sort_keys=True))

        if not instruments:
            return []

        return instruments['InstrumentDescription']


    def get_observatories(
            self,
            **keywords: str
        ) -> List[Dict]:
        """
        Gets descriptions of the observatories from the server.

        Parameters
        ----------
        keywords
            instrument or instrumentType value.
        Returns
        -------
        List
            An array of ObservatoryDescriptions
            dictionaries where the structure of the dictionary mirrors
            ObservatoryDescription in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        if 'instrument' in keywords:
            url = self._endpoint + 'observatories?instrument=' \
                  + urllib.parse.quote(keywords['instrument'])
        elif 'instrumentType' in keywords:
            url = self._endpoint + 'observatories?instrumentType=' \
                  + urllib.parse.quote(keywords['instrumentType'])
        else:
            url = self._endpoint + 'observatories'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        observatories = response.json()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('observatories = %s',
                              json.dumps(observatories, indent=4,
                                         sort_keys=True))

        if not observatories:
            return []

        return observatories['ObservatoryDescription']


    def get_observatory_groups_and_instruments(
            self,
            **keywords: str
        ) -> List[Dict]:
        """
        Gets descriptions of the observatory groups (and associated
        instruments) from the server.

        Parameters
        ----------
        keywords
            instrumentType value.
        Returns
        -------
        List
            An array of ObservatoryGroupInstrumentDescription
            dictionaries where the structure of the dictionary mirrors
            ObservatoryGroupInstrumentDescription in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        if 'instrumentType' in keywords:
            url = self._endpoint \
                  + 'observatoryGroupsAndInstruments?instrumentType=' \
                  + urllib.parse.quote(keywords['instrumentType'])
        else:
            url = self._endpoint + 'observatoryGroupsAndInstruments'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        observatories = response.json()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('observatories = %s',
                              json.dumps(observatories, indent=4,
                                         sort_keys=True))

        if not observatories:
            return []

        return observatories['ObservatoryGroupInstrumentDescription']


    # pylint: disable=too-many-branches
    def get_datasets(
            self,
            **keywords: str
        ) -> List[Dict]:
        """
        Gets descriptions of the specified datasets from the server.

        Parameters
        ----------
        keywords
            observatoryGroup, instrumentType, observatory,
            instrument, startDate, stopDate, idPattern, labelPattern,
            and/or notesPattern value(s).
        Returns
        -------
        List
            A dictionary containing descriptions of the datasets
            requested.  The dictionary structure is defined by the
            DatasetDescription element in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        url = self._endpoint + 'datasets?'

        observatory_groups = keywords.get('observatoryGroup', None)
        if observatory_groups is not None:
            if isinstance(observatory_groups, str):
                observatory_groups = [observatory_groups]
            for observatory_group in observatory_groups:
                url = url + 'observatoryGroup=' \
                      + urllib.parse.quote(observatory_group) + '&'

        instrument_types = keywords.get('instrumentType', None)
        if instrument_types is not None:
            if isinstance(instrument_types, str):
                instrument_types = [instrument_types]
            for instrument_type in instrument_types:
                url = url + 'instrumentType=' \
                      + urllib.parse.quote(instrument_type) + '&'

        observatories = keywords.get('observatory', None)
        if observatories is not None:
            if isinstance(observatories, str):
                observatories = [observatories]
            for observatory in observatories:
                url = url + 'observatory=' \
                      + urllib.parse.quote(observatory) + '&'

        instruments = keywords.get('instrument', None)
        if instruments is not None:
            if isinstance(instruments, str):
                instruments = [instruments]
            for instrument in instruments:
                url = url + 'instrument=' \
                      + urllib.parse.quote(instrument) + '&'

        if 'startDate' in keywords:
            url = url + 'startDate=' \
                  + urllib.parse.quote(keywords['startDate']) + '&'

        if 'stopDate' in keywords:
            url = url + 'stopDate=' \
                  + urllib.parse.quote(keywords['stopDate']) + '&'

        if 'idPattern' in keywords:
            url = url + 'idPattern=' \
                  + urllib.parse.quote(keywords['idPattern']) + '&'

        if 'labelPattern' in keywords:
            url = url + 'labelPattern=' \
                  + urllib.parse.quote(keywords['labelPattern']) + '&'

        if 'notesPattern' in keywords:
            url = url + 'notesPattern=' \
                  + urllib.parse.quote(keywords['notesPattern']) + '&'

        self.logger.debug('request url = %s', url[:-1])

        response = self._session.get(url[:-1], timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        datasets = response.json()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('datasets = %s',
                              json.dumps(datasets, indent=4, sort_keys=True))

        if not datasets:
            return []

        return sorted(datasets['DatasetDescription'], key=itemgetter('Id'))
    # pylint: enable=too-many-branches


    def get_inventory(
            self,
            identifier: str,
            **keywords: str
        ) -> List[TimeInterval]:
        """
        Gets a description of the specified dataset's data inventory.

        Parameters
        ----------
        identifier
            dataset identifier of data inventory to get.
        keywords
            time interval value.
        Returns
        -------
        List
            An array of TimeIntervals when data is available.
        """

        url = self._endpoint + 'datasets/' + \
                  urllib.parse.quote(identifier, safe='') + '/inventory'

        if 'timeInterval' in keywords:
            time_interval_keyword = keywords['timeInterval']
            url = url + '/' + \
                  TimeInterval.basic_iso_format(time_interval_keyword.start) + \
                  ',' + \
                  TimeInterval.basic_iso_format(time_interval_keyword.end)

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        inventory = response.json()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('inventory = %s',
                              json.dumps(inventory, indent=4, sort_keys=True))

        intervals = []

        data_intervals = inventory['InventoryDescription'][0]

        if 'TimeInterval' in data_intervals:

            for time_interval in data_intervals['TimeInterval']:

                intervals.append(
                    TimeInterval(
                        time_interval['Start'],
                        time_interval['End']
                    )
                )

        return intervals


    def get_variables(
            self,
            identifier: str
        ) -> List[Dict]:
        """
        Gets a description of the variables in the specified dataset.

        Parameters
        ----------
        identifier
            dataset identifier of data to get.
        Returns
        -------
        List
            A List of dictionary descriptions of the variables in
            the specified dataset.  The dictionary structure is defined by
            the VariableDescription element in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """

        url = self._endpoint + 'datasets/' + \
                  urllib.parse.quote(identifier, safe='') + '/variables'

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        variables = response.json()

        if not variables:
            return []

        return variables['VariableDescription']


    def get_data_result(
            self,
            data_request: DataRequest,
            progress_callback: Callable[[float, str, Any], int],
            progress_user_value: Any
        ) -> Tuple[int, Dict]:
        """
        Submits the given request to the server and returns the result.
        This is a relatively low-level method and most callers should
        probably use a higher-level method such as get_data.

        Parameters
        ----------
        data_request
            data request.
        progress_callback
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns a non-0 value,
            getting the data will be aborted and the get_data() function
            will immediately return (204, None).  The float parameter
            is a value between 0.0 and 1.0 to indicate progress and
            the str parameter will contain a text message indicating
            the progress of this call.
        progressUserValue
            value that is passsed to the progressCallback function.
        Returns
        -------
        Tuple
            [0] contains the int HTTP status code.  200 when
            successful.<br>
            [1] contains a dictionary representing the DataResult from
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>
            or None.
        See Also
        --------
        get_data
        """

        self.logger.debug('data_request = %s', data_request.json())

        url = self._endpoint + 'datasets'

        if self.retry_after_time:

            sleep_time = (self.retry_after_time - \
                          datetime.now()).total_seconds()

            if progress_callback is not None:
                if progress_callback(0.2, 'Waiting ' + sleep_time + \
                                     's before making server request.',
                                     progress_user_value) != 0:
                    return (204, None)

            self.logger.info('Sleeping %d seconds before making request',
                             sleep_time)
            time.sleep(sleep_time)
            self.retry_after_time = None

        response = self._session.post(url, data=data_request.json(),
                                      timeout=self._timeout)

        try:
            data_result = response.json()
        except ValueError:
            # for example, a 503 from apache will not be json
            self.logger.debug('Non-JSON response: %s', response.text)

        if response.status_code != 200:

            if response.status_code == 503 and \
               'Retry-After' in response.headers:

                retry_after = response.headers['Retry-After']

                self.logger.debug('503 status with Retry-After header: %s',
                                  retry_after)

                self.retry_after_time = datetime.now() + \
                    timedelta(0, int(retry_after))

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('data_request = %s', data_request)
            self.logger.info('response.text: %s', response.text)
            return (response.status_code, None)

        if not data_result:
            return (response.status_code, None)

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('data_result = %s',
                              json.dumps(data_result, indent=4,
                                         sort_keys=True))

        return (response.status_code, data_result)


    def get_data_file(
            self,
            dataset: str,
            variables: List[str],
            start: Union[datetime, str], end: Union[datetime, str],
            **keywords: Union[
                Dict,
                Callable[[float, str, Any], int],
                Any]
        ) -> Tuple[int, Dict]:
        """
        Gets the specified data file from the server.

        Parameters
        ----------
        dataset
            dataset identifier of data to get.
        variables
            array containing names of variables to get.
        start
            start time of data to get.
        end
            end time of data to get.
        keywords
            optional keyword parameters as follows<br>
            binData - indicates that uniformly spaced values should be
            computed for scaler/vector/spectrogram data according to
            the given binning parameter values.  binData is a Dict that
            may contain the following keys: interval,
            interpolateMissingValues, sigmaMultiplier, and/or
            overrideDefaultBinning with values that override the defaults.<br>
            progressCallback - is a
            Callable[[float, str, typing.Any], int]
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns non-0 value,
            getting the data will be aborted and the get_data_file()
            function will immediately return (204, None).  The float
            parameter is a value between 0.0 and 1.0 to indicate progress
            and the str parameter will contain a text message indicating
            the progress of this call.<br>
            progressUserValue - is an Any value that is passsed
            to the progressCallback function.<br>
        Returns
        -------
        Tuple
            [0] contains the int HTTP status code.  200 when
            successful.<br>
            [1] contains a dictionary representing the DataResult from
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>
            or None.
        Raises
        ------
        ValueError
            If the given start/end datetime values are invalid.
        See Also
        --------
        get_data : In addition to what get_data_file does, get_data also
            downloads and reads the data file into memory (SpaceData
            object).
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-return-statements
        # pylint: enable=too-many-statements
        # pylint: disable=too-many-branches

        start_datetime, end_datetime = TimeInterval.get_datetimes(start,
                                                                  end)

        data_request = CdfRequest(dataset, variables,
                                  TimeInterval(start_datetime,
                                               end_datetime),
                                  3, CdfFormat.BINARY,
                                  **keywords.get('binData', {}))

        progress_callback = keywords.get('progressCallback', None)
        progress_user_value = keywords.get('progressUserValue', None)

        self.logger.debug('data_request = %s', data_request)

        if progress_callback is not None:
            if progress_callback(0.1, 'Making server request.',
                                 progress_user_value) != 0:
                return (204, None)

        status_code, data_result = self.get_data_result(data_request,
                                                        progress_callback,
                                                        progress_user_value)

        if progress_callback is not None:
            if progress_callback(1.0, 'Initial server request complete.',
                                 progress_user_value) != 0:
                return (status_code, None)

        return (status_code, data_result)


    def download(
            self,
            url: str,
            size: int = 0,
            **keywords
        ) -> str:
        """
        Downloads the file specified by the given URL to a temporary
        file without reading all of it into memory.  This method
        utilizes the connection pool and persistent HTTP connection
        to the CdasWs server.

        Parameters
        ----------
        url
            URL of file to download.
        size
            number of bytes in file to download.
        keywords
            optional keyword parameters as follows<br>
            progressCallback - is a
            typing.Callable[[float, str, typing.Any], int]
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns a non-0 value,
            getting the data will be aborted and this download() function
            will immediately return None.  The float parameter
            is a value between 0.0 and 1.0 to indicate progress and
            the str parameter will contain a text message indicating
            the progress of this call.<br>
            progressUserValue - is a typing.Any value that is passsed
            to the progressCallback function.<br>
        Returns
        -------
        str
            name of tempory file or None if there was an error.
        """
        # pylint: disable=too-many-locals

        progress_callback = keywords.get('progressCallback', None)
        progress_user_value = keywords.get('progressUserValue', None)

        suffix = os.path.splitext(urlparse(url).path)[1]

        file_descriptor, tmp_filename = mkstemp(suffix=suffix)

        download_bytes = 0
        next_progress_report = 0.1
        with self._session.get(url, stream=True,
                               timeout=self._timeout) as response:

            file = open(tmp_filename, 'wb')
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)
                    # file.flush()
                    if progress_callback is not None:
                        download_bytes += len(chunk)
                        if size == 0:
                            download_progress = 0.0
                        else:
                            download_progress = float(download_bytes) / size
                        if download_progress > next_progress_report:
                            next_progress_report += download_progress
                            if progress_callback(download_progress,\
                                   'Continuing download of data.',
                                                 progress_user_value) != 0:

                                file.close()
                                os.close(file_descriptor)
                                return None
            file.close()
            os.close(file_descriptor)

        if progress_callback is not None:
            if progress_callback(0.4,
                                 'Data download complete. Reading data.',
                                 progress_user_value) != 0:
                return None

        return tmp_filename


    def get_data(
            self,
            dataset: str,
            variables: List[str],
            start: Union[datetime, str], end: Union[datetime, str],
            **keywords: Union[
                Dict,
                Callable[[float, str, Any], int],
                Any]
        ) -> Tuple[Dict, 'spdm.SpaceData']:
        """
        Gets the specified data from the server.

        Parameters
        ----------
        dataset
            dataset identifier of data to get.
        variables
            array containing names of variables to get.
        start
            start time of data to get.
        end
            end time of data to get.
        keywords
            optional keyword parameters as follows<br>
            binData - indicates that uniformly spaced values should be
            computed for scaler/vector/spectrogram data according to
            the given binning parameter values.  See
            <https://cdaweb.gsfc.nasa.gov/CDAWeb_Binning_readme.html>
            for more details.  binData is a Dict that
            may contain the following keys: interval,
            interpolateMissingValues, sigmaMultiplier, and/or
            overrideDefaultBinning with values that override the defaults.<br>
            progressCallback - is a
            Callable[[float, str, typing.Any], int]
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns non-0 value,
            getting the data will be aborted and the get_data() function
            will immediately return (204, None).  The float parameter
            is a value between 0.0 and 1.0 to indicate progress and
            the str parameter will contain a text message indicating
            the progress of this call.<br>
            progressUserValue - is an Any value that is passsed
            to the progressCallback function.<br>
        Returns
        -------
        Tuple
            [0] contains a dictionary of HTTP and CDAS status information.
            When successful, ['http']['status_code'] will be 200.<br>
            [1] contains the requested data (SpaceData object) or None.
        Raises
        ------
        ValueError
            If the given start/end datetime values are invalid.
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-return-statements
        # pylint: enable=too-many-statements
        # pylint: disable=too-many-branches
        # pylint: disable=import-outside-toplevel

        import spacepy.datamodel as spdm       # type: ignore

        start_datetime, end_datetime = TimeInterval.get_datetimes(start,
                                                                  end)
        data_request = CdfRequest(dataset, variables,
                                  TimeInterval(start_datetime, end_datetime),
                                  3, CdfFormat.BINARY,
                                  binData=keywords.get('binData', {}))

        progress_callback = keywords.get('progressCallback', None)
        progress_user_value = keywords.get('progressUserValue', None)

        self.logger.debug('data_request = %s', data_request)

        status = {
            'http': {
                'status_code': 204
            },
            'cdas': {
                'status': [],
                'message': [],
                'warning': [],
                'error': []
            }
        }

        if progress_callback is not None:
            if progress_callback(0.1, 'Making initial server request.',
                                 progress_user_value) != 0:
                return (status, None)

        status_code, data_result = self.get_data_result(data_request,
                                                        progress_callback,
                                                        progress_user_value)

        status['http']['status_code'] = status_code

        if progress_callback is not None:
            if progress_callback(0.3, 'Initial server request complete.',
                                 progress_user_value) != 0:
                return (status, None)

        if status_code != 200:

            self.logger.info('get_data_result failed with http code %d',
                             status_code)
            self.logger.info('data_request = %s', data_request)
            return (status, None)

        if not data_result:
            return (status, None)

        if 'Status' in data_result:
            status['cdas']['status'] = data_result['Status']
        if 'Message' in data_result:
            status['cdas']['message'] = data_result['Message']
        if 'Warning' in data_result:
            status['cdas']['warning'] = data_result['Warning']
        if 'Error' in data_result:
            status['cdas']['error'] = data_result['Error']

        if progress_callback is not None:
            if progress_callback(0.4, 'Beginning download of data.',
                                 progress_user_value) != 0:
                return (status, None)

        file_descriptions = data_result['FileDescription']

        data_url = file_descriptions[0]['Name']
        data_length = file_descriptions[0]['Length']

        self.logger.debug('data_url = %s, data_length = %d',
                          data_url, data_length)

        sub_progress_control = {
            'progressCallback': progress_callback,
            'progressUserValue': progress_user_value,
            'progressStart': 0.4,
            'progressFraction': 0.1
        }

        tmp_filename = self.download(data_url, data_length,
                                     progressCallback=_get_data_progress,
                                     progressUserValue=sub_progress_control)

        try:
            data = spdm.fromCDF(tmp_filename)
            if progress_callback is not None:
                if progress_callback(1.0, 'Finished reading data.',
                                     progress_user_value) != 0:
                    return (status, None)
            os.remove(tmp_filename)
            return (status, data)
        except:
            self.logger.error('Exception from spdm.fromCDF(%s): %s', 
                              tmp_filename, sys.exc_info()[0])
            self.logger.error('CDF file has been retained.')
            raise


    # pylint: disable=too-many-arguments
    def get_graph(
            self,
            dataset: str,
            variables: List[str],
            start: Union[datetime, str],
            end: Union[datetime, str],
            options: GraphOptions = None,
            image_format: List[ImageFormat] = None,
            **keywords
        ) -> Tuple[int, Dict]:
        """
        Gets a graphical representation of the specified data from the
        server.

        Parameters
        ----------
        dataset
            dataset identifier of data to get.
        variables
            array containing names of variables to get.
        start
            start time of data to get.
        end
            end time of data to get.
        options
            graph options.
        image_format
            image format.  If None, then [ImageFormat.PNG].
        keywords
            optional keyword parameters as follows<br>
            binData - indicates that uniformly spaced values should be
            computed for scaler/vector/spectrogram data according to
            the given binning parameter values.  binData is a Dict that
            may contain the following keys: interval,
            interpolateMissingValues, sigmaMultiplier, and/or
            overrideDefaultBinning with values that override the defaults.<br>
            progressCallback - is a
            typing.Callable[[float, str, typing.Any], int]
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns non-0 value,
            getting the data will be aborted and the get_data() function
            will immediately return (204, None).  The float parameter
            is a value between 0.0 and 1.0 to indicate progress and
            the str parameter will contain a text message indicating
            the progress of this call.<br>
            progressUserValue - is a typing.Any value that is passsed
            to the progressCallback function.<br>
        Returns
        -------
        Tuple
            [0] contains the HTTP status code value (200 when successful).<br>
            [1] contains a dictionary representation of a
                <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>
                DataResult object or None.<br>
        Raises
        ------
        ValueError
            If the given start/end datetime values are invalid.
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-return-statements
        # pylint: enable=too-many-statements
        # pylint: disable=too-many-branches

        start_datetime, end_datetime = TimeInterval.get_datetimes(start,
                                                                  end)

        request = GraphRequest(dataset, variables,
                               TimeInterval(start_datetime, end_datetime),
                               options, image_format,
                               **keywords)

        progress_callback = keywords.get('progressCallback', None)
        progress_user_value = keywords.get('progressUserValue', None)

        self.logger.debug('request = %s', request)

        if progress_callback is not None:
            if progress_callback(0.1, 'Making server request.',
                                 progress_user_value) != 0:
                return (204, None)

        status_code, result = self.get_data_result(request, progress_callback, progress_user_value)

        if progress_callback is not None:
            if progress_callback(1.0, 'Server request complete.',
                                 progress_user_value) != 0:
                return (status_code, None)

        if status_code != 200:

            self.logger.info('get_result failed with http code %d',
                             status_code)
            self.logger.info('request = %s', request)
            return (status_code, None)

        return (status_code, result)
    # pylint: enable=too-many-arguments


    # pylint: disable=too-many-arguments
    def get_thumbnail(
            self,
            dataset: str,
            variables: List[str],
            start: Union[datetime, str],
            end: Union[datetime, str],
            identifier: str,
            thumbnail: int = 1,
            **keywords
        ) -> Tuple[int, Dict]:
        """
        Gets a graphical representation of the specified data from the
        server.

        Parameters
        ----------
        dataset
            dataset identifier of data to get.
        variables
            array containing names of variables to get.
        start
            start time of data to get.
        end
            end time of data to get.
        identifier
            thumbnail identifier (returned in a previous get_graph
            result).
        thumbnail
            number of thumbnail whose full size image is being requested.
            Thumbnail images are counted beginning at one (not zero).
        keywords
            optional keyword parameters as follows<br>
            progressCallback - is a
            typing.Callable[[float, str, typing.Any], int]
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns non-0 value,
            getting the data will be aborted and the get_data() function
            will immediately return (204, None).  The float parameter
            is a value between 0.0 and 1.0 to indicate progress and
            the str parameter will contain a text message indicating
            the progress of this call.<br>
            progressUserValue - is a typing.Any value that is passsed
            to the progressCallback function.<br>
        Returns
        -------
        Tuple
            [0] contains the HTTP status code value (200 when successful).<br>
            [1] contains a dictionary representation of a
                <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>
                DataResult object or None.<br>
        Raises
        ------
        ValueError
            If the given start/end datetime values are invalid.
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-return-statements
        # pylint: enable=too-many-statements
        # pylint: disable=too-many-branches

        start_datetime, end_datetime = TimeInterval.get_datetimes(start,
                                                                  end)

        request = ThumbnailRequest(dataset, variables,
                                   TimeInterval(start_datetime, end_datetime),
                                   identifier, thumbnail)

        progress_callback = keywords.get('progressCallback', None)
        progress_user_value = keywords.get('progressUserValue', None)

        self.logger.debug('request = %s', request)

        if progress_callback is not None:
            if progress_callback(0.1, 'Making server request.',
                                 progress_user_value) != 0:
                return (204, None)

        status_code, result = self.get_data_result(request,
                                                   progress_callback,
                                                   progress_user_value)

        if progress_callback is not None:
            if progress_callback(1.0, 'Server request complete.',
                                 progress_user_value) != 0:
                return (status_code, None)

        if status_code != 200:

            self.logger.info('get_result failed with http code %d',
                             status_code)
            self.logger.info('request = %s', request)
            return (status_code, None)

        return (status_code, result)
    # pylint: enable=too-many-arguments


    # pylint: disable=too-many-arguments
    def get_text(
            self,
            dataset: str,
            variables: List[str],
            start: Union[datetime, str],
            end: Union[datetime, str],
            compression: Compression = Compression.UNCOMPRESSED,
            text_format: TextFormat = TextFormat.PLAIN,
            **keywords
        ) -> Tuple[int, Dict]:
        """
        Gets a textual representation of the specified data from the
        server.

        Parameters
        ----------
        dataset
            dataset identifier of data to get.
        variables
            array containing names of variables to get.
        start
            start time of data to get.
        end
            end time of data to get.
        compression
            file compression.
        text_format
            text format.
        keywords
            optional keyword parameters as follows<br>
            binData - indicates that uniformly spaced values should be
            computed for scaler/vector/spectrogram data according to
            the given binning parameter values.  binData is a Dict that
            may contain the following keys: interval,
            interpolateMissingValues, sigmaMultiplier, and/or
            overrideDefaultBinning with values that override the defaults.<br>
            progressCallback - is a
            typing.Callable[[float, str, typing.Any], int]
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns non-0 value,
            getting the data will be aborted and the get_data() function
            will immediately return (204, None).  The float parameter
            is a value between 0.0 and 1.0 to indicate progress and
            the str parameter will contain a text message indicating
            the progress of this call.<br>
            progressUserValue - is a typing.Any value that is passsed
            to the progressCallback function.<br>
        Returns
        -------
        Tuple
            [0] contains the HTTP status code value (200 when successful).<br>
            [1] contains a dictionary representation of a
                <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>
                DataResult object or None.<br>
        Raises
        ------
        ValueError
            If the given start/end datetime values are invalid.
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-return-statements
        # pylint: enable=too-many-statements
        # pylint: disable=too-many-branches

        start_datetime, end_datetime = TimeInterval.get_datetimes(start,
                                                                  end)

        request = TextRequest(dataset, variables,
                              TimeInterval(start_datetime, end_datetime),
                              compression, text_format,
                              **keywords)

        progress_callback = keywords.get('progressCallback', None)
        progress_user_value = keywords.get('progressUserValue', None)

        self.logger.debug('request = %s', request)

        if progress_callback is not None:
            if progress_callback(0.1, 'Making server request.',
                                 progress_user_value) != 0:
                return (204, None)

        status_code, result = self.get_data_result(request,
                                                   progress_callback,
                                                   progress_user_value)

        if progress_callback is not None:
            if progress_callback(1.0, 'Server request complete.',
                                 progress_user_value) != 0:
                return (status_code, None)

        if status_code != 200:

            self.logger.info('get_result failed with http code %d',
                             status_code)
            self.logger.info('request = %s', request)
            return (status_code, None)

        return (status_code, result)
    # pylint: enable=too-many-arguments


    def get_audio(
            self,
            dataset: str,
            variables: List[str],
            start: Union[datetime, str],
            end: Union[datetime, str],
            **keywords
        ) -> Tuple[int, Dict]:
        """
        Gets an audio representation of the specified data from the
        server.

        Parameters
        ----------
        dataset
            dataset identifier of data to get.
        variables
            array containing names of variables to get.
        start
            start time of data to get.
        end
            end time of data to get.
        keywords
            optional keyword parameters as follows<br>
            binData - indicates that uniformly spaced values should be
            computed for scaler/vector/spectrogram data according to
            the given binning parameter values.  binData is a Dict that
            may contain the following keys: interval,
            interpolateMissingValues, sigmaMultiplier, and/or
            overrideDefaultBinning with values that override the defaults.<br>
            progressCallback - is a
            typing.Callable[[float, str, typing.Any], int]
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns non-0 value,
            getting the data will be aborted and the get_data() function
            will immediately return (204, None).  The float parameter
            is a value between 0.0 and 1.0 to indicate progress and
            the str parameter will contain a text message indicating
            the progress of this call.<br>
            progressUserValue - is a typing.Any value that is passsed
            to the progressCallback function.<br>
        Returns
        -------
        Tuple
            [0] contains the HTTP status code value (200 when successful).<br>
            [1] contains a dictionary representation of a
                <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>
                DataResult object or None.<br>
        Raises
        ------
        ValueError
            If the given start/end datetime values are invalid.
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-return-statements
        # pylint: enable=too-many-statements
        # pylint: disable=too-many-branches

        start_datetime, end_datetime = TimeInterval.get_datetimes(start,
                                                                  end)

        request = AudioRequest(dataset, variables,
                               TimeInterval(start_datetime, end_datetime),
                               **keywords)

        progress_callback = keywords.get('progressCallback', None)
        progress_user_value = keywords.get('progressUserValue', None)

        self.logger.debug('request = %s', request)

        if progress_callback is not None:
            if progress_callback(0.1, 'Making server request.',
                                 progress_user_value) != 0:
                return (204, None)

        status_code, result = self.get_data_result(request,
                                                   progress_callback,
                                                   progress_user_value)

        if progress_callback is not None:
            if progress_callback(1.0, 'Server request complete.',
                                 progress_user_value) != 0:
                return (status_code, None)

        if status_code != 200:

            self.logger.info('get_result failed with http code %d',
                             status_code)
            self.logger.info('request = %s', request)
            return (status_code, None)

        return (status_code, result)
