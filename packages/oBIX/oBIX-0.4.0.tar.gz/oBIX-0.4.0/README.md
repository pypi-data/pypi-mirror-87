oBIX
=======================

A client package for interacting with oBIX(Open Building Information Exchange)

Installation
-----

```bash
pip install oBIX
```

sample
-----

```python
import unittest
from oBIX.client.client import Client, DataType
from datetime import datetime, timezone, timedelta


class ClientTest(unittest.TestCase):
    client = Client("127.0.0.1", "userName", "password", port=4430)

    def test_read_point(self):
        point = self.client.read_point("/config/AHU1/OutDoorTemp/")
        self.assertTrue(isinstance(point, dict))

    def test_read_point_value(self):
        point = self.client.read_point_value("/config/AHU1/OutDoorTemp/")
        self.assertTrue(isinstance(point, float))

    def test_set_point_value(self):
        point_path = "/config/AHU1/OutDoorTemp"
        point_set_value = 19
        set_result = self.client.set_point_value(point_path, point_set_value, DataType.real)
        self.assertEqual(set_result, "OK")
        point = self.client.read_point_value(point_path)  # 再次读取验证
        self.assertEqual(point, point_set_value)

    def test_set_point_auto(self):
        point_path = "/config/AHU1/OutDoorTemp"
        set_result = self.client.set_point_auto(point_path, DataType.real)
        self.assertEqual(set_result, "OK")

    def test_read_history(self):
        history = self.client.read_history("Station02", "OutDoorTemp",
                                           datetime(2020, 9, 7, 13, 10,  tzinfo=timezone(timedelta(hours=8))),
                                           datetime(2020, 9, 7, 13, 20,  tzinfo=timezone(timedelta(hours=8))))
        self.assertTrue(len(history) > 0)

        limit_num = 9
        history = self.client.read_history("Station02", "OutDoorTemp",
                                           datetime(2020, 9, 7, 13, 10, tzinfo=timezone(timedelta(hours=8))),
                                           limit=limit_num)
        self.assertTrue(len(history) == limit_num)

```