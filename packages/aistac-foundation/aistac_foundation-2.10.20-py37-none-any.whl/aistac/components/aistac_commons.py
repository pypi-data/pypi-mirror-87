import collections
import math
import re
import threading
from copy import deepcopy
from datetime import datetime
from typing import Any

__author__ = 'Darryl Oatridge'


class AistacCommons(object):

    @staticmethod
    def list_formatter(value: Any) -> list:
        """ Useful utility method to convert any type of str, list, tuple or pd.Series into a list"""
        if isinstance(value, (int, float, str, datetime)):
            return [value]
        if isinstance(value, (list, tuple, set)):
            return list(value)
        if isinstance(value, (collections.abc.KeysView, collections.abc.ValuesView, collections.abc.ItemsView)):
            return list(value)
        if isinstance(value, dict):
            return list(value.keys())
        return list()

    @staticmethod
    def valid_date(str_date: str):
        """Validates if a string could be a date. This assume a combination of year month day are the start
        of the string"""
        if not isinstance(str_date, str):
            return False
        try:
            mat = re.match('(\d{2})[/.-](\d{2})[/.-](\d{4}?)', str_date)
            if mat is not None:
                groups = tuple(mat.groups()[-1::-1])
                if int(groups[1]) > 12:
                    groups = (groups[0], groups[2], groups[1])
                datetime(*(map(int, groups)))
                return True
            mat = re.match('(\d{4})[/.-](\d{2})[/.-](\d{2}?)', str_date)
            if mat is not None:
                groups = tuple(mat.groups())
                if int(groups[1]) > 12:
                    groups = (groups[0], groups[2], groups[1])
                datetime(*(map(int, groups)))
                return True
        except ValueError:
            pass
        return False

    @staticmethod
    def bytes2human(size_bytes: int):
        """Converts byte value to a human readable format"""
        if size_bytes == 0:
            return "0b"
        size_name = ("b", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s}{size_name[i]}"

    @staticmethod
    def param2dict(**kwargs):
        return dict((k, v) for (k, v) in locals().get('kwargs', {}).items() if v is not None)

    @staticmethod
    def dict_with_missing(base: dict, default: Any):
        """returns a dictionary with defining  __missing__() which returns the default value"""

        class DictMissing(dict):

            def __missing__(self, x):
                return default

        return DictMissing(base)

    @staticmethod
    def label_gen(limit: int=None) -> str:
        """generates a sequential headers. if limit is set will return at that limit"""
        headers = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        counter = 0
        for n in range(0, 100):
            for i in range(len(headers)):
                rtn_str = f"{headers[i]}" if n == 0 else f"{headers[i]}{n}"
                if isinstance(limit, int) and counter >= limit:
                    return rtn_str
                counter += 1
                yield rtn_str

    @staticmethod
    def is_list_equal(a: list, b: list) -> bool:
        """checks if two lists are equal in count and frequency of elements, ignores order"""
        if collections.Counter(a) == collections.Counter(b):
            return True
        return False

    @staticmethod
    def unique_list(seq: list) -> list:
        """ Useful utility method to retain the order of a list but removes duplicates"""
        seen = set()
        # Note: assign seen add to a local variable as local variable are less costly to resolve than dynamic call
        seen_add = seen.add
        # Note: seen.add() always returns None, the 'or' is only there to attempt to set update
        return [x for x in seq if not (x in seen or seen_add(x))]

    @staticmethod
    def resize_list(seq: list, resize: int) -> list:
        """resize a sequence list duplicating or removing sequence entries to fit to the new size. if the
        seq length and the resize length are not divisible, values are repeated or removed to make the length
            for example: [1,4,2] resized to 7 => [1,1,1,4,4,2,2] where the first index is repeated an additional time.
        """
        if len(seq) == 0:
            return [0] * resize
        seq_len = len(seq)
        rtn_counter = [int(round(resize / seq_len))] * seq_len
        shortfall = resize - sum(rtn_counter)
        for i in range(abs(shortfall)):
            if shortfall > 0:
                rtn_counter[rtn_counter.index(min(rtn_counter))] += 1
            elif shortfall < 0:
                rtn_counter[rtn_counter.index(max(rtn_counter))] -= 1
        rtn_seq = []
        for i in range(len(seq)):
            rtn_seq += [seq[i]] * rtn_counter[i]
        return rtn_seq

    @staticmethod
    def filter_headers(data: dict, headers: [str, list]=None, drop: bool=None, dtype: [str, list]=None,
                       exclude: bool=None, regex: [str, list]=None, re_ignore_case: bool=None) -> list:
        """ returns a list of headers based on the filter criteria

        :param data: the Canonical data to get the column headers from
        :param headers: a list of headers to drop or filter on type
        :param drop: to drop or not drop the headers
        :param dtype: the column types to include or excluse. Default None else int, float, bool, object, 'number'
        :param exclude: to exclude or include the dtypes. Default is False
        :param regex: a regiar expression to seach the headers
        :param re_ignore_case: true if the regex should ignore case. Default is False
        :return: a filtered list of headers

        :raise: TypeError if any of the types are not as expected
        """
        if drop is None or not isinstance(drop, bool):
            drop = False
        if exclude is None or not isinstance(exclude, bool):
            exclude = False
        if re_ignore_case is None or not isinstance(re_ignore_case, bool):
            re_ignore_case = False

        if not isinstance(data, dict):
            raise TypeError("The first function attribute must be a dictionary")
        _headers = AistacCommons.list_formatter(headers)
        dtype = AistacCommons.list_formatter(dtype)
        regex = AistacCommons.list_formatter(regex)
        _obj_cols = list(data.keys())
        _rtn_cols = set()
        unmodified = True

        if _headers is not None and _headers:
            _rtn_cols = set(_obj_cols).difference(_headers) if drop else set(_obj_cols).intersection(_headers)
            unmodified = False

        if regex is not None and regex:
            re_ignore_case = re.I if re_ignore_case else 0
            _regex_cols = list()
            for exp in regex:
                _regex_cols += [s for s in _obj_cols if re.search(exp, s, re_ignore_case)]
            _rtn_cols = _rtn_cols.union(set(_regex_cols))
            unmodified = False

        if unmodified:
            _rtn_cols = set(_obj_cols)

        if dtype is not None and dtype:
            type_header = []
            for col in _rtn_cols:
                if any((isinstance(x, tuple(dtype)) for x in col)):
                    type_header.append(col)
            _rtn_cols = set(_rtn_cols).difference(type_header) if exclude else set(_rtn_cols).intersection(type_header)

        return [c for c in _rtn_cols]

    @staticmethod
    def filter_columns(data: dict, headers=None, drop=False, dtype=None, exclude=False, regex=None,
                       re_ignore_case=None, inplace=False) -> dict:
        """ Returns a subset of columns based on the filter criteria

        :param data: the Canonical data to get the column headers from
        :param headers: a list of headers to drop or filter on type
        :param drop: to drop or not drop the headers
        :param dtype: the column types to include or excluse. Default None else int, float, bool, object, 'number'
        :param exclude: to exclude or include the dtypes
        :param regex: a regiar expression to seach the headers
        :param re_ignore_case: true if the regex should ignore case. Default is False
        :param inplace: if the passed pandas.DataFrame should be used or a deep copy
        :return:
        """
        if not inplace:
            with threading.Lock():
                data = deepcopy(data)
        obj_cols = AistacCommons.filter_headers(data=data, headers=headers, drop=drop, dtype=dtype, exclude=exclude,
                                                regex=regex, re_ignore_case=re_ignore_case)
        for col in data.keys():
            if col not in obj_cols:
                data.pop(col)
        return data


