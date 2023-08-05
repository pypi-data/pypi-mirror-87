import os
import random
import re
import string
import time


class Resolver:
    # 选择项文件缓存
    CHOICES_CACHE = {}

    def __init__(self, defs: dict, def_dir: str, encoding: str, use_cache: bool, options: dict):
        self.defs = defs['def']
        self.def_dir = def_dir
        self.encoding = encoding
        self.use_cache = use_cache
        self.options = options
        # 需要生成的数据长度
        # 0 表示返回单个对象
        self.data_length = int(defs['len']) if 'len' in defs else 0
        # 自增长整数基数
        self.i_base = options['i_base'] if 'i_base' in options else 0
        # 当需要返回多个数据时，当前数据的索引
        self.data_index = 0
        self.date_range = self.resolve_date_range()
        self.date_steps = {}
        self.resolve_date_step(self.data_length)

    def resolve(self):
        if self.data_length == 0:
            return self.resolve_data(self.defs)

        data = []
        for _ in range(self.data_length):
            data.append(self.resolve_data(self.defs))
            self.data_index += 1
        return data

    def resolve_date_range(self):
        if 'date_range' not in self.options:
            return [0, 0]
        [begin, end] = self.options['date_range']
        date_fmt = self.options['date_fmt'] if 'date_fmt' in self.options else '%Y-%m-%d %H:%M:%S'
        bt = self.parse_date(begin, date_fmt)
        et = self.parse_date(end, date_fmt)

        return [bt, et]

    def resolve_date_step(self, length):
        if length in self.date_steps:
            return

        if self.data_length <= 1:
            self.date_steps[length] = 0
            return

        self.date_steps[length] = int((self.date_range[1] - self.date_range[0]) / (length - 1))

    def next_int(self, offset) -> int:
        if offset is None:
            offset = self.data_index
        return self.i_base + offset

    def next_date(self, length, offset) -> int:
        if length is None:
            length = self.data_length
        if offset is None:
            offset = self.data_index
        return self.date_range[0] + self.date_steps[length] * offset

    def load_file(self, filename):
        abs_filename = os.path.abspath(os.path.join(self.def_dir, filename))

        if self.use_cache and abs_filename in self.CHOICES_CACHE:
            return self.CHOICES_CACHE[abs_filename]

        with open(abs_filename, encoding=self.encoding, mode='r') as fp:
            if filename.endswith('.json'):
                import json
                self.CHOICES_CACHE[abs_filename] = json.load(fp)
            else:
                lines = fp.readlines()
                self.CHOICES_CACHE[abs_filename] = [line.rstrip('\r\n') for line in lines]
            fp.close()

        return self.CHOICES_CACHE[abs_filename]

    @staticmethod
    def parse_date(s, fmt='%Y%m%d') -> int:
        return int(time.mktime(time.strptime(s, fmt)))

    @staticmethod
    def parse_datetime(s) -> int:
        return int(time.mktime(time.strptime(s, '%Y%m%d%H%M%S')))

    @staticmethod
    def get_int_value(exp):
        # 枚举值，直接选择
        if isinstance(exp, list):
            return int(random.choice(exp))
        [start, end] = [int(i) for i in exp.split('-')]
        return random.randint(start, end)

    @staticmethod
    def get_float_value(exp):
        # 枚举值，直接选择
        if isinstance(exp, list):
            return float(random.choice(exp))
        [start, end] = [float(i) for i in exp.split('-')]
        return random.randint(start * 100, end * 100) / 100

    @staticmethod
    def get_bool_value(exp):
        # 枚举值，直接选择
        if isinstance(exp, list):
            return bool(random.choice(exp))
        return random.choice([True, False])

    @staticmethod
    def get_string_value(exp):
        # 枚举值，直接选择
        if isinstance(exp, list):
            return random.choice(exp)
        match = re.match(r'^(?P<min>\d+)-(?P<max>\d+)(?P<exp>[lLns]+)$', exp)
        if match is None:
            print('[mockee]字符串规则无效: %s' % exp)
            return

        min_len = int(match.group('min'))
        max_len = int(match.group('max'))
        exp = match.group('exp')

        data_set = []
        if 'l' in exp:
            data_set.append(string.ascii_lowercase)
        if 'L' in exp:
            data_set.append(string.ascii_uppercase)
        if 'n' in exp:
            data_set.append(string.digits)
        if 's' in exp:
            data_set.append(string.punctuation)

        data_len = min_len if min_len == max_len else random.randint(min_len, max_len)

        return ''.join(random.sample(''.join(data_set), data_len))

    def get_date_value(self, exp):
        # 枚举值，直接选择
        if isinstance(exp, list):
            return random.choice(exp)
        temp = exp.split('-')
        start = self.parse_date(temp[0])
        end = self.parse_date(temp[1])
        fmt = '-'.join(temp[2:])[1:] if len(temp) > 2 else '%Y-%m-%d'
        return time.strftime(fmt, time.localtime(random.randint(start, end)))

    def get_time_value(self, exp):
        # 枚举值，直接选择
        if isinstance(exp, list):
            return random.choice(exp)
        temp = exp.split('-')
        start = self.parse_datetime('20200101' + temp[0])
        end = self.parse_datetime('20200101' + temp[1])
        fmt = '-'.join(temp[2:])[1:] if len(temp) > 2 else '%H:%M:%S'
        return time.strftime(fmt, time.localtime(random.randint(start, end)))

    def get_datetime_value(self, exp):
        # 枚举值，直接选择
        if isinstance(exp, list):
            return random.choice(exp)
        temp = exp.split('-')
        start = self.parse_datetime(temp[0])
        end = self.parse_datetime(temp[1])
        fmt = '-'.join(temp[2:])[1:] if len(temp) > 2 else '%Y-%m-%d %H:%M:%S'
        return time.strftime(fmt, time.localtime(random.randint(start, end)))

    @staticmethod
    def get_json_value(exp):
        # 枚举值，直接选择
        if isinstance(exp, list):
            return random.choice(exp)

    def get_value(self, data_type, exp, length, offset):
        if data_type == 'i':
            return self.get_int_value(exp)

        if data_type == 'f':
            return self.get_float_value(exp)

        if data_type == 'b':
            return self.get_bool_value(exp)

        if data_type == 's':
            return self.get_string_value(exp)

        # 后面都是日期/时间类型了
        if exp.startswith('auto'):
            temp = exp.split('->')
            fmt = temp[1] if len(temp) > 1 else '%Y-%m-%d %H:%M:%S'
            return time.strftime(fmt, time.localtime(self.next_date(length, offset)))

        if data_type == 'd':
            return self.get_date_value(exp)

        if data_type == 't':
            return self.get_time_value(exp)

        if data_type == 'dt':
            return self.get_datetime_value(exp)

    @staticmethod
    def resolve_rule(rule):
        match = re.match(r'^(?P<type>(i|f|b|s|j|d|t|dt|ref))(\s+(?P<exp>.+))?$', rule)
        if match is None:
            return None, None

        data_type = match.group('type')
        exp = match.group('exp')

        return data_type, exp

    def resolve_exp(self, desc, length, offset):
        (data_type, exp) = self.resolve_rule(desc)

        if data_type is None or (data_type != 'b' and exp is None):
            print('[mockee]数据规则无效: %s' % desc)
            return desc

        # 引用定义文件
        if data_type == 'ref':
            return self.resolve_data(self.load_file(exp))

        # JSON值选择文件
        if data_type == 'j':
            return self.get_json_value(self.load_file(exp))

        if data_type == 'i' and exp == 'auto':
            return self.next_int(offset)

        if exp is not None:
            if exp.startswith('(#') and exp.endswith('#)'):
                # 从文件加载枚举
                exp = self.load_file(exp[2:-2])
            elif exp.startswith('(') and exp.endswith(')'):
                # 从列表枚举列表
                exp = re.split(r'\s+', exp[1:-1])

        return self.get_value(data_type, exp, length, offset)

    def get_resolved_value(self, val, length=None, offset=None):
        if isinstance(val, dict):
            return self.resolve_data(val)

        if not isinstance(val, str):
            return val

        if not val.startswith('#>'):
            return val

        return self.resolve_exp(val[2:], length, offset)

    def resolve_data(self, defs):
        if isinstance(defs, str):
            if defs.startswith('#>'):
                (data_type, exp) = self.resolve_rule(defs[2:])
                if data_type != 'ref':
                    print('[mockee] 无效的规则定义: ' + defs)
                    return defs
                return self.resolve_data(self.load_file(exp))
            else:
                print('[mockee] 无效的规则定义: ' + defs)
                return defs

        result = {}
        ext_fields = {}
        for key in defs:
            item = defs[key]

            # 看是不是扩展项
            # key=#ext#
            # 其值应该指定一个(字符串)/多个(字符串数组) json 定义文件
            if key == '#ext#':
                if isinstance(item, str):
                    ext_fields.update(**self.load_file(item))
                    continue

                for i in item:
                    ext_fields.update(**self.load_file(i))

                continue

            match = re.match(r'^(?P<name>.+?)(\[(?P<len>[0-9]+)])?$', key)

            key = match.group('name')
            length = match.group('len')

            if length is None:
                result[key] = self.get_resolved_value(item)
                continue

            length = int(length)

            self.resolve_date_step(length)

            value = []
            for index in range(length):
                value.append(self.get_resolved_value(item, length, index))

            result[key] = value

        # 移除重复项后的字段
        available_fields = {}

        for key in ext_fields:
            if key in defs:
                continue
            available_fields[key] = ext_fields[key]

        if available_fields:
            result.update(**self.resolve_data(available_fields))

        return result
