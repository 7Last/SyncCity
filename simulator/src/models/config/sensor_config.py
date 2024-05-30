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
        self.uuid = UUID(config.get('uuid'))
        self.limit = config.get('limit') or None
        self.begin_date = config.get('begin_date') or None
        self.latitude = config.get('latitude')
        self.longitude = config.get('longitude')

        generation_delay = config.get('generation_delay') or None
        points_spacing = config.get('points_spacing')

        try:
            if not config.get('type'):
                raise Exception('type must not be empty')
            self.type = SensorType.from_str(config.get('type'))
        except Exception:
            log.exception(
                'Type must not be empty and must match one of SensorType values',
            )
            raise

        try:
            self.points_spacing: timedelta = isodate.parse_duration(points_spacing)
        except isodate.isoerror.ISO8601Error:
            log.exception(
                'Invalid points_spacing value. Must be specified following ISO8601',
            )
            raise

        try:
            self.generation_delay: timedelta = isodate.parse_duration(generation_delay)
        except isodate.isoerror.ISO8601Error:
            log.exception(
                'Invalid generation_delay value. Must be specified following ISO8601',
            )
            raise

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'
