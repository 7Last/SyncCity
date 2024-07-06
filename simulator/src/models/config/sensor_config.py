import logging as log
from datetime import timedelta
from typing import Dict
from uuid import UUID

import isodate

from ..sensor_type import SensorType


class SensorConfig:
    def __init__(self, config: Dict[str, any]) -> None:
        """
        Represents the schema for the sensor configuration
        :param config: dictionary with the configuration for a single sensor
        """
        self._sensor_uuid = UUID(config.get('uuid'))
        self.__limit = config.get('limit') or None
        self.__begin_date = config.get('begin_date') or None
        self.__latitude = config.get('latitude')
        self.__longitude = config.get('longitude')
        self.__group_name = config.get('group_name') or None

        generation_delay = config.get('generation_delay') or None
        points_spacing = config.get('points_spacing') or None

        try:
            if not config.get('type'):
                raise Exception('type must not be empty')
            self.__type = SensorType.from_str(config.get('type'))
        except Exception:
            log.exception(
                'Type must not be empty and must match one of SensorType values',
            )
            raise

        try:
            if points_spacing is None:
                self._points_spacing = None
            else:
                self._points_spacing: timedelta = isodate.parse_duration(points_spacing)
        except isodate.isoerror.ISO8601Error:
            log.exception(
                'Invalid _points_spacing value. Must be specified following ISO8601',
            )
            raise

        try:
            if generation_delay is None:
                self._generation_delay = None
            else:
                self._generation_delay: timedelta = isodate.parse_duration(
                    generation_delay)
        except isodate.isoerror.ISO8601Error:
            log.exception(
                'Invalid _generation_delay value. Must be specified following ISO8601',
            )
            raise

    def type(self) -> SensorType:
        return self.__type

    def sensor_uuid(self) -> UUID:
        return self._sensor_uuid

    def limit(self) -> int | None:
        return self.__limit

    def begin_date(self) -> str | None:
        return self.__begin_date

    def latitude(self) -> float:
        return self.__latitude

    def longitude(self) -> float:
        return self.__longitude

    def group_name(self) -> str | None:
        return self.__group_name

    def points_spacing(self) -> timedelta | None:
        return self._points_spacing

    def generation_delay(self) -> timedelta | None:
        return self._generation_delay

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'
