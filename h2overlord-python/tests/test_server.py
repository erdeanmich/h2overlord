import unittest
from unittest.mock import MagicMock

import pendulum


class MyTestCase(unittest.TestCase):

    def test_initial_state(self):
        time = '17:00'
        dt = pendulum.parse(time)
        print(dt.to_time_string())
        dt = dt.add(minutes=2)
        print(dt.to_time_string())

    
if __name__ == '__main__':
    unittest.main()
