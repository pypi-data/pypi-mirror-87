import pandas as pd
from psense_common import PSenseParser
from psense_common.psense_parser import is_float, SensorDataFormat
import unittest
from unittest.mock import patch, MagicMock, Mock
from datetime import datetime, timedelta
import pytz


def is_dst():
    """Determine whether or not Daylight Savings Time (DST)
    is currently in effect"""

    x = datetime(
        datetime.now().year, 1, 1, 0, 0, 0, tzinfo=pytz.timezone("US/Eastern")
    )  # Jan 1 of this year
    y = datetime.now(pytz.timezone("US/Eastern"))

    # if DST is in effect, their offsets will be different
    return not (y.utcoffset() == x.utcoffset())


class TestPSenseParser(unittest.TestCase):
    def setUp(self):
        self.parser = PSenseParser(debugmode=True)
        pass

    def test_is_float(self):
        self.assertTrue(is_float(0))
        self.assertTrue(is_float("0"))
        self.assertTrue(is_float("0.5"))
        self.assertFalse(is_float("A"))
        self.assertFalse(is_float({"value": 0.5}))
        self.assertFalse(is_float([0.5]))

    def test_sensordataformat(self):
        obj = SensorDataFormat()

        # empty init
        self.assertIsNone(obj.name)
        self.assertEqual(obj.delimiter, ",")
        self.assertIsNone(obj.type_is_sensor)
        self.assertEqual(obj.has_timestamp, True)

        self.assertIsNone(obj.get_key("signal1"))
        self.assertIsNone(obj.get_header("signal1"))
        self.assertIsNone(obj.get_index("signal1"))
        self.assertEqual(obj.data_headers(), [])
        self.assertEqual(obj.data_keys(), [])
        self.assertEqual(obj.data_indices(), [])

        obj.set_key("signal1", ("test", 20))
        self.assertEqual(obj.get_key("signal1"), ("test", 20))
        self.assertEqual(obj.get_header("signal1"), "test")
        self.assertEqual(obj.get_index("signal1"), 20)

        self.assertEqual(obj.data_headers(), ["test"])
        self.assertEqual(obj.data_keys(), ["signal1"])
        self.assertEqual(obj.data_indices(), [20])

        obj = SensorDataFormat(
            name="test",
            delimiter="\t",
            has_timestamp=False,
            columns=dict(
                type=("TYPE", 1),
                timestamp=("timestamp", 0),
                signal1=("SIGNAL1", 2),
                vout1=("VOUT1", 4),
                enable1=("enable1", 3),
            ),
        )
        self.assertEqual(obj.name, "test")
        self.assertEqual(obj.delimiter, "\t")
        self.assertEqual(obj.has_timestamp, False)
        self.assertEqual(obj.get_key("signal1"), ("SIGNAL1", 2))
        self.assertIsNone(obj.get_key("doesntexist"))
        self.assertEqual(obj.get_header("signal1"), "SIGNAL1")
        self.assertEqual(obj.get_index("signal1"), 2)
        self.assertListEqual(
            obj.data_headers(), ["timestamp", "TYPE", "SIGNAL1", "enable1", "VOUT1"]
        )
        self.assertListEqual(
            obj.data_keys(), ["timestamp", "type", "signal1", "enable1", "vout1"]
        )
        self.assertListEqual(obj.data_indices(), [1, 0, 3, 4, 2])

    def test_force_source(self):
        self.assertRaises(IOError, self.parser.force_source, "not-a-real-data-type")
        type1 = "PSHIELD"
        self.parser.force_source(type1)
        self.assertEqual(self.parser.source, type1)
        type2 = "BWII-DL"
        self.parser.force_source(type2)
        self.assertEqual(self.parser.source, type2)

    def test_find_header_text(self):
        mock_type = "PSHIELD"
        search_string = self.parser.header_text[mock_type]

        m_open = MagicMock()
        m_methods = Mock()
        m_methods.tell.side_effect = [1, 2, 3, 4, 5, 15, 15]
        m_methods.readline.side_effect = [
            "random",
            "random",
            search_string,
            "random",
            "random",
            "random",
        ]
        m_open().__enter__.return_value = m_methods

        with patch("builtins.open", m_open, create=True):
            with patch("os.path.getsize", return_value=11):
                self.assertTrue(
                    self.parser.find_header_text("fake_file", search_string)
                )
                self.assertFalse(
                    self.parser.find_header_text(
                        "fake_file", "string-that-doesnt-exist"
                    )
                )

    def test_identify_file_source(self):

        self.assertRaises(
            FileNotFoundError, self.parser.identify_file_source, "fake_file"
        )

        self.parser.identify_file_source(fpath="tests/pshield_example")
        self.assertEqual(self.parser.source, "PSHIELD")
        self.parser.identify_file_source(fpath="tests/gamry_example")
        self.assertEqual(self.parser.source, "EXPLAIN")
        self.parser.identify_file_source("tests/__init__.py")
        self.assertEqual(self.parser.source, None)

    def test_read_variable_header_file(self):
        data, header = self.parser.read_variable_header_file(
            "tests/__init__.py", "NOT_FOUND_HEADER", sep=","
        )
        self.assertIsNone(data)
        self.assertIsNone(header)

        data, header = self.parser.read_variable_header_file(
            "tests/web1chan_example", "timestamp,Raw1,Vout1", sep=","
        )
        self.assertIsInstance(data, pd.DataFrame)
        self.assertListEqual(
            list(data.columns), ["timestamp", "Raw1", "Vout1", "Filt1"]
        )
        self.assertEqual(data.shape, (10, 4))
        self.assertEqual(len(header), 190)

    def test_parse_record(self):
        starting_time = datetime.now()

        self.parser.force_source("BWII-MINI")
        data = ",".join(
            [
                starting_time.isoformat(),
                "sensor_record",
                "10",
                "1.0",
                "1000",
                "500",
                "1",
                "0",
                "2.0",
                "1010",
                "1",
                "0",
                "3.0",
                "1500",
                "1",
                "0",
                "3300",
            ]
        )
        res = self.parser.parse_record(data)
        self.assertTrue(
            datetime.fromisoformat(res[0]) - starting_time < timedelta(seconds=3)
        )
        self.assertEqual(res[1], [0.5, 0.51, 1.0])
        self.assertEqual(res[2], [1.0, 2.0, 3.0])
        self.assertEqual(res[3], [True, True, True])
        data = ",".join(
            [
                starting_time.isoformat(),
                "sensor_record",
                "10",
                "1.0",
                "1000",
                "500",
                "0",
                "0",
                "2.0",
                "1010",
                "0",
                "0",
                "3.0",
                "1500",
                "0",
                "0",
                "3300",
            ]
        )
        res = self.parser.parse_record(data)
        self.assertEqual(res[3], [False, False, False])

        self.parser.force_source("BWII-DL")
        data = ",".join(
            [
                starting_time.isoformat(),  # timestamp
                "sensor_record",  # type
                "1",  # rnum
                "1",  # i
                ".2",  # vw
                ".1",  # vr
                "0",  # vc
                "1",  # on
                "0",  # disc
                "10",  # i
                ".4",  # vw
                ".2",  # vr
                ".1",  # vc
                "1",  # on
                "0",  # disc
                "0",  # batt
                "3260",  # vbatt
            ]
        )
        res = self.parser.parse_record(data)
        self.assertTrue(
            datetime.fromisoformat(res[0]) - starting_time < timedelta(seconds=3)
        )
        self.assertEqual(res[1], [0.0001, 0.0002])
        self.assertEqual(res[2], [1.0, 10.0])
        self.assertEqual(res[3], [True, True])
        data = ",".join(
            [
                starting_time.isoformat(),
                "sensor_record",  # type
                "1",  # rnum
                "1",  # i1
                ".2",  # vw
                ".1",  # vr
                "0",  # vc
                "0",  # on
                "0",  # disc
                "10",  # i
                ".4",  # w
                ".2",  # r
                ".1",  # c
                "0",  # on
                "0",  # disc
                "0",  # batt
                "3260",  # vbatt
            ]
        )
        res = self.parser.parse_record(data)
        self.assertEqual(res[3], [False, False])

        data = "1, 1554417874.0000026, 12.51"
        self.parser.force_source("PSHIELD")
        res = self.parser.parse_record(data)
        self.assertEqual(res[0], "2019-04-04T14:44:34.000003")  # local time, not utc
        self.assertEqual(res[1], [None])
        self.assertEqual(res[2], [12.51])
        self.assertEqual(res[3], [True])

        data = "0.399550	7.3E-9"
        self.parser.force_source("VFP")
        res = self.parser.parse_record(data)
        self.assertTrue(
            datetime.fromisoformat(res[0]) - starting_time < timedelta(seconds=3)
        )
        self.assertEqual(res[1], [0.39955])
        self.assertEqual(res[2], [7.3])
        self.assertEqual(res[3], [True])

        data = "2015-12-26 20:19:18,0.72,0.3,0.72"
        self.parser.force_source("WEB-APP")
        res = self.parser.parse_record(data)
        self.assertEqual(res[0], "2015-12-26T20:19:18")
        self.assertEqual(res[1], [0.3])
        self.assertEqual(res[2], [0.72])
        self.assertTrue(res[3])

        data = "2020-02-10 10:59:24,0.83,0.507,-7.89,-0.456,5.05,0.123,0.83,1.3,0.03"
        self.parser.force_source("WEB-APP")
        res = self.parser.parse_record(data)
        self.assertEqual(res[0], "2020-02-10T10:59:24")
        self.assertEqual(res[1], [0.507, -0.456, 0.123])
        self.assertEqual(res[2], [0.83, -7.89, 5.05])
        self.assertEqual(res[3], [True] * 3)

        res = self.parser.parse_record(data, num_channels=2)
        self.assertEqual(res[0], "2020-02-10T10:59:24")
        self.assertEqual(res[1], [0.507, -0.456])
        self.assertEqual(res[2], [0.83, -7.89])
        self.assertEqual(res[3], [True] * 2)

        data = "1.000e+1, 4.020e-8, 5.779e-8, 6.402e-8, 7.063e-8"
        self.parser.force_source("CHI")
        res = self.parser.parse_record(data)
        self.assertEqual(res[1], [None] * 4)
        self.assertEqual(res[2], [4.02e-8, 5.779e-8, 6.402e-8, 7.063e-8])
        self.assertEqual(res[3], [True] * 4)
        data = "1.000e+1, 1e-8, 2e-8, 3e-8, 4e-8, -1e-8, -2e-8, -3e-8, -4e-8"
        res = self.parser.parse_record(data)
        self.assertEqual(res[1], [None] * 8)
        self.assertEqual(res[2], [1e-8, 2e-8, 3e-8, 4e-8, -1e-8, -2e-8, -3e-8, -4e-8])
        self.assertEqual(res[3], [True] * 8)

    def test_load_no_source(self):
        testfile = "tests/pshield_example"

        # fake source
        self.parser.source = "fake-source"
        self.assertRaises(ValueError, self.parser.load_rawfile, testfile, None, None)

    def test_load_pshield(self):
        testfile = "tests/pshield_example"
        # pshield file
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(df["vout1"].iloc[-1], 0.5)
        self.assertEqual(df["signal1"].iloc[-1], 5.29)
        self.assertEqual(
            df["timestamp"].iloc[-1], pd.Timestamp("2018-07-23 16:28:08.229594946")
        )

    def test_load_bwii_script(self):
        # psense format (bwii-instrument.py)
        testfile = "tests/psense_example"
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(df["vout1"].iloc[-1], 0)
        self.assertEqual(df["signal1"].iloc[-1], 1)
        self.assertEqual(df["vout2"].iloc[-1], 2)
        self.assertEqual(df["signal2"].iloc[-1], 3)
        self.assertEqual(df["timestamp"].iloc[-1], pd.Timestamp("2019-03-04T13:08:54"))

        self.assertTrue(df["enable1"].iloc[-1])
        self.assertTrue(df["enable2"].iloc[0])

    def test_load_bwii_dl(self):
        # bwii format (bwii-dl)
        testfile = "tests/bwii_example"
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(df["vout1"].iloc[-1], 0.487)
        self.assertEqual(df["signal1"].iloc[-1], 1.76)
        self.assertEqual(df["vout2"].iloc[-1], 0)
        self.assertEqual(df["signal2"].iloc[-1], 0)
        self.assertEqual(df["timestamp"].iloc[-1], pd.Timestamp("2019-03-04 16:37:42"))

        start_time = "2019/01/01 12:00"
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, False))
        df = self.parser.data
        self.assertEqual(df["vout1"].iloc[-1], 0.487)
        self.assertEqual(df["signal1"].iloc[-1], 1.76)
        self.assertEqual(df["vout2"].iloc[-1], 0)
        self.assertEqual(df["signal2"].iloc[-1], 0)
        self.assertEqual(df["timestamp"].iloc[-1], pd.Timestamp("2019-01-01 12:13:43"))

        self.assertTrue(self.parser.load_rawfile(testfile, start_time, True))
        df = self.parser.data
        self.assertEqual(df["vout1"].iloc[-1], 0.487)
        self.assertEqual(df["signal1"].iloc[-1], 1.76)
        self.assertEqual(df["vout2"].iloc[-1], 0)
        self.assertEqual(df["signal2"].iloc[-1], 0)
        self.assertEqual(df["timestamp"].iloc[-1], pd.Timestamp("2019-01-01 12:00:00"))

    def test_load_bwii_mini(self):
        testfile = "tests/bwii_mini_example"
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(df["vout1"].iloc[1], 0.501)
        self.assertEqual(df["signal1"].iloc[1], 0.175)
        self.assertEqual(df["vout2"].iloc[1], 0.502)
        self.assertEqual(df["signal2"].iloc[1], 1.75)
        self.assertEqual(df["vout3"].iloc[1], 1)
        self.assertEqual(df["signal3"].iloc[1], 17.5)

        self.assertEqual(df["vout1"].iloc[-1], 0.501)
        self.assertEqual(df["signal1"].iloc[-1], 175)
        self.assertEqual(df["vout2"].iloc[-1], -0.488)
        self.assertEqual(df["signal2"].iloc[-1], 0)
        self.assertEqual(df["vout3"].iloc[-1], -0.488)
        self.assertEqual(df["signal3"].iloc[-1], 0)
        self.assertEqual(df["timestamp"].iloc[-1], pd.Timestamp("2020-01-01 19:32:17"))

        self.assertTrue(df["enable1"].iloc[0])
        self.assertFalse(df["enable2"].iloc[0])
        self.assertFalse(df["enable3"].iloc[0])
        self.assertFalse(df["enable3"].iloc[-1])

        start_time = "2019/01/01 12:00"
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, False))
        df = self.parser.data
        self.assertEqual(df["timestamp"].iloc[0], pd.Timestamp("2019-01-01 12:00:00"))
        self.assertEqual(df["timestamp"].iloc[-1], pd.Timestamp("2019-01-01 12:02:19"))

        self.assertTrue(self.parser.load_rawfile(testfile, start_time, True))
        df = self.parser.data
        self.assertEqual(df["timestamp"].iloc[0], pd.Timestamp("2019-01-01 11:57:41"))
        self.assertEqual(df["timestamp"].iloc[-1], pd.Timestamp("2019-01-01 12:00:00"))

    def test_load_bwii_util(self):
        # files downloaded from BWII_Util.exe have extra whitespace. Make sure they are loaded properly
        testfile = "tests/bwii_util_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "BWII-MINI")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))

        df = self.parser.data
        self.assertEqual(len(df.index), 20)
        self.assertEqual(df["signal1"].iloc[0], 41.5901)
        self.assertEqual(df["signal2"].iloc[0], 0.0520)
        self.assertEqual(df["signal3"].iloc[0], 0.0500)
        self.assertEqual(df["signal1"].iloc[-1], 9.5240)
        self.assertEqual(df["signal2"].iloc[-1], 0.0510)
        self.assertEqual(df["signal3"].iloc[-1], -34.5678)

        self.assertEqual(df["vout1"].iloc[0], 0.505)
        self.assertEqual(df["vout2"].iloc[0], 0.501)
        self.assertEqual(df["vout3"].iloc[0], 0.500)
        self.assertEqual(df["vout1"].iloc[-1], 0.505)
        self.assertEqual(df["vout2"].iloc[-1], -0.500)
        self.assertEqual(df["vout3"].iloc[-1], 0.499)

        self.assertTrue(df["enable1"].iloc[0])
        self.assertTrue(df["enable2"].iloc[0])
        self.assertTrue(df["enable3"].iloc[0])
        self.assertTrue(df["enable1"].iloc[-1])
        self.assertFalse(df["enable2"].iloc[-1])
        self.assertFalse(df["enable3"].iloc[-1])

    def test_load_webapp_v1v2(self):
        # web app file
        testfile = "tests/web1chan_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "WEB-APP")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(len(df.columns), 4)

        self.assertEqual(df["vout1"].iloc[-1], 0.3)
        self.assertEqual(df["signal1"].iloc[-1], 2.77)
        self.assertTrue(df["enable1"].iloc[-1])

        self.assertEqual(df["timestamp"].iloc[-1], pd.Timestamp("2019-07-26 17:12:30"))

        testfile = "tests/web2chan_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "WEB-APP")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(len(df.columns), 7)

        self.assertEqual(df["vout1"].iloc[-1], 0.5)
        self.assertEqual(df["signal1"].iloc[-1], 5)
        self.assertTrue(df["enable1"].iloc[-1])

        self.assertEqual(df["vout2"].iloc[-1], 0.4)
        self.assertEqual(df["signal2"].iloc[-1], 15)
        self.assertTrue(df["enable2"].iloc[-1])

        self.assertEqual(df["timestamp"].iloc[-1], pd.Timestamp("2019-07-09 17:35:24"))

        testfile = "tests/web3chan_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "WEB-APP")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(len(df.columns), 10)

        self.assertEqual(df["vout1"].iloc[-1], 0.508)
        self.assertEqual(df["signal1"].iloc[-1], 2.48)
        self.assertTrue(df["enable1"].iloc[-1])

        self.assertEqual(df["vout2"].iloc[-1], -0.501)
        self.assertEqual(df["signal2"].iloc[-1], 0.03)
        self.assertTrue(df["enable2"].iloc[-1])

        self.assertEqual(df["timestamp"].iloc[-1], pd.Timestamp("2020-02-10 11:04:54"))

    def test_load_vfp600(self):
        # vfp600
        start_time = "2019/01/01 12:00"
        testfile = "tests/vfp_example"
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, False))
        df = self.parser.data
        self.assertEqual(df["timestamp"].iloc[0], pd.Timestamp(start_time))
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, True))
        df = self.parser.data
        self.assertTrue(df["timestamp"].iloc[0] < pd.Timestamp(start_time))
        ts = [df["timestamp"].iloc[-1], pd.Timestamp(start_time)]
        self.assertTrue(pd.Timedelta(max(ts) - min(ts)).seconds < 1)

        self.assertEqual(df["vout1"].iloc[-1], 0.39955)
        self.assertEqual(round(df["signal1"].iloc[-1], 2), 3.8)
        self.assertTrue(df["enable1"].iloc[-1])

        # vfp600 #2
        start_time = "2019/01/01 12:00"
        testfile = "tests/vfp_example2"
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, False))
        df = self.parser.data
        self.assertEqual(df["timestamp"].iloc[0], pd.Timestamp(start_time))
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, True))
        df = self.parser.data
        self.assertTrue(df["timestamp"].iloc[0] < pd.Timestamp(start_time))
        ts = [df["timestamp"].iloc[-1], pd.Timestamp(start_time)]
        self.assertTrue(pd.Timedelta(max(ts) - min(ts)).seconds < 1)

        self.assertEqual(df["vout1"].iloc[-2], 0.101215)
        self.assertEqual(round(df["signal1"].iloc[-2], 2), 0.19)
        self.assertEqual(df["vout1"].iloc[-1], 0.101219)
        self.assertEqual(round(df["signal1"].iloc[-1], 3), 0.244)
        self.assertTrue(df["enable1"].iloc[-1])

    def test_load_explain(self):
        # gamry explain
        start_time = "2018/09/11 12:00"
        testfile = "tests/gamry_example"
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, False))
        df = self.parser.data
        self.assertEqual(df["timestamp"].iloc[0], pd.Timestamp(start_time))
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, True))
        df = self.parser.data
        self.assertEqual(df["timestamp"].iloc[0], pd.Timestamp(start_time))

        self.assertEqual(df["vout1"].iloc[-1], 0.499654)
        self.assertEqual(df["signal1"].iloc[-1], 3.60525)
        self.assertTrue(df["enable1"].iloc[-1])

    def test_load_chinstruments(self):
        testfile = "tests/chinstruments_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "CHI")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data

        self.assertEqual(df["timestamp"].iloc[0], pd.Timestamp("2020/07/15 15:27:12"))
        self.assertEqual(df["timestamp"].iloc[-1], pd.Timestamp("2020/07/15 15:37:12"))

        self.assertEqual(df["vout1"].iloc[0], 0.5)
        self.assertEqual(df["vout1"].iloc[-1], 0.5)
        self.assertEqual(df["vout2"].iloc[0], -0.5)
        self.assertEqual(df["vout2"].iloc[-1], -0.5)
        self.assertEqual(df["vout3"].iloc[0], -0.3)
        self.assertEqual(df["vout3"].iloc[-1], -0.3)
        self.assertEqual(df["vout4"].iloc[0], 1.0)
        self.assertEqual(df["vout4"].iloc[-1], 1.0)

        self.assertTrue(df["enable1"].iloc[-1])
        self.assertTrue(df["enable1"].iloc[0])
        self.assertTrue(df["enable2"].iloc[-1])
        self.assertTrue(df["enable2"].iloc[0])
        self.assertTrue(df["enable3"].iloc[-1])
        self.assertTrue(df["enable3"].iloc[0])
        self.assertTrue(df["enable4"].iloc[-1])
        self.assertTrue(df["enable4"].iloc[0])

        self.assertEqual(df["signal1"].iloc[-1], 0.3608)
        self.assertEqual(df["signal2"].iloc[-1], 20.09)
        self.assertEqual(df["signal3"].iloc[-1], 8)
        self.assertEqual(df["signal4"].iloc[-1], 39.8)
