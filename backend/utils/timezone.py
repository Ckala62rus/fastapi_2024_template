#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zoneinfo

from datetime import datetime

from core.config import settings


class TimeZone:
    def __init__(self, tz: str = settings.DATETIME_TIMEZONE):
        self.tz_info = zoneinfo.ZoneInfo(tz)

    def now(self) -> datetime:
        """
        :return:
        """
        return datetime.now(self.tz_info)

    def f_datetime(self, dt: datetime) -> datetime:
        """
        :param dt:
        :return:
        """
        return dt.astimezone(self.tz_info)

    def f_str(self, date_str: str, format_str: str = settings.DATETIME_FORMAT) -> datetime:
        """
        :param date_str:
        :param format_str:
        :return:
        """
        return datetime.strptime(date_str, format_str).replace(tzinfo=self.tz_info)

    def datetime_to_format(self, dt: datetime, format_str: str = settings.DATETIME_FORMAT) -> str:
        return dt.strftime(format_str)


timezone = TimeZone()
