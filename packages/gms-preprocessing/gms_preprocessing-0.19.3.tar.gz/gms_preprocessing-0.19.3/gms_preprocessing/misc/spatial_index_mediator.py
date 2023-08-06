# -*- coding: utf-8 -*-

# gms_preprocessing, spatial and spectral homogenization of satellite remote sensing data
#
# Copyright (C) 2020  Daniel Scheffler (GFZ Potsdam, daniel.scheffler@gfz-potsdam.de)
#
# This software was developed within the context of the GeoMultiSens project funded
# by the German Federal Ministry of Education and Research
# (project grant code: 01 IS 14 010 A-C).
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
# Please note the following exception: `gms_preprocessing` depends on tqdm, which
# is distributed under the Mozilla Public Licence (MPL) v2.0 except for the files
# "tqdm/_tqdm.py", "setup.py", "README.rst", "MANIFEST.in" and ".gitignore".
# Details can be found here: https://github.com/tqdm/tqdm/blob/master/LICENCE.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import socket
import struct
import os
import re
import warnings
from datetime import datetime, timedelta
from shapely.geometry import Polygon
import pytz
from logging import getLogger
from typing import List  # noqa F401  # flake8 issue

from ..misc.exceptions import GMSEnvironmentError
from ..misc.logging import close_logger


class SpatialIndexMediatorServer:
    def __init__(self, rootDir, logger=None):
        self.rootDir = rootDir
        self.path_idxMedSrv = os.path.join(rootDir, 'index-mediator-server.sh')
        self.logger = logger or getLogger('SpatialIndexMediatorServer')

        # validate
        if not os.path.isfile(self.path_idxMedSrv):
            self.path_idxMedSrv = os.path.join(rootDir, 'index-mediator-server')

            if not os.path.isfile(self.path_idxMedSrv):
                raise GMSEnvironmentError('File path of index mediator server does not exist at %s.'
                                          % self.path_idxMedSrv)

    def __getstate__(self):
        """Defines how the attributes of SpatialIndexMediatorServer are pickled."""

        if self.logger not in [None, 'not set']:
            close_logger(self.logger)
            self.logger = None
        return self.__dict__

    def __del__(self):
        close_logger(self.logger)
        self.logger = None

    @property
    def is_running(self):
        return self.status['running']

    @property
    def process_id(self):
        return self.status['process_id']

    @property
    def status(self):
        """Check server status.

        :return running(bool):    running or not?
        :return process_id(int):
        """
        outputStr = self._communicate('status')

        # decrypt status
        running = 'is running' in outputStr

        # get PID
        _process_id = re.search(r'with pid ([\d]*)', outputStr)
        if _process_id and _process_id.group(1):
            process_id = int(_process_id.group(1))
        else:
            process_id = None

        return {'running': running, 'process_id': process_id}

    def start(self):  # FIXME can be executed twice without a message that server is already running
        outputStr = self._communicate('start')
        if outputStr == 'success' and self.is_running:
            self.logger.info('Spatial Index Mediator Server started successfully.')
            return 'started'
        else:
            if outputStr != 'success':
                self.logger.warning("\nAttempt to start Spatial Index Mediator Server failed with message '%s'!"
                                    % outputStr.replace('\n', ''))
            else:
                self.logger.warning("\nCommunication to Spatial Index Mediator Server was successful but "
                                    "the server is still not running. Returned message was: %s"
                                    % outputStr.replace('\n', ''))

    def stop(self):
        outputStr = self._communicate('stop')

        if outputStr == 'success' or re.search(r'index-mediator-server stopped', outputStr, re.I):
            return 'stopped'
        else:
            warnings.warn("\nStopping Spatial Index Mediator Server failed with message '%s'!"
                          % outputStr.replace('\n', ''))

    def restart(self):
        outputStr = self._communicate('restart')
        if outputStr == 'success' and self.is_running:
            return 'restarted'
        else:
            warnings.warn("\nRestarting Spatial Index Mediator Server failed with message '%s'!"
                          % outputStr.replace('\n', ''))

    def _communicate(self, controller_cmd):
        curdir = os.path.abspath(os.curdir)
        os.chdir(self.rootDir)
        # FIXME workaround: otherwise subcall_with_output hangs at proc.communicate (waiting for EOF forever)
        no_stdout = no_stderr = controller_cmd in ['start', 'restart']
        # no_stdout = no_stderr = None, None
        from ..misc.helper_functions import subcall_with_output
        output, exitcode, err = subcall_with_output('bash %s %s' % (self.path_idxMedSrv,
                                                                    controller_cmd), no_stdout, no_stderr)
        os.chdir(curdir)

        if exitcode:
            raise Exception(err)
        else:
            if output:
                return output.decode('UTF-8')
            else:
                # FIXME actually there should be always an output (also with controller commands 'start' and 'restart'
                return 'success'