class AnalyticsCommons(object):

    class Intent(object):

        def __init__(self, section: dict):
            self._intent = deepcopy(section)

        @property
        def dtype(self):
            return self._intent.get('dtype', 'object')

        @property
        def selection(self):
            return self._intent.get('selection', [])

        @property
        def granularity(self):
            return self._intent.get('granularity', 1)

        @property
        def lower(self):
            return self._intent.get('lower', 0.0)

        @property
        def upper(self):
            return self._intent.get('upper', 0.0)

        @property
        def top(self):
            return self._intent.get('top', 1.0)

        @property
        def precision(self):
            return self._intent.get('precision', 0)

        @property
        def year_first(self):
            return self._intent.get('year_first', False)

        @property
        def day_first(self):
            return self._intent.get('day_first', False)

        @property
        def data_format(self):
            return self._intent.get('data_format', None)

        @property
        def weighting_precision(self):
            return self._intent.get('weighting_precision', None)

    class Patterns(object):

        def __init__(self, section: dict):
            self._patterns = deepcopy(section)

        @property
        def weight_pattern(self):
            return self._patterns.get('weight_pattern', list())

        @property
        def weight_mean(self):
            return self._patterns.get('weight_mean', list())

        @property
        def weight_std(self):
            return self._patterns.get('weight_std', list())

        @property
        def sample_distribution(self):
            return self._patterns.get('sample_distribution', list())

        @property
        def dominant_values(self):
            return self._patterns.get('dominant_values', list())

        @property
        def dominance_weighting(self):
            return self._patterns.get('dominance_weighting', list())

        @property
        def dominant_percent(self):
            return self._patterns.get('dominant_percent', 0)

    class Stats(object):

        def __init__(self, section: dict):
            self._stats = deepcopy(section)

        @property
        def nulls_percent(self):
            return self._stats.get('nulls_percent', 0)

        @property
        def sample(self):
            return self._stats.get('sample', 0)

        @property
        def outlier_percent(self):
            return self._stats.get('outlier_percent', 0)

        @property
        def mean(self):
            return self._stats.get('mean', 0)

        @property
        def var(self):
            return self._stats.get('var', 0)

        @property
        def sem(self):
            return self._stats.get('sem', 0)

        @property
        def mad(self):
            return self._stats.get('mad', 0)

        @property
        def skew(self):
            return self._stats.get('skew', 0)

        @property
        def kurtosis(self):
            return self._stats.get('kurtosis', 0)

    def __init__(self, analysis: dict, label: str = None):
        if not isinstance(analysis, dict) or len(analysis) == 0:
            raise ValueError("The passed analysis is not a dictionary or is of zero length")
        self._analysis = deepcopy(analysis)
        analysis_label = 'n/a'
        if len(analysis) == 1:
            analysis_label = list(self._analysis.keys())[0]
            self._analysis = self._analysis.get(analysis_label, {})
        if 'associate' in self._analysis.keys() or 'analysis' in self._analysis.keys():
            self.associate = self._analysis.get('associate', 'n/a')
            self._analysis = self._analysis.get('analysis', {})
        else:
            self.associate = 'n/a'
        self.label = label if isinstance(label, str) else analysis_label
        self._intent = self.Intent(section=self._analysis.get('intent', {}))
        self._patterns = self.Patterns(section=self._analysis.get('patterns', {}))
        self._stats = self.Stats(section=self._analysis.get('stats', {}))

    @property
    def intent(self) -> Intent:
        return self._intent

    @property
    def patterns(self) -> Patterns:
        return self._patterns

    @property
    def stats(self) -> Stats:
        return self._stats

    def to_dict(self):
        return deepcopy(self._analysis)

    def __str__(self):
        return self._analysis.__str__()

    def __repr__(self):
        return self._analysis.__repr__()
