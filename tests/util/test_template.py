"""
tests.test_util
~~~~~~~~~~~~~~~~~

Tests Home Assistant util methods.
"""
# pylint: disable=too-many-public-methods
import unittest
import homeassistant.core as ha

from homeassistant.util import template


class TestUtilTemplate(unittest.TestCase):

    def setUp(self):  # pylint: disable=invalid-name
        self.hass = ha.HomeAssistant()

    def tearDown(self):  # pylint: disable=invalid-name
        """ Stop down stuff we started. """
        self.hass.stop()

    def test_referring_states_by_entity_id(self):
        self.hass.states.set('test.object', 'happy')
        self.assertEqual(
            'happy',
            template.render(self.hass, '{{ states.test.object.state }}'))

    def test_iterating_all_states(self):
        self.hass.states.set('test.object', 'happy')
        self.hass.states.set('sensor.temperature', 10)

        self.assertEqual(
            '10happy',
            template.render(
                self.hass,
                '{% for state in states %}{{ state.state }}{% endfor %}'))

    def test_iterating_domain_states(self):
        self.hass.states.set('test.object', 'happy')
        self.hass.states.set('sensor.back_door', 'open')
        self.hass.states.set('sensor.temperature', 10)

        self.assertEqual(
            'open10',
            template.render(
                self.hass,
                '{% for state in states.sensor %}{{ state.state }}{% endfor %}'))

    def test_rounding_value(self):
        self.hass.states.set('sensor.temperature', 12.78)

        self.assertEqual(
            '12.8',
            template.render(
                self.hass,
                '{{ states.sensor.temperature.state | round(1) }}'))

    def test_rounding_value2(self):
        self.hass.states.set('sensor.temperature', 12.72)

        self.assertEqual(
            '127',
            template.render(
                self.hass,
                '{{ states.sensor.temperature.state | multiply(10) | round }}'))

    def test_passing_vars_as_keywords(self):
        self.assertEqual(
            '127', template.render(self.hass, '{{ hello }}', hello=127))

    def test_passing_vars_as_vars(self):
        self.assertEqual(
            '127', template.render(self.hass, '{{ hello }}', {'hello': 127}))

    def test_render_with_possible_json_value_with_valid_json(self):
        self.assertEqual(
            'world',
            template.render_with_possible_json_value(
                self.hass, '{{ value_json.hello }}', '{"hello": "world"}'))

    def test_render_with_possible_json_value_with_invalid_json(self):
        self.assertEqual(
            '',
            template.render_with_possible_json_value(
                self.hass, '{{ value_json }}', '{ I AM NOT JSON }'))