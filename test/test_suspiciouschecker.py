#!/usr/bin/env python

import os
import sys
import unittest
from unittest_data_provider import data_provider
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cmsif_package.suspiciouschecker import SuspiciousChecker



class TestSuspiciousChecker(unittest.TestCase):

    bad_probes = lambda: (
        (["$l762 = 927;$GLOBALS['hb575a']=Array();global$hb575a;$hb575a=$GLOBALS;$"]),
        (["        eval($b43323ec[$GLOBALS['ucef98290'][20]]); "]),
        (["  var sh = CreateObject('WScript.Shell') "])
    )

    good_probes = lambda: (
        (["  return drupal_hmac_base64($value, $this->session_id . $private_key); "]),
        (["  return eval($value); "]),
        (["  require_once DRUPAL_ROOT . '/includes/bootstrap.inc'; drupal_bootstrap(DRUPAL_BOOTSTRAP_FULL); "])
    )

    @data_provider(bad_probes)
    def test_detects_malware(self, probe):
        checker = SuspiciousChecker()

        self.assertTrue(
            checker.is_file_containing_malicious_content(content=probe, file_name='test')
        )

    @data_provider(good_probes)
    def test_detects_clean_code(self, probe):
        checker = SuspiciousChecker()

        self.assertFalse(
            checker.is_file_containing_malicious_content(content=probe, file_name='test')
        )
