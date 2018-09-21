import unittest
from freezegun import freeze_time

from schedule import Schedule

class TestSchedule(unittest.TestCase):
    def setUp(self):
        self.schedule = Schedule()

    @freeze_time("2018-09-21")
    def test_bright_schedule_during_school(self):
        self.schedule.handleScheduleDisplay()
        self.assertEqual(self.schedule.scheduleTable.opacity, 1)

    @freeze_time("2018-09-22")
    def test_light_schedule_on_saturday(self):
        self.schedule.handleScheduleDisplay()
        self.assertEqual(self.schedule.scheduleTable.opacity, 0.1)
        
    @freeze_time("2018-09-22")
    def test_light_schedule_on_sunday(self):
        self.schedule.handleScheduleDisplay()
        self.assertEqual(self.schedule.scheduleTable.opacity, 0.1)        
        
if __name__ == '__main__':
    unittest.main()
    