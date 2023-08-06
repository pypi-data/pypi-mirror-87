import datetime
from pandas import read_csv
from pandas._testing import assert_frame_equal
from pfit.CSVColMelter import CSVMelter
import unittest

class TestCSVMelter(unittest.TestCase):
    def setUp(self):
        self.csvMelter = CSVMelter()
        self.date = "2020-05-21"
        self.time = "08:37:55"
        self.isoTime = "2020-05-21T08:37:55-07:00"
        self.dateObj = datetime.datetime(year=2020, month=5, day=21, hour=8, minute=37, second=55, tzinfo=self.csvMelter.areaTimezone)
        self.timeObj = datetime.time(hour=8, minute=37, second=55)
        
    def test_get_iso_format(self):
        self.assertEqual(self.csvMelter.getISOFormat(self.date, self.time), self.isoTime)
        self.assertEqual(self.csvMelter.getISOFormat(self.dateObj, self.timeObj), self.isoTime)
        
        with self.assertRaises(ValueError):
            self.csvMelter.getISOFormat("2010/07/30", self.time)
            self.csvMelter.getISOFormat("2010/07/35", self.time)
            self.csvMelter.getISOFormat(self.date, "183459")
            self.csvMelter.getISOFormat(self.date, "83:78:00")
            self.csvMelter.getISOFormat(self.date, "0:0:99")  

    def test_parse_time_format(self):
        self.assertEqual(self.csvMelter.parseTimeFormat(datetime.datetime.combine(self.dateObj, self.timeObj)), (self.date, self.time))
        
        with self.assertRaises(ValueError):
            self.csvMelter.parseTimeFormat(self.date)
            self.csvMelter.parseTimeFormat(self.time)
            self.csvMelter.parseTimeFormat("2020-35-21T08:37:55-07:00")
            self.csvMelter.parseTimeFormat("2020-35-21 08:37:55")
            self.csvMelter.parseTimeFormat("2020-35-21T08:37:55-07:00")
            self.csvMelter.parseTimeFormat("2020-05-21T08:37:65-07:00")
            self.csvMelter.parseTimeFormat("2020-05-21 08:37:65-07:00")
            self.csvMelter.parseTimeFormat("2020-05-21 08:37:15-07:00")
            self.csvMelter.parseTimeFormat("2020-05-21 08:37:15")
            
    def test_melt_dataframe(self):
        wideFile = read_csv("test/sample/NTGS_Wide.csv", keep_default_na=False, float_precision="round_trip", parse_dates={"time": [4,5]}, date_parser=self.csvMelter.getISOFormat)
        wideMelt = read_csv("test/sample/NTGS_Wide_Melted.csv", keep_default_na=False, float_precision="round_trip")
        resMelt = self.csvMelter.meltDataframe(wideFile)
        assert_frame_equal(resMelt, wideMelt, check_exact=True)
    
    def test_stringify_depths(self):
        depthDict = {5: "5_m",
                    5.1: "5.1_m",
                    0.05: "0.05_m",
                    0: "0_m",
                    1.005: "1.005_m",
                    2.0: "2_m",
                    -5: "-5_m"}
        depths = ["5_m", "5.1_m", "0.05_m", "0_m", "1.005_m", "2_m", "-5_m"]
        resDict, resDepths = self.csvMelter.stringifyDepths(["colA", "colB", 5, 5.1, 0.05, 0, 1.005, "colH", 2.0, -5.0])
        self.assertDictEqual(depthDict, resDict)
        self.assertListEqual(depths, resDepths)
        
    def test_long_to_wide(self):
        longFile = read_csv("test/sample/NTGS_Long.csv", keep_default_na=False, float_precision="round_trip")
        longWidened = read_csv("test/sample/NTGS_Long_Widened.csv", keep_default_na=False, float_precision="round_trip")
        resWide = self.csvMelter.longToWide(longFile)
        assert_frame_equal(resWide, longWidened, check_exact=True)

if __name__ == "__main__":
    unittest.main()
