import unittest
from unittest.mock import patch
import time

from It1_interfaces.KeyboardListener import KeyboardListener

class TestKeyboardListener(unittest.TestCase):

    def setUp(self):
        self.received_directions = []

    def callback(self, direction):
        self.received_directions.append(direction)

    @patch('your_module.keyboard.is_pressed')
    def test_blue_listener(self, mock_is_pressed):
        mock_is_pressed.side_effect = lambda key: key == 'w'

        KeyboardListener.start_blue_listener(self.callback)

        time.sleep(0.1)  # תן קצת זמן ל-thread לרוץ

        # עצור את side_effect מלהחזיר true
        mock_is_pressed.side_effect = lambda key: False

        self.assertIn('U', self.received_directions)

    @patch('your_module.keyboard.is_pressed')
    def test_green_listener(self, mock_is_pressed):
        mock_is_pressed.side_effect = lambda key: key == 'right'

        KeyboardListener.start_green_listener(self.callback)

        time.sleep(0.1)

        mock_is_pressed.side_effect = lambda key: False

        self.assertIn('R', self.received_directions)