class SpatialIndexMediator:
    FULL_SCENE_QUERY_MSG = 3
    """ message value for a full scene query message """

    def __init__(self, host="localhost", port=8654, timeout=5.0, retries=10):
        """
        Establishes a connection to the spatial index mediator server.

        :param host:    host address of the index mediator server (default "localhost")
        :param port:    port number of the index mediator server (default 8654)
        :param timeout: timeout as float in seconds (default 5.0 sec)
        :param retries: number of retries in case of timeout
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.retries = retries

    @staticmethod
    def __deriveSeasonCode(refDate, maxDaysDelta):
        if refDate is None or maxDaysDelta is None:
            return 0

        delta = timedelta(days=maxDaysDelta)

        startMonth = (refDate - delta).month - 1
        endMonth = (refDate + delta).month - 1

        seasonCode = 0

        for x in range(12):
            month = (startMonth + x) % 12

            seasonCode |= 1 << month

            if month == endMonth:
                break

        return seasonCode

    def getFullSceneDataForDataset(self, envelope, timeStart, timeEnd, minCloudCover, maxCloudCover, datasetid,
                                   dayNight=0, refDate=None, maxDaysDelta=None):
        # type: (list, datetime, datetime, float, float, int, int, datetime, int) -> List[Scene]
        """
        Query the spatial index with the given parameters in order to get a list of matching scenes intersecting the
        given envelope

        :param envelope:        list of left, right and low, up coordinates (in lat/lon wgs84) of the region of
                                interest in the form of (min_lon, max_lon, min_lat, max_lat),
                                e.g. envelope = (10.0, 16.0, 50.0, 60.0)
        :param timeStart:       start timestamp of the relevant timerange as datetime instance,
                                e.g., datetime(2015, 1, 1)
        :param timeEnd:         end timestamp of the relevant timerange as datetime instance, e.g. datetime(2016, 6, 15)
        :param minCloudCover:   minimum cloudcover in percent, e.g. 12, will return scenes with cloudcover >= 12% only
        :param maxCloudCover:   maximum cloudcover in percent, e.g. 23, will return scenes with cloudcover <= 23% only
        :param datasetid:       datasetid of the dataset in question, e.g. 104 for Landsat-8
        :param dayNight         day/night indicator, with (0 = both, 1 = day, 2 = night)
        :param refDate:         reference timestamp as datetime instance, e.g. datetime(2015, 1, 1) [optional]
        :param maxDaysDelta:    maximum allowed number of days the target scenes might be apart from the given refDate
                                [optional]
        """
        scenes = []

        for i in range(self.retries):
            try:
                filterTimerange = not (refDate is None or maxDaysDelta is None)

                # prepare buffer
                # numbytes = 1 + 4*8 + 8 + 8 + 4 + 1 + 1 + 2 + 2 + 1
                b = bytearray(60)

                # pack msg header and envelope
                offset = 0
                struct.pack_into('> b 4d', b, offset, self.FULL_SCENE_QUERY_MSG, *envelope)
                offset += 33

                # pack the dates
                struct.pack_into('> h 6b', b, offset, timeStart.year, timeStart.month, timeStart.day, timeStart.hour,
                                 timeStart.minute, timeStart.second, 0)
                offset += 8
                struct.pack_into('> h 6b', b, offset, timeEnd.year, timeEnd.month, timeEnd.day, timeEnd.hour,
                                 timeEnd.minute, timeEnd.second, 0)
                offset += 8

                # derive season code
                seasonCode = self.__deriveSeasonCode(refDate, maxDaysDelta)

                # pack the rest
                #  TODO: send unconstraint min/max proclevel values
                struct.pack_into('> i 2b h 3b', b, offset, seasonCode, minCloudCover, maxCloudCover, datasetid, 0, 127,
                                 dayNight)

                # get connection and lock the channel
                con = Connection(self.host, self.port, self.timeout)

                # send the buffer
                con.socket.sendall(b)

                # receive the response
                # read first byte, indicating the response type, must match full scene query msg
                if con.recvByte() != self.FULL_SCENE_QUERY_MSG:
                    raise EnvironmentError('Bad Protocol')

                # now read the number of bytes that follow
                numBytes = con.recvInt()
                b = bytearray(numBytes)
                offset = 0

                # read all data from the channel and unlock it
                con.recvBuffer(b, numBytes)

                # we received the entire message - return the connection to the global pool
                con.disconnect()

                # interpret received data
                # extract datasetid and number of scenes
                dataset = struct.unpack_from('> h', b, offset)[0]
                offset += 2
                if dataset != datasetid:
                    raise EnvironmentError('Bad Protocol')

                numScenes = struct.unpack_from('> i', b, offset)[0]
                offset += 4

                scenes = []

                for _x in range(numScenes):
                    # [0] id (4 byte)
                    # [1] year (2 byte)
                    # [2] month (1 byte)
                    # [3] day (1 byte)
                    # [4] hour (1 byte)
                    # [5] minute (1 byte)
                    # [6] second (1 byte)
                    # [7] empty (1 byte)
                    # [8] cloud cover (1 byte)
                    # [9] proc_level (1 byte) caution: this gets not yet updated in the index
                    # [10] day/night (1 byte)
                    # [11] length of bounds array (1 byte)
                    scenedata = struct.unpack_from('> i h 10b', b, offset)
                    offset += 16

                    # print(scenedata)
                    timestamp = datetime(scenedata[1], scenedata[2], scenedata[3], scenedata[4], scenedata[5],
                                         scenedata[6])

                    # read bounds
                    numBounds = scenedata[11]
                    fmt = "> {0}d".format(numBounds)
                    bounds = struct.unpack_from(fmt, b, offset)
                    offset += numBounds * 8

                    # check ref date
                    if filterTimerange:
                        if timestamp.month == 2 and timestamp.day == 29:
                            # deal with feb.29th
                            timestampInRefYear = timestamp.replace(refDate.year, 3, 1).replace(tzinfo=pytz.UTC)
                        else:
                            timestampInRefYear = timestamp.replace(refDate.year).replace(tzinfo=pytz.UTC)

                        if abs(refDate - timestampInRefYear).days > maxDaysDelta:
                            # skip scene
                            continue

                    # create scene
                    scenes.append(Scene(scenedata[0], timestamp, scenedata[8], scenedata[9], scenedata[10], bounds))

                break

            except socket.timeout:
                if i < self.retries - 1:
                    continue
                else:
                    raise TimeoutError('Spatial query timed out 10 times!')

            except struct.error:
                if i < self.retries - 1:
                    continue
                else:
                    raise

        return scenes


class Connection:
    """ Connection to the spatial index mediator server """

    HELLO_MSG = 1
    """ message value for a "hello" message """

    DISCONNECT_MSG = 6
    """ message value for a disconnect message """

    def __init__(self, host, port, timeout):
        # connect to index mediator server
        try:
            self.socket = socket.create_connection((host, port), timeout)
        except ConnectionRefusedError:
            raise ConnectionRefusedError('The spatial index mediator server refused the connection!')

        # send hello and confirm response
        if not self.__greet():
            raise EnvironmentError('Bad protocol')

    def __greet(self):
        # send hello byte
        self.writeByte(self.HELLO_MSG)

        # receive hello byte echo
        response = self.recvByte()

        return response == self.HELLO_MSG

    def writeByte(self, byte):
        # send byte
        self.socket.sendall(struct.pack('b', byte))

    def recvByte(self):
        return struct.unpack('b', self.socket.recv(1))[0]

    def recvInt(self):
        return struct.unpack('>i', self.socket.recv(4))[0]

    def recvBuffer(self, buffer, numBytes):
        toread = numBytes
        view = memoryview(buffer)
        while toread:
            nbytes = self.socket.recv_into(view, toread)
            view = view[nbytes:]
            toread -= nbytes

    def disconnect(self):
        """Closes the connection to the index mediator server.

        No further communication, like placing queries will be possible.
        """
        self.writeByte(self.DISCONNECT_MSG)
        self.socket.close()


class Scene:
    """Scene Metadata class"""

    def __init__(self, sceneid, acquisitiondate, cloudcover, proclevel, daynight, bounds):
        """
        :param sceneid:         database sceneid, e.g. 26366229
        :param acquisitiondate: acquisition date of the scene as datetime instance, e.g. 2016-03-25 10:15:26
        :param cloudcover:      cloudcover value of the scene, e.g. 11
        :param daynight:        day/night indicator (0=unknown, 1=day, 2=night)
        :param bounds:          scene bounds as list of lat/lon wgs84 coordinates (lon1, lat1, lon2, lat2, ...),
                                e.g. (10.00604, 49.19385, 7.45638, 49.64513, 8.13739, 51.3515, 10.77705, 50.89307)
        """
        self.sceneid = sceneid
        self.acquisitiondate = acquisitiondate
        self.cloudcover = cloudcover
        self.proclevel = proclevel
        self.daynight = daynight
        self.bounds = bounds
        tempList = list(bounds) + [None] * 2
        self.coordsLonLat = [tempList[n:n + 2] for n in range(0, len(bounds), 2)]

        # set validated (!) polygon
        poly = Polygon(self.coordsLonLat)
        if not poly.is_valid:
            poly = poly.buffer(0)
            assert poly.is_valid
        self.polyLonLat = poly
