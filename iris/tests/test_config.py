import unittest
import textwrap
import yaml

from iris.config import Configuration


class ConfigurationTests(unittest.TestCase):
    def load_yaml(self, yml):
        return Configuration(yaml.load(textwrap.dedent(yml)))

    def test_setdefault_without_previous_value(self):
        config = Configuration({
            'nested': {}
        })
        config.setdefault('foo', 1)
        self.assertEqual(config.get('foo'), 1)
        config.setdefault('nested.foo', 2)
        self.assertEqual(config.get('nested.foo'), 2)

    def test_setdefault_with_previous_value(self):
        config = Configuration({
            'foo': 1,
            'nested': {
                'foo': 2
            }
        })
        config.setdefault('foo', 0)
        self.assertEqual(config.get('foo'), 1)
        config.setdefault('nested.foo', 0)
        self.assertEqual(config.get('nested.foo'), 2)

    def test_get_missing_key(self):
        config = Configuration({'a': {'b': 1}, 'c': None})

        self.assertIsNone(config.get('x'))
        self.assertEqual(config.get('x', 2), 2)

        self.assertIsNone(config.get('x.x'), None)
        self.assertEqual(config.get('x.x', 2), 2)

        self.assertIsNone(config.get('c.x'), None)
        self.assertEqual(config.get('c.x', 2), 2)

    def test_set_in_empty_sections(self):
        config = self.load_yaml("""
        foo:
        """)
        # yaml doesn't know that we expect `foo` to be a dict
        self.assertIsNone(config.get('foo'))
        config.set('foo.bar', 1)
        self.assertEqual(config.get('foo.bar'), 1)

    def test_update(self):
        config = Configuration({'a': 1, 'b': {'c': 2}})
        config.update({'a': 2})
        self.assertEqual(config.get('a'), 2)
        self.assertEqual(config.get('b.c'), 2)
