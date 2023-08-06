# -*- coding: utf-8 -*-

import os

import math
import numpy
import pandas

from .common import *

class QuoteData:
    data_path = None

    def __init__(self, data_path):
        """本地行情数据类

        参数:
            data_path: 数据路径

        """
        if not data_path or not os.path.exists(data_path):
            raise Exception('the DATA_PATH is not exists.')
        self.data_path = data_path

    def get_quote_date(self) -> time.struct_time:
        """获取行情日期

        返回值:
            最新行情日期

        """
        filename = 'ckvalid.txt'
        data_file = os.path.join(self.data_path, filename)
        if not os.path.exists(data_file):
            raise Exception('%s is not exists.' % filename)

        result = read_kvfile(data_file)
        stime = result.get('last_date')
        if not stime:
            raise Exception('the quote_data not found.')
        last_date = time.strptime(stime, '%Y-%m-%d')
        tdays = self.get_trade_days(end_date=last_date, count=1)
        if not tdays:
            raise Exception('trade-days is empty.')
        return formatter_st(tdays[0])

    def get_trade_days(self, start_date=None, end_date=None, count=None) -> list:
        """获取交易日列表

        参数:
            start_date: 开始日期，与 count 二选一；类型 str/struct_time/datetime.date/datetime.datetime
            end_date: 结束日期；类型 str/struct_time/datetime.date/datetime.datetime；默认值 datetime.date.today()
            count: 结果集行数，与 start_date 二选一

        返回值:
            交易日列表；类型 [datetime.date]

        """
        dt_start = datetime.date.fromtimestamp(time.mktime(formatter_st(start_date))) if start_date else None
        dt_end = datetime.date.fromtimestamp(time.mktime(formatter_st(end_date))) if end_date else None

        filename = 'quote-tdays.csv'
        data_file = os.path.join(self.data_path, filename)
        if not os.path.exists(data_file):
            raise Exception('%s is not exists.' % filename)

        c = {0: lambda x: datetime.date.fromtimestamp(time.mktime(time.strptime(x.decode(), '%Y-%m-%d')))}
        result = numpy.loadtxt(data_file, dtype=datetime.date, skiprows=1, converters=c)
        if not dt_start and not dt_end and not count:
            return result
        if not dt_end:
            dt_end = datetime.date.today()
        if count and count > 0:
            return result[numpy.where(result <= dt_end)][-count:]
        elif dt_start:
            return result[numpy.where((result >= dt_start) & (result <= dt_end))]
        return []

    def get_security_info(self, security=None, fields=None, types=None) -> pandas.DataFrame:
        """获取证券信息数据

        参数:
            security: 一支股票代码或者一个股票代码的 list
            fields: 获取的字段；类型 字符串 list；默认值 None 获取所有字段
            types: 获取证券类型；类型 字符串 list；默认值 stock；
                   可选值: 'stock', 'fund', 'index', 'futures', 'options', 'etf', 'lof' 等；

        返回值:
            DataFrame 对象，包含 fields 指定的字段：
                display_name：中文名称
                name：缩写简称
                start_date：上市日期；类型 datetime.date
                end_date: 退市日期；类型 datetime.date；如没有退市为 2200-01-01
                type：证券类型；stock（股票）, index（指数），etf（ETF基金），fja（分级A），fjb（分级B）

        """
        security = formatter_list(security)
        fields = formatter_list(fields)
        types = formatter_list(types, 'stock')

        filename = 'quote-ctb.csv'
        data_file = os.path.join(self.data_path, filename)
        if not os.path.exists(data_file):
            raise Exception('%s is not exists.' % filename)

        result = pandas.DataFrame()
        df = pandas.read_csv(data_file, dtype={'code': str}, parse_dates=['start_date', 'end_date'])
        if types:
            df = df[df['type'].isin(types)]
        if security:
            df = df[df['code'].isin(security)]
        if fields:
            cols_retain = ['code'] + fields
            cols_all = list(df.columns)
            cols_drop = [x for x in cols_all if x not in cols_retain]
            df.drop(columns=cols_drop, inplace=True)
        result = result.append(df, ignore_index=True)
        result.set_index('code', inplace=True)
        return result

    def get_security_xrxd(self, security, start_date=None, end_date=None, count=None) -> pandas.DataFrame:
        """获取证券除权除息数据

        参数:
            security: 一支股票代码或者一个股票代码的 list
            start_date: 开始日期，与 count 二选一；类型 str/struct_time/datetime.date/datetime.datetime
            end_date: 结束日期；类型 str/struct_time/datetime.date/datetime.datetime；默认值 datetime.date.today()
            count: 结果集行数，与 start_date 二选一

        返回值:
            DataFrame 对象，包含字段：
                date: 实施日期
                code：证券代码
                dividend_ratio：送股比例，每 10 股送 X 股
                transfer_ratio：转赠比例，每 10 股转增 X 股
                bonus_ratio：派息比例，每 10 股派 X 元

        """
        security = formatter_list(security)
        if not security:
            raise ValueError('security need be provided.')

        filename = 'quote-xrxd.csv'
        data_file = os.path.join(self.data_path, filename)
        if not os.path.exists(data_file):
            raise Exception('%s is not exists.' % filename)

        df = pandas.read_csv(data_file, dtype={'code': str}, parse_dates=['date'])
        df = df[df['code'].isin(security)]
        tdays = self.get_trade_days(start_date, end_date, count)
        df = df[df['date'].isin(tdays)]
        df.sort_values(['code', 'date'], axis=0, ascending=True, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def get_quote_static(self, date=None, fields=None, exch=None) -> pandas.DataFrame:
        """获取静态行情数据

        参数:
            date: 行情日期；类型 str/struct_time/datetime.date/datetime.datetime; 默认值：最新行情日
            fields: 获取的字段；类型 字符串 list；默认值 None 获取所有字段
                   可选值：'open','close','high','low','volume','money','high_limit','low_limit','pre_close','paused'
            exch: 交易所；默认值 ['SH', 'SZ']

        返回值:
            DataFrame 对象，包含 fields 指定的字段：
                datetime: 行情时间
                code：证券代码
                open：开盘价
                close：收盘价
                high：最高价
                low：最低价
                volume：成交量
                money：成交额
                high_limit：涨停价
                low_limit：跌停价
                pre_close：昨日收盘价
                paused：停牌标记

        """
        fields = formatter_list(fields)
        exch = formatter_list(exch, ['SH', 'SZ'])
        curr_date = formatter_st(date, self.get_quote_date())
        # print(curr_date)
        result = pandas.DataFrame()
        for x in exch:
            filename = os.path.join('static', x, time.strftime('%Y', curr_date),
                                    x + '_STATIC_' + time.strftime('%Y%m%d', curr_date) + '.csv')
            csv_file = os.path.join(self.data_path, filename)
            if not os.path.exists(csv_file):
                continue
            df = pandas.read_csv(csv_file, dtype={'code': str}, parse_dates=['datetime'])
            df['code'] = df['code'] + '.' + x
            if fields:
                cols_retain = ['datetime', 'code'] + fields
                cols_all = list(df.columns)
                cols_drop = [x for x in cols_all if x not in cols_retain]
                df.drop(columns=cols_drop, inplace=True)
            result = result.append(df, ignore_index=True)
        # print(result)
        return result

    def get_quote_kdata(self, security, period='day', fq='pre', fq_date=None, fields=None, start_date=None,
                        end_date=None, count=None):
        """获取K线数据

        参数:
            security: 一支股票代码或者一个股票代码的 list
            period: 周期，默认值 day，支持 day, week, mon, season, year, mnX
                    mnX 代表 X 分钟K线数据，如 mn1，mn5, mn15, mn30, mn60 等
            fq: 复权方式；默认值 'pre'；可选值 'pre' 前复权, None 不复权
            fq_date: 复权日期；当 fq == 'pre' 时，默认复权日期为 end_date
            fields: 获取的字段；类型 字符串 list；默认值 None 获取所有字段
                   可选值：'open','close','high','low','volume','money'
            start_date: 开始日期，与 count 二选一；类型 str/struct_time/datetime.date/datetime.datetime
            end_date: 结束日期；类型 str/struct_time/datetime.date/datetime.datetime；默认值 datetime.date.today()
            count: 结果集行数，与 start_date 二选一

        返回值:
            DataFrame 对象，包含 fields 指定的字段：
                datetime: 行情时间
                code：证券代码
                open：开盘价
                close：收盘价
                high：最高价
                low：最低价
                volume：成交量
                money：成交额

        """
        def exec_fq(df, cols_retain, fq_xrxd):
            if fq_xrxd is None:
                return df
            cols_px = ['open', 'close', 'high', 'low', 'pre_close', 'high_limit', 'low_limit']
            cols_fq = [x for x in list(df.columns) if x in cols_px and x in cols_retain]
            if not cols_fq:
                return df
            for index, row in fq_xrxd.iterrows():
                start = time.time()
                c = df[df['code'] == row['code']]['close']
                if len(c) == 0:
                    continue
                s = str(c.iloc[0])
                p = s.find('.')
                n = len(s) - p - 1 if p >= 0 else 0
                c = df.loc[(df['code'] == row['code']) & (df['datetime'] < pandas.Timestamp(row['date'])), cols_fq]
                if len(c) == 0:
                    continue
                # print(row['code'], row['date'], r, v)
                r = 10 / (10 + (row['dividend_ratio'] if not math.isnan(row['dividend_ratio']) else 0) + (
                    row['transfer_ratio'] if not math.isnan(row['transfer_ratio']) else 0))
                v = (row['bonus_ratio'] if not math.isnan(row['bonus_ratio']) else 0) / 10
                c = round(c * r - v, n)
                df.loc[(df['code'] == row['code']) & (df['datetime'] < pandas.Timestamp(row['date'])), cols_fq] = c
            return df

        if period in ['day', 'week', 'mon', 'season', 'year']:
            period_type = 'day'
        elif period[0:2] == 'mn' and period[2:].isdecimal():
            period_type = 'mn1'
        else:
            raise Exception('period is invalid.')

        security = formatter_list(security)
        fields = formatter_list(fields, ['open', 'close', 'high', 'low', 'volume', 'money'])
        start_date = formatter_st(start_date) if start_date else None
        end_date = formatter_st(end_date, time.localtime())
        if not start_date and not count:
            raise Exception('start_date or count must to be set.')

        if fq:
            fq_date = formatter_st(fq_date, end_date)
            fq_xrxd = self.get_security_xrxd(security=security, start_date=start_date, end_date=fq_date, count=count)

        cols_retain = ['datetime', 'code'] + fields
        mode_static = False
        prep_count = None
        if count:
            if period == 'day':
                prep_count = count
            elif period == 'week':
                prep_count = count * 5
            elif period == 'month':
                prep_count = count * 23
            elif period == 'season':
                prep_count = count * 66
            elif period == 'year':
                prep_count = count * 262
            elif period_type == 'mn1':
                prep_count = count * int(period[2:])
        if period_type == 'day':
            if prep_count:
                evaluate_days = prep_count
            elif start_date:
                evaluate_days = int((time.mktime(end_date) - time.mktime(start_date)) / 86400 * 5 / 7)
            else:
                evaluate_days = None
            if evaluate_days < len(security):
                mode_static = True
        result = pandas.DataFrame()
        if mode_static:
            print("get data from static files")
            trade_list = self.get_trade_days(start_date, end_date, prep_count)
            for x in trade_list:
                df = self.get_quote_static(x)
                df = df[df['code'].isin(security)]
                df = exec_fq(df, cols_retain, fq_xrxd)
                cols_all = list(df.columns)
                cols_drop = [x for x in cols_all if x not in cols_retain]
                df.drop(columns=cols_drop, inplace=True)
                result = result.append(df, ignore_index=True)
            result.sort_values(['code', 'datetime'], axis=0, ascending=True, inplace=True)
            result.reset_index(drop=True, inplace=True)
        else:
            print("get data from", period_type, "files")
            dt_start = numpy.datetime64(
                datetime.datetime.fromtimestamp(time.mktime(start_date))) if start_date else None
            dt_end = numpy.datetime64(datetime.datetime.fromtimestamp(time.mktime(end_date)))
            for x in security:
                p = x.find('.')
                if p < 0:
                    continue
                sec_code = x[0:p]
                exc_code = x[p + 1:]
                filename = os.path.join(period_type, exc_code, exc_code + '_' + period_type.upper()
                                        + '_' + sec_code + '.csv')
                csv_file = os.path.join(self.data_path, filename)
                if not os.path.exists(csv_file):
                    continue
                df = pandas.read_csv(csv_file, parse_dates=['datetime'])
                if not prep_count:
                    df = df[(df['datetime'] >= dt_start) & (df['datetime'] <= dt_end)]
                else:
                    df = df[df['datetime'] <= dt_end][-prep_count:]
                df.insert(loc=0, column='code', value=sec_code + '.' + exc_code)
                df = exec_fq(df, cols_retain, fq_xrxd)
                if fields:
                    cols_all = list(df.columns)
                    cols_drop = [x for x in cols_all if x not in cols_retain]
                    df.drop(columns=cols_drop, inplace=True)
                result = result.append(df, ignore_index=True)
        agg_need = True
        if period == 'year':
            result['period'] = result['datetime'].apply(lambda x: x.year)
        elif period == 'season':
            result['period'] = result['datetime'].apply(lambda x: '%dq%d' % (x.year, (x.month - 1) // 3 + 1))
        elif period == 'mon':
            result['period'] = result['datetime'].apply(lambda x: x.year * 100 + x.month)
        elif period == 'week':
            result['period'] = result['datetime'].apply(lambda x: '%dw%02d' % (x.year, x.isocalendar()[1]))
        elif period_type == 'mn1' and period != 'mn1':
            m = [570, 660]
            n = int(period[2:])
            result['period'] = result['datetime'].apply(lambda x: '%d%02d%02dt%04d' % (
                x.year, x.month, x.day, ((x.hour * 60 + x.minute - 1 - m[0 if x.hour < 12 else 1]) // n + 1) * n))
        else:
            agg_need = False
        if agg_need:
            agg_dict = {'datetime': 'last', 'open': 'first', 'close': 'last', 'high': 'max', 'low': 'min',
                        'volume': 'sum',
                        'money': 'sum'}
            for k in [x for x in agg_dict.keys() if x not in cols_retain]:
                del agg_dict[k]
            result = result.groupby(['code', 'period']).agg(agg_dict)
            result.reset_index(inplace=True)
            result.drop(columns='period', inplace=True)
        if count:
            result = result.tail(count)
        result.reset_index(inplace=True)
        return result
