"""
测试作息时间管理
"""
import pytest
from datetime import datetime
from nwafu_task_feishu import NWSUAFSchedule


class TestNWSUAFSchedule:
    """测试作息时间类"""

    def test_is_summer_time_may(self):
        """5 月属于夏令时"""
        date = datetime(2026, 5, 1)
        assert NWSUAFSchedule.is_summer_time(date) is True

        date = datetime(2026, 5, 31)
        assert NWSUAFSchedule.is_summer_time(date) is True

    def test_is_summer_time_september(self):
        """9 月属于夏令时"""
        date = datetime(2026, 9, 1)
        assert NWSUAFSchedule.is_summer_time(date) is True

        date = datetime(2026, 9, 30)
        assert NWSUAFSchedule.is_summer_time(date) is True

    def test_is_summer_time_april(self):
        """4 月属于冬令时"""
        date = datetime(2026, 4, 1)
        assert NWSUAFSchedule.is_summer_time(date) is False

        date = datetime(2026, 4, 30)
        assert NWSUAFSchedule.is_summer_time(date) is False

    def test_is_summer_time_october(self):
        """10 月属于冬令时"""
        date = datetime(2026, 10, 1)
        assert NWSUAFSchedule.is_summer_time(date) is False

        date = datetime(2026, 10, 31)
        assert NWSUAFSchedule.is_summer_time(date) is False

    def test_get_times_summer(self):
        """获取夏令时作息"""
        date = datetime(2026, 6, 15)
        times = NWSUAFSchedule.get_times(date)
        assert times['5-6'] == ('14:30', '16:10')
        assert times['7-8'] == ('16:30', '18:10')

    def test_get_times_winter(self):
        """获取冬令时作息"""
        date = datetime(2026, 12, 15)
        times = NWSUAFSchedule.get_times(date)
        assert times['5-6'] == ('14:00', '15:40')
        assert times['7-8'] == ('16:00', '17:40')
