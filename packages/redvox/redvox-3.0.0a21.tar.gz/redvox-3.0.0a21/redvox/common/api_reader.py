"""
Read Redvox data from a single directory
Data files can be either API 900 or API 1000 data formats
The ReadResult object contains lists for both API versions
"""
# todo: convert enums to text before returning?
# todo: concat.py for api m?
# todo: get the cpu utilization from station metrics
import os
import numpy as np
import pandas as pd

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

from redvox.api1000 import io as apim_io
from redvox.api1000.wrapped_redvox_packet.wrapped_packet import WrappedRedvoxPacketM
from redvox.api900 import reader as api900_io
from redvox.common import file_statistics as fs, date_time_utils as dtu, timesync as ts


@dataclass
class StationSummary:
    """
    Contains a summary of each stations' data reader results.
    properties:
        station_id: str, station id
        station_uuid: str, station uuid
        os: str, station os
        os_version: str, station os version
        app_version: str, station app version
        audio_sampling_rate_hz: float, sample rate in hz
        total_duration_s: float, duration of data in seconds
        start_dt: dtu.datetime object, start datetime of data read
        end_dt: dtu.datetime object, end datetime of data read
    """
    station_id: str
    station_uuid: str
    os: str
    os_version: str
    app_version: str
    audio_sampling_rate_hz: float
    total_duration_s: float
    start_dt: dtu.datetime
    end_dt: dtu.datetime

    @staticmethod
    def from_station(station: WrappedRedvoxPacketM) -> 'StationSummary':
        """
        :param station: the station to make a summary for
        :return: the station summary of a single station
        """
        total_duration: float = station.get_packet_duration_s()
        start_dt: dtu.datetime = dtu.datetime_from_epoch_microseconds_utc(
            station.get_timing_information().get_packet_start_mach_timestamp())
        end_dt: dtu.datetime = dtu.datetime_from_epoch_microseconds_utc(
            station.get_timing_information().get_packet_end_mach_timestamp())

        station_info = station.get_station_information()
        audio = station.get_sensors().get_audio()
        return StationSummary(
            station_info.get_id(),
            station_info.get_uuid(),
            station_info.get_os().name,
            station_info.get_os_version(),
            station_info.get_app_version(),
            audio.get_sample_rate() if audio is not None else np.nan,
            total_duration,
            start_dt,
            end_dt
        )


@dataclass
class StationKey:
    """
    Minimum data required to form a unique key for a station
    Properties:
        id: str, id of a station
        uuid: str, the uuid of a station
        start_timestamp: float, the start timestamp in microseconds since epoch UTC of the station
    """
    id: str
    uuid: str
    start_timestamp: float

    def __str__(self):
        return f"{self.id}:{self.uuid}, {self.start_timestamp}"

    def check_for_id(self, check_id: str) -> bool:
        """
        checks if the check_id is equal to id, uuid, or id:uuid
        :param check_id: str, id to check for
        :return: True if the check_id is one of the three valid possibilities, False otherwise
        """
        return check_id == self.id or check_id == self.uuid or check_id == f"{self.id}:{self.uuid}"


