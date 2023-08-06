import unittest
import os
import shutil

from aistac.components.aistac_commons import AnalyticsCommons, AistacCommons
from aistac.properties.property_manager import PropertyManager


class CommonsTest(unittest.TestCase):

    def setUp(self):
        os.environ['HADRON_PM_PATH'] = os.path.join('work', 'config')
        os.environ['HADRON_DEFAULT_PATH'] = os.path.join('work', 'data')
        try:
            os.makedirs(os.environ['HADRON_PM_PATH'])
            os.makedirs(os.environ['HADRON_DEFAULT_PATH'])
        except:
            pass
        PropertyManager._remove_all()

    def tearDown(self):
        try:
            shutil.rmtree('work')
        except:
            pass

    def test_is_list_equal(self):
        a = [1, 4, 2, 1, 4]
        b = [4, 2, 4, 1, 1]
        self.assertTrue(AistacCommons.is_list_equal(a,b))
        b = [4, 2, 4, 2, 1]
        self.assertFalse(AistacCommons.is_list_equal(a, b))

    def test_resize_list(self):
        seq = [1,2,3,4]
        for size in range(10):
            result = AistacCommons.resize_list(seq=seq, resize=size)
            self.assertEqual(size, len(result))
            if len(result) >= 4:
                self.assertEqual(seq, AistacCommons.unique_list(result))

    def test_dict_builder(self):
        result = AistacCommons.param2dict()
        self.assertEqual({}, result)
        result = AistacCommons.param2dict(a=1, b='B')
        self.assertEqual({'a': 1, 'b': 'B'}, result)
        result = AistacCommons.param2dict(a=1, b=[1,2,3])
        self.assertEqual({'a': 1, 'b': [1, 2, 3]}, result)
        result = AistacCommons.param2dict(a={'A': 1})
        self.assertEqual({'a': {'A': 1}}, result)
        result = AistacCommons.param2dict(a=1, b=None)
        self.assertEqual({'a': 1}, result)

    def test_dict_with_missing(self):
        default = 'no value'
        sample = AistacCommons.dict_with_missing({}, default)
        result = sample['key']
        self.assertEqual(default, result)

    def test_analytics_structure(self):
        analysis = {'survived': {'associate': 'survived',
                                 'analysis': {'intent': {'selection': [0, 1],
                                                         'dtype': 'category',
                                                         'upper': 61.62,
                                                         'lower': 38.38,
                                                         'granularity': 2,
                                                         'weighting_precision': 2},
                                              'patterns': {'weight_pattern': [61.62, 38.38],
                                                           'sample_distribution': [549, 342]},
                                              'stats': {'nulls_percent': 0.0, 'outlier_percent': 0.0, 'sample': 891}}}}
        result = AnalyticsCommons(analysis=analysis, label='titanic_survived')
        self.assertEqual('titanic_survived', result.label)
        self.assertEqual('survived', result.associate)
        result = AnalyticsCommons(analysis=analysis)
        self.assertEqual('survived', result.label)
        self.assertEqual('survived', result.associate)
        analysis = {'associate': 'survived',
                    'analysis': {'intent': {'selection': [0, 1],
                                            'dtype': 'category',
                                            'upper': 61.62,
                                            'lower': 38.38,
                                            'granularity': 2,
                                            'weighting_precision': 2},
                                 'patterns': {'weight_pattern': [61.62, 38.38],
                                              'sample_distribution': [549, 342]},
                                 'stats': {'nulls_percent': 0.0, 'outlier_percent': 0.0, 'sample': 891}}}
        result = AnalyticsCommons(analysis=analysis, label='titanic_survived')
        self.assertEqual('titanic_survived', result.label)
        self.assertEqual('survived', result.associate)
        result = AnalyticsCommons(analysis=analysis)
        self.assertEqual('n/a', result.label)

    def test_analytics_structure_elements(self):
        analysis = {'survived': {'associate': 'survived',
                                 'analysis': {'intent': {'selection': [0, 1],
                                                         'dtype': 'category',
                                                         'upper': 61.62,
                                                         'lower': 38.38,
                                                         'granularity': 2,
                                                         'weighting_precision': 2},
                                              'patterns': {'weight_pattern': [61.62, 38.38],
                                                           'sample_distribution': [549, 342]},
                                              'stats': {'nulls_percent': 0.0, 'outlier_percent': 0.0, 'sample': 891}}}}
        result = AnalyticsCommons(analysis=analysis)
        self.assertEqual([0, 1], result.intent.selection)
        self.assertEqual('category', result.intent.dtype)
        self.assertEqual([61.62, 38.38], result.patterns.weight_pattern)
        self.assertEqual(891, result.stats.sample)

    def test_analytics_structure_items(self):
        analysis = {'intent': {'selection': [0, 1],
                               'dtype': 'category',
                               'upper': 61.62,
                               'lower': 38.38,
                               'granularity': 2,
                               'weighting_precision': 2},
                    'patterns': {'weight_pattern': [61.62, 38.38],
                                 'sample_distribution': [549, 342]},
                    'stats': {'nulls_percent': 0.0, 'outlier_percent': 0.0, 'sample': 891}}
        result = AnalyticsCommons(analysis=analysis)
        self.assertEqual([0, 1], result.intent.selection)
        self.assertEqual('category', result.intent.dtype)
        self.assertEqual([61.62, 38.38], result.patterns.weight_pattern)
        self.assertEqual(891, result.stats.sample)

    def test_bytestohuman(self):
        result = AistacCommons.bytes2human(1024)
        self.assertEqual('1.0KB', result)
        result = AistacCommons.bytes2human(1024**2)
        self.assertEqual('1.0MB', result)
        result = AistacCommons.bytes2human(1024**3)
        self.assertEqual('1.0GB', result)

    def test_validate_date(self):
        str_date = '2017/01/23'
        self.assertTrue(AistacCommons.valid_date(str_date))
        str_date = '2017/23/01'
        self.assertTrue(AistacCommons.valid_date(str_date))
        str_date = '23-01-2017'
        self.assertTrue(AistacCommons.valid_date(str_date))
        str_date = '01-21-2017'
        self.assertTrue(AistacCommons.valid_date(str_date))
        str_date = 'NaT'
        self.assertFalse(AistacCommons.valid_date(str_date))
        str_date = ''
        self.assertFalse(AistacCommons.valid_date(str_date))
        str_date = '01-21-2017 21:12:46'
        self.assertTrue(AistacCommons.valid_date(str_date))


    def test_raise(self):
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
