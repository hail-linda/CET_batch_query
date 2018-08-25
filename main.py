# -*- coding: utf-8 -*-
# Author = Linda

import pre
import unittest
from spider import CETBatchQuery
import os
import spider

if __name__ == '__main__':
    pre.xls_to_csv()
    pre.csv_IE()

    suite = unittest.TestSuite()

    tests = [CETBatchQuery("test_CET_batch_query")]
    suite.addTests(tests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)