class ReadResult:
    """
    Stores station information after being read from files
    Properties:
        station_id_uuid_to_stations: dict of string to Station object, where the string is id:uuid format
        __station_id_to_id_uuid: dict of string to string, maps id to uuid
        __station_summaries: dict of string to StationSummary object, maps id to StationSummary
    """
    def __init__(self, stations: List[WrappedRedvoxPacketM]):
        """
        :param stations: list of WrappedRedvoxPacketM objects to add
        """
        self.station_keys: List[StationKey] = []
        self.station_keys_to_stations: Dict[StationKey, WrappedRedvoxPacketM] = {}
        self.__station_summaries: Dict[StationKey, StationSummary] = {}
        for station in stations:
            stationkey = StationKey(station.get_station_information().get_id(),
                                    station.get_station_information().get_uuid(),
                                    station.get_timing_information().get_app_start_mach_timestamp())
            self.station_keys.append(stationkey)
            self.station_keys_to_stations[stationkey] = station
            self.__station_summaries[stationkey] = StationSummary.from_station(station)

    def get_key_by_id(self, check_id: str) -> Optional[StationKey]:
        """
        Look at keys' id and uuid for the check_id; must be one of id, id:uuid, or uuid
        :param check_id: str id to look for
        :return: The key if the id matches, None otherwise
        """
        for key in self.station_keys:
            if key.check_for_id(check_id):
                return key
        return None

    def pop_station(self, station_id: str) -> 'ReadResult':
        """
        removes a station from the ReadResult; station_id can be one of id, uuid or id:uuid
        :param station_id: str, id of station to remove
        :return: copy of ReadResult without the station_id specified
        """
        result = self.get_key_by_id(station_id)
        if result:
            self.__station_summaries.pop(result)
            self.station_keys_to_stations.pop(result)
            self.station_keys.remove(result)
        else:
            print(f"ReadResult cannot remove station {station_id} because it does not exist")
        return self

    def get_station(self, station_id: str) -> Optional[WrappedRedvoxPacketM]:
        """
        Find the station identified by the station_id given; it can be id, uuid or id:uuid
        :param station_id: str, id of station to get
        :return: the station's WrappedRedvoxPacketM if it exists, None otherwise
        """
        result = self.get_key_by_id(station_id)
        if result:
            return self.station_keys_to_stations[result]
        else:
            print(f"WARNING: ReadResult attempted to read station id: {station_id}, but could not find it")
        return None

    def get_all_stations(self) -> List[WrappedRedvoxPacketM]:
        """
        :return: a list of all stations' WrappedRedvoxPacketM in the ReadResult
        """
        return list(self.station_keys_to_stations.values())

    def get_all_station_ids(self) -> List[str]:
        """
        :return: a list of all station ids in the ReadResult
        """
        result = []
        for key in self.station_keys:
            result.append(key.id)
        return result

    def get_station_summary(self, station_id: str) -> Optional[StationSummary]:
        """
        Find the station summary identified by the station_id given; it can be id, uuid or id:uuid
        :return: A StationSummary in this ReadResult if it exists, None otherwise
        """
        result = self.get_key_by_id(station_id)
        if result:
            return self.__station_summaries[result]
        else:
            print(f"WARNING: ReadResult attempted to read summary of station id: {station_id}, but could not find it")
        return None

    def get_station_summaries(self) -> List[StationSummary]:
        """
        :return: A list of StationSummaries contained in this ReadResult
        """
        return list(self.__station_summaries.values())

    def append_station(self, new_station: WrappedRedvoxPacketM):
        """
        adds a WrappedRedvoxPacketM to the ReadResult.  Appends data to existing packets
        :param new_station: Station object to add
        """
        result = self.get_key_by_id(new_station.get_station_information().get_id())
        if result:
            self.station_keys_to_stations[result].append(new_station)
        else:
            stationkey = StationKey(new_station.get_station_information().get_id(),
                                    new_station.get_station_information().get_uuid(),
                                    new_station.get_timing_information().get_app_start_mach_timestamp())
            self.station_keys.append(stationkey)
            self.station_keys_to_stations[stationkey] = new_station
            self.__station_summaries[stationkey] = StationSummary.from_station(new_station)

    def append(self, new_stations: 'ReadResult'):
        """
        adds stations from another ReadResult to the calling ReadResult
        :param new_stations: ReadResult object with stations to add
        """
        result = self.get_all_stations()
        result.extend(new_stations.get_all_stations())
        return ReadResult(result)


def read_all_in_dir(directory: str,
                    start_timestamp_utc_s: Optional[int] = None,
                    end_timestamp_utc_s: Optional[int] = None,
                    station_ids: Optional[List[str]] = None,
                    structured_layout: bool = False) -> ReadResult:
    """
    load all data files in the directory
    :param directory: string, location of all the files;
                        if structured_layout is True, the directory contains a root api1000 or api900 directory,
                        if structured_layout is False, the directory contains unsorted files
    :param start_timestamp_utc_s: optional int, The start timestamp as seconds since the epoch UTC.
    :param end_timestamp_utc_s: optional int, The end timestamp as seconds since the epoch UTC.
    :param station_ids: optional list of string station ids to filter against, default empty list
    :param structured_layout: optional bool to define if this is loading structured data, default False.
    :return: a ReadResult object containing the data requested
    """
    # create the object to store the data
    stations: ReadResult = ReadResult({})
    # if structured_layout, there should be a specifically named folder in directory
    if structured_layout:
        if "api900" not in directory:
            api900_dir = os.path.join(directory, "api900")
        else:
            api900_dir = directory
        if "api1000" not in directory:
            apim_dir = os.path.join(directory, "api1000")
        else:
            apim_dir = directory
        # check if none of the paths exists
        if not (os.path.exists(api900_dir) or os.path.exists(apim_dir)):
            # no specially named directory found; raise error
            raise ValueError(f"{directory} does not contain api900 or api1000 directory.")
    else:
        # load files from unstructured layout; everything is sitting in the main directory
        api900_dir = directory
        apim_dir = directory

    # get api900 data
    stations.append(load_file_range_from_api900(api900_dir, start_timestamp_utc_s, end_timestamp_utc_s,
                                                station_ids, structured_layout, False))
    # get api1000 data
    stations.append(load_from_file_range_api_m(apim_dir, start_timestamp_utc_s, end_timestamp_utc_s,
                                               station_ids, structured_layout))
    return stations
