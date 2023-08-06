import pandas as pd
from pfit.FileDataChecker import FileDataChecker
import unittest

class TestFileDataChecker(unittest.TestCase):
    def setUp(self):
        self.checker = FileDataChecker()
        self.rx_time = self.checker.TIME_RGX
        self.rx_metre = self.checker.METRE_RGX
        self.expected = ["project_name", "site_id", "latitude", "longitude", "date_YYYY-MM-DD", "time_HH:MM:SS"]
        
    def test_time_regex(self):
        self.assertRegex("00:00:00", self.rx_time)
        self.assertRegex("0:00:00", self.rx_time)
        self.assertRegex("12:59:59", self.rx_time)
        self.assertRegex("12:59:00", self.rx_time)
        self.assertRegex("13:00:00", self.rx_time)
        self.assertRegex("23:00:00", self.rx_time)
        self.assertRegex("23:59:59", self.rx_time)
        self.assertNotRegex("24:00:00", self.rx_time)
        self.assertNotRegex("99:99:99", self.rx_time)
        self.assertNotRegex("01:00:60", self.rx_time)
        self.assertNotRegex("10:00:99", self.rx_time)
        self.assertNotRegex("10:95:58", self.rx_time)
        self.assertNotRegex("-12:22:58", self.rx_time)
        self.assertNotRegex("2:2:8", self.rx_time)
        self.assertRegex("2:32:38", self.rx_time)
        self.assertRegex("9:37:54", self.rx_time)

    def test_metre_regex(self):
        self.assertRegex("0.05_m", self.rx_metre)
        self.assertRegex("15_m", self.rx_metre)
        self.assertRegex("10_m", self.rx_metre)
        self.assertRegex("10.0_m", self.rx_metre)
        self.assertRegex("10.000_m", self.rx_metre)
        self.assertRegex("0.000001_m", self.rx_metre)
        self.assertRegex("5.6_m", self.rx_metre)
        self.assertRegex("5.6_m", self.rx_metre)
        self.assertRegex("51321321331.6846548756735_m", self.rx_metre)
        self.assertRegex("0.0_m", self.rx_metre)
        self.assertRegex("99_m", self.rx_metre)
        self.assertRegex("-1_m", self.rx_metre)
        self.assertRegex("-1.0_m", self.rx_metre)
        self.assertRegex("-11111111.01231212131231232332_m", self.rx_metre)
        self.assertNotRegex("1_km", self.rx_metre)
        self.assertNotRegex("3_m ", self.rx_metre)
        self.assertNotRegex("3.0_m ", self.rx_metre)
        self.assertNotRegex(" 3.0_m", self.rx_metre)
        self.assertNotRegex(" 3_m", self.rx_metre)
        self.assertNotRegex("0.0.1_m", self.rx_metre)
        self.assertRegex("001.1_m", self.rx_metre)
        self.assertRegex("00.1_m", self.rx_metre)
        
    def test_date_format(self):
        with self.assertLogs("main") as context:
            self.checker.checkDateFmt("2002-123-20", 1)
            self.checker.checkDateFmt("2002/12/20", 1)
            self.checker.checkDateFmt("December 12, 2002", 1)
            self.checker.checkDateFmt("20090813", 1)
            self.checker.checkDateFmt("2009-08-33", 1)
            self.checker.checkDateFmt("1-08-03", 1)
            self.checker.checkDateFmt("2011-88-03", 1)
        self.assertEqual(len(context.output), 7)
            
    def test_extra_columns(self):
        with self.assertLogs("main") as context:
            self.checker.checkExtraColNames(["test"])
            self.checker.checkExtraColNames(self.expected + ["0.05a_m"])
            self.checker.checkExtraColNames(self.expected[:1] + ["timezone"] + self.expected[1:])
        self.assertEqual(len(context.output), 3)
        
    def test_col_order(self):
        with self.assertLogs("main") as context:
            self.checker.checkColNames(["a"])
            self.checker.checkColNames(["project_name", "latitude", "longitude", "date_YYYY-MM-DD", "time_HH:MM:SS"])
            self.checker.checkColNames(["site_id", "project_name", "latitude", "longitude", "date_YYYY-MM-DD", "time_HH:MM:SS"])
        # 7 errors because "a"
        # then "latitude", "longitude", "date_YYYY-MM-DD", "time_HH:MM:SS" are all out of the expected order
        # then "site_id" and "project_name" are not in the correct order but the rest of the columns are
        self.assertEqual(len(context.output), 7)

    def test_temperatures(self):
        with self.assertLogs("main") as context:
            self.checker.checkTemperatures("nan", 1)
            self.checker.checkTemperatures("a", 1)
        self.assertEqual(len(context.output), 2)
        
    def test_latitudes(self):
        with self.assertLogs("main") as context:
            self.checker.checkLatitude("abc", 1)
            self.checker.checkLatitude("91", 1)
            self.checker.checkLatitude("-91", 1)
        self.assertEqual(len(context.output), 3)     
        
    def test_longitudes(self):
        with self.assertLogs("main") as context:
            self.checker.checkLatitude("abc", 1)
            self.checker.checkLatitude("181", 1)
            self.checker.checkLatitude("-181", 1)
        self.assertEqual(len(context.output), 3)
        
    def test_unique_timestamps(self):
        dates = pd.Series(["2020-01-01", "2020-01-02", "2020-01-01"])
        times = pd.Series(["00:00:00", "00:02:00", "00:00:00"])
        with self.assertLogs("main") as context:
            self.checker.checkUniqueTimes(dates, times)
        self.assertEqual(len(context.output), 1)

if __name__ == "__main__":
    unittest.main()