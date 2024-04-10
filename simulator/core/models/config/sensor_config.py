from typing import Dict
from datetime import timedelta
import logging as log

import isodate

from ..sensor_type import SensorType


class SensorConfig:
    def __init__(self, config: Dict) -> None:
        """
        Represents the schema for the sensor configuration
        :param config: dictionary with the configuration for a single sensor
        """
        self.limit = config.get('limit') or None
        self.begin_date = config.get('begin_date') or None
        self.latitude = config.get('latitude')
        self.longitude = config.get('longitude')

        generation_delay = config.get('generation_delay') or None
        points_spacing = config.get('points_spacing')

        try:
            self.type = SensorType.from_str(config.get('type'))
        except Exception as e:
            log.fatal(
                'Invalid points_spacing value. Must be specified following ISO8601',
                e,
            )
            raise

        try:
            self.points_spacing: timedelta = isodate.parse_duration(points_spacing)
        except Exception as e:
            log.fatal(
                'Invalid points_spacing value. Must be specified following ISO8601',
                e,
            )
            raise

        try:
            self.generation_delay: timedelta = isodate.parse_duration(generation_delay)
        except Exception as e:
            log.fatal(
                'Invalid generation_delay value. Must be specified following ISO8601',
                e,
            )
            raise

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'
