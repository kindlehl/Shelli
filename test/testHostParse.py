import os
import copy
import unittest

from shelli import *

defaults = host.default_options()

class TestHostParse(unittest.TestCase):
    def setUp(self):       
        yaml = conf.YAMLoader(path='test/simple.yml')
        self.hosts = host.create_hosts_from_yaml(yaml)

    def test_default_hash(self):
        for h in self.hosts:
            if h.hostname == 'ns2':
                self.assertEqual(h.options, defaults)

    def test_string_as_host(self):
        found_ns2 = False
        for h in self.hosts:
            if h.hostname == 'ns2':
                self.assertEqual(h.options, defaults)
                found_ns2 = True
        self.assertTrue(found_ns2)
    
    def test_custom_hash(self):
        for h in self.hosts:
            if h.hostname == 'fiat':
                custom_options = copy.deepcopy(defaults)
                custom_options['auth_method'] = 'key'
                custom_options['password'] = 'shhhh'
                custom_options['port'] = 9000
                self.assertEqual(h.options, custom_options)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
