import pytest
import numpy as np
import pandas as pd
import datetime as dt
import time
from dask import delayed

from dutil.pipeline import cached, clear_cache, DelayedParameters, DelayedParameter, delayed_cached, delayed_compute


cache_dir = 'cache/temp/'
eps = 0.00001


@pytest.mark.parametrize(
    'data, ftype',
    [
        ((0, 1, 3, 5, -1), 'pickle'),
        ((0, 1., 3232.22, 5., -1., None), 'pickle'),
        ([0, 1, 3, 5, -1], 'pickle'),
        ([0, 1., 3232.22, 5., -1., None], 'pickle'),
        (pd.Series([0, 1, 3, 5, -1]), 'pickle'),
        (pd.Series([0, 1., 3232.22, 5., -1., np.nan]), 'pickle'),
        (pd.Series([1, 2, 3, 4], dtype='category'), 'pickle'),
        (pd.DataFrame({
            'a': [0, 1, 3, 5, -1],
            'b': [2, 1, 0, 0, 14],
        }), 'pickle'),
        (pd.DataFrame({
            'a': [0, 1., 3232.22, -1., np.nan],
            'b': ['a', 'b', 'c', 'ee', '14'],
            'c': [dt.datetime(2018, 1, 1),
                  dt.datetime(2019, 1, 1),
                  dt.datetime(2020, 1, 1),
                  dt.datetime(2021, 1, 1),
                  dt.datetime(2022, 1, 1)],
        }), 'pickle'),
        (pd.DataFrame({
            'a': [0, 1, 3, 5, -1],
            'b': [2, 1, 0, 0, 14],
        }), 'parquet'),
        (pd.DataFrame({
            'a': [0, 1., 3232.22, -1., np.nan],
            'b': ['a', 'b', 'c', 'ee', '14'],
            'c': [dt.datetime(2018, 1, 1),
                  dt.datetime(2019, 1, 1),
                  dt.datetime(2020, 1, 1),
                  dt.datetime(2021, 1, 1),
                  dt.datetime(2022, 1, 1)],
            'd': [pd.Timestamp('2018-01-01'),
                  pd.Timestamp('2018-01-01'),
                  pd.Timestamp('2018-01-01'),
                  pd.Timestamp('2018-01-01'),
                  pd.Timestamp('2018-01-01')],
        }), 'parquet'),
        (pd.DataFrame({
            'a': [0, 1., 3232.22, -1., np.nan],
            'b': [dt.timedelta(hours=1),
                  dt.timedelta(hours=1),
                  dt.timedelta(hours=1),
                  dt.timedelta(hours=1),
                  dt.timedelta(hours=1)],
        }), 'pickle'),
    ]
)
def test_cached_load_and_hash(data, ftype):
    @cached(folder=cache_dir, ftype=ftype, override=False)
    def load_data():
        return data

    @cached(folder=cache_dir, ftype='pickle', override=False)
    def compute_data(data):
        return 0

    clear_cache(cache_dir)
    loaded = load_data().load()
    _ = compute_data(loaded).load()
    loaded = load_data().load()
    _ = compute_data(loaded).load()

    if isinstance(data, pd.Series):
        pd.testing.assert_series_equal(loaded, data)
    elif isinstance(data, pd.DataFrame):
        pd.testing.assert_frame_equal(loaded, data)
    elif isinstance(data, np.ndarray):
        np.testing.assert_equal(loaded, data)
    else:
        assert loaded == data


@pytest.mark.parametrize(
    'data, ftype, eps, ts',
    [
        (pd.DataFrame({
            'a': [0, 1, 3, 5, -1],
            'b': [2, 1, 0, 0, 14],
        }), 'parquet', 0.1, pd.Timestamp('2018-01-01'),),
        (pd.DataFrame({
            'a': [0, 1., 3232.22, -1., np.nan],
            'b': ['a', 'b', 'c', 'ee', '14'],
            'c': [dt.datetime(2018, 1, 1),
                  dt.datetime(2019, 1, 1),
                  dt.datetime(2020, 1, 1),
                  dt.datetime(2021, 1, 1),
                  dt.datetime(2022, 1, 1)],
            'd': [pd.Timestamp('2018-01-01'),
                  pd.Timestamp('2018-01-01'),
                  pd.Timestamp('2018-01-01'),
                  pd.Timestamp('2018-01-01'),
                  pd.Timestamp('2018-01-01')],
        }), 'parquet', 0.1, pd.Timestamp('2018-01-01'),),
        (pd.DataFrame({
            'a': [0, 1., 3232.22, -1., np.nan],
            'b': [dt.timedelta(hours=1),
                  dt.timedelta(hours=1),
                  dt.timedelta(hours=1),
                  dt.timedelta(hours=1),
                  dt.timedelta(hours=1)],
        }), 'pickle', 0.1, pd.Timestamp('2018-01-01'),),
    ]
)
def test_cached_with_args_kwargs_load(data, ftype, eps, ts):
    @cached(folder=cache_dir, ftype=ftype, override=False)
    def load_data(eps, ts):
        assert eps > 0
        assert ts > pd.Timestamp('2000-01-01')
        return data

    clear_cache(cache_dir)
    _ = load_data(eps, ts=ts).load()
    loaded = load_data(eps, ts=ts).load()

    if isinstance(data, pd.Series):
        pd.testing.assert_series_equal(loaded, data)
    elif isinstance(data, pd.DataFrame):
        pd.testing.assert_frame_equal(loaded, data)
    elif isinstance(data, np.ndarray):
        np.testing.assert_equal(loaded, data)
    else:
        assert loaded == data


@pytest.mark.parametrize(
    'data, output, ftype',
    [
        (pd.DataFrame({
            'a': [0, 1, 3, 5, -1],
            'b': [2, 1, 0, 0, 14],
        }), pd.DataFrame({
            'a': [0, 1, 3, 5, -1],
            'b': [2, 1, 0, 0, 14],
        }), 'parquet'),
        (pd.DataFrame({
            'a': [.5, np.nan, np.nan],
            'b': ['a', 'b', '14'],
            'c': [dt.datetime(2018, 1, 1),
                  dt.datetime(2019, 1, 1),
                  dt.datetime(2022, 1, 1)],
            'd': [pd.Timestamp('2018-01-01'),
                  pd.Timestamp('2018-01-01'),
                  pd.Timestamp('2018-01-01')],
        }), pd.DataFrame({
            'a': [.5],
            'b': ['a'],
            'c': [dt.datetime(2018, 1, 1)],
            'd': [pd.Timestamp('2018-01-01')],
        }), 'parquet'),
        (pd.DataFrame({
            'a': [0, 1., np.nan],
            'b': [dt.timedelta(hours=1),
                  dt.timedelta(hours=1),
                  dt.timedelta(hours=1)],
        }), pd.DataFrame({
            'a': [0, 1.],
            'b': [dt.timedelta(hours=1),
                  dt.timedelta(hours=1)],
        }), 'pickle'),
    ]
)
def test_cached_with_chained_df_load_and_hash(data, output, ftype):
    @cached(folder=cache_dir, ftype=ftype, override=False)
    def load_data():
        return data
    
    @cached(folder=cache_dir, ftype=ftype, override=False)
    def process_data(df):
        return df.dropna()

    clear_cache(cache_dir)
    df = load_data()
    _ = process_data(df).load()

    df = load_data()
    processed = process_data(df).load()

    if isinstance(data, pd.Series):
        pd.testing.assert_series_equal(processed, output)
    elif isinstance(data, pd.DataFrame):
        pd.testing.assert_frame_equal(processed, output)
    elif isinstance(data, np.ndarray):
        np.testing.assert_equal(processed, output)
    else:
        assert processed == output


@pytest.mark.parametrize(
    'data, ftype, eps, ts',
    [
        (pd.DataFrame({
            'a': [0, 1, 3, 5, -1],
            'b': [2, 1, 0, 0, 14],
        }), 'parquet', 0.1, pd.Timestamp('2018-01-01'),),
    ]
)
def test_dask_cached_with_args_kwargs_load_compute(data, ftype, eps, ts):
    @delayed()
    @cached(folder=cache_dir, ftype=ftype, override=False)
    def load_data(eps, ts):
        assert eps > 0
        assert ts > pd.Timestamp('2000-01-01')
        return data

    clear_cache(cache_dir)
    r = load_data(eps, ts=ts)
    _ = r.compute()
    loaded = r.compute().load()

    if isinstance(data, pd.Series):
        pd.testing.assert_series_equal(loaded, data)
    elif isinstance(data, pd.DataFrame):
        pd.testing.assert_frame_equal(loaded, data)
    elif isinstance(data, np.ndarray):
        np.testing.assert_equal(loaded, data)
    else:
        assert loaded == data


def test_cached_with_args_kwargs_partial_ignore():
    @cached(folder=cache_dir, ignore_kwargs=['ts'])
    def load_data(eps, ts):
        time.sleep(1.)
        assert eps > 0
        assert ts > pd.Timestamp('2000-01-01')
        return eps

    clear_cache(cache_dir)
    start = dt.datetime.utcnow()
    res1 = load_data(eps=0.1, ts=pd.Timestamp('2010-01-01')).load()
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert delay > 0.95

    start = dt.datetime.utcnow()
    res2 = load_data(eps=0.1, ts=pd.Timestamp('2012-01-01')).load()
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert delay < 0.95
    assert res1 == res2

    start = dt.datetime.utcnow()
    res3 = load_data(eps=0.2, ts=pd.Timestamp('2012-01-01')).load()
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert delay > 0.95
    assert res1 != res3


def test_cached_load_time():
    @cached(folder=cache_dir, override=False)
    def load_data():
        time.sleep(1)
        return 1

    clear_cache(cache_dir)

    start = dt.datetime.utcnow()
    _ = load_data().load()
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert delay > 0.95

    start = dt.datetime.utcnow()
    _ = load_data().load()
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert delay < 0.95


def test_dask_cached_load_time():
    @delayed()
    @cached(folder=cache_dir, override=False)
    def load_data():
        time.sleep(1)
        return 1

    clear_cache(cache_dir)

    start = dt.datetime.utcnow()
    r = load_data()
    r.compute()
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert delay > 0.95

    start = dt.datetime.utcnow()
    r = load_data()
    r.compute()
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert delay < 0.95


def test_dask_pipeline():
    clear_cache(cache_dir)

    @delayed()
    @cached(folder=cache_dir)
    def load_data_1():
        time.sleep(1)
        return 5

    @delayed()
    @cached(folder=cache_dir)
    def load_data_2():
        time.sleep(1)
        return 3

    @delayed()
    @cached(folder=cache_dir)
    def add(x, y):
        return x + y

    d1 = load_data_1()
    d2 = load_data_2()
    r = add(d1, d2)

    start = dt.datetime.utcnow()
    (output,) = delayed_compute((r,))
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert 0.95 < delay < 1.95
    assert output == 8

    start = dt.datetime.utcnow()
    (output,) = delayed_compute((r,))
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert delay < 0.95
    assert output == 8


def test_dask_pipeline_sequential_runs():
    clear_cache(cache_dir)

    @delayed()
    @cached(folder=cache_dir)
    def load_data_1():
        time.sleep(1)
        return 5

    @delayed()
    @cached(folder=cache_dir)
    def load_data_2():
        time.sleep(1)
        return 3

    @delayed()
    @cached(folder=cache_dir)
    def add(x, y):
        return x + y

    d1 = load_data_1()
    d2 = load_data_2()
    r = add(d1, d2)

    start = dt.datetime.utcnow()
    d1_, d2_ = delayed_compute((d1, d2))
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert 0.95 < delay < 1.95

    start = dt.datetime.utcnow()
    (output,) = delayed_compute((r,))
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert delay < 0.95
    assert output == 8


def test_dask_pipeline_with_parameters():
    clear_cache(cache_dir)

    @delayed()
    @cached(folder=cache_dir)
    def load_data_1(ts: dt.datetime):
        assert ts > dt.datetime(2019, 1, 1)
        time.sleep(1)
        return 5

    @delayed()
    @cached(folder=cache_dir)
    def load_data_2(fix: float):
        time.sleep(1)
        return 3 + fix

    @delayed()
    @cached(folder=cache_dir)
    def add(x, y):
        return x + y

    params = DelayedParameters()
    ts = params.create('ts', value=dt.datetime(2020, 1, 1))
    fix = params.create('fix', value=0.5)
    d1 = load_data_1(ts)
    d2 = load_data_2(fix)
    r = add(d1, d2)

    start = dt.datetime.utcnow()
    (output,) = delayed_compute((r,))
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert 0.95 < delay < 1.95
    assert abs(output - 8.5) < eps

    start = dt.datetime.utcnow()
    (output,) = delayed_compute((r,))
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert delay < 0.95
    assert abs(output - 8.5) < eps

    params.update_many({'ts': dt.datetime(2020, 2, 1), 'fix': 1.5})
    start = dt.datetime.utcnow()
    (output,) = delayed_compute((r,))
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert 0.95 < delay < 1.95
    assert abs(output - 9.5) < eps

    start = dt.datetime.utcnow()
    (output,) = delayed_compute((r,))
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert delay < 0.95
    assert abs(output - 9.5) < eps


def test_dask_pipeline_with_parameters_create_many():
    clear_cache(cache_dir)

    @delayed()
    @cached(folder=cache_dir)
    def load_data_1(ts: dt.datetime):
        assert ts > dt.datetime(2019, 1, 1)
        time.sleep(1)
        return 5

    @delayed()
    @cached(folder=cache_dir)
    def load_data_2(fix: float):
        time.sleep(1)
        return 3 + fix

    @delayed()
    @cached(folder=cache_dir)
    def add(x, y):
        return x + y

    params = DelayedParameters()
    params.create_many({
        'ts': dt.datetime(2020, 1, 1),
        'fix': 0.5,
    })
    print(params.get_params())
    d2 = load_data_2(params.get_delayed('fix'))
    d1 = load_data_1(params.get_delayed('ts'))
    r = add(d1, d2)

    start = dt.datetime.utcnow()
    (output,) = delayed_compute((r,))
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert 0.95 < delay < 1.95
    assert abs(output - 8.5) < eps


def test_dask_pipeline_with_parameters_context():
    clear_cache(cache_dir)

    @delayed()
    @cached(folder=cache_dir)
    def load_data_1(ts: dt.datetime):
        assert ts > dt.datetime(2019, 1, 1)
        return 5

    @delayed()
    @cached(folder=cache_dir)
    def load_data_2(fix: float):
        return 3 + fix

    @delayed()
    @cached(folder=cache_dir)
    def add(x, y):
        return x + y

    params = DelayedParameters()
    ts = params.create('ts', value=dt.datetime(2020, 1, 1))
    fix = params.create('fix', value=0.5)
    d1 = load_data_1(ts)
    d2 = load_data_2(fix)
    r = add(d1, d2)

    (output,) = delayed_compute((r,))
    assert abs(output - 8.5) < eps

    with params.context({'ts': dt.datetime(2020, 2, 1), 'fix': 1.5}):
        (output,) = delayed_compute((r,))
        assert abs(output - 9.5) < eps

    (output,) = delayed_compute((r,))
    assert abs(output - 8.5) < eps


def test_dask_pipeline_with_parameters_private():
    clear_cache(cache_dir)

    @delayed()
    @cached(folder=cache_dir)
    def load_data_1(_ts: dt.datetime):
        time.sleep(1)
        assert _ts > dt.datetime(2019, 1, 1)
        return 5

    @delayed()
    @cached(folder=cache_dir)
    def load_data_2(fix: float):
        time.sleep(1)
        return 3 + fix

    @delayed()
    @cached(folder=cache_dir)
    def add(x, y):
        return x + y

    params = DelayedParameters()
    _ts = params.create('_ts', value=dt.datetime(2020, 1, 1))
    fix = params.create('fix', value=0.5)
    d1 = load_data_1(_ts=_ts)
    d2 = load_data_2(fix=fix)
    r = add(d1, d2)

    start = dt.datetime.utcnow()
    (output,) = delayed_compute((r,))
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert 0.95 < delay < 1.95

    with params.context({'_ts': dt.datetime(2020, 2, 1)}):
        start = dt.datetime.utcnow()
        (output,) = delayed_compute((r,))
        delay = (dt.datetime.utcnow() - start).total_seconds()
        assert delay < 0.95


def test_dask_pipeline_with_parameters_2():
    clear_cache(cache_dir)

    @delayed()
    @cached(folder=cache_dir)
    def load_data_1(ts: dt.datetime):
        assert ts > dt.datetime(2019, 1, 1)
        time.sleep(1)
        return 5

    @delayed()
    @cached(folder=cache_dir)
    def load_data_2(fix: float):
        time.sleep(1)
        return 3 + fix

    @delayed()
    @cached(folder=cache_dir)
    def add(x, y):
        return x + y

    ts = DelayedParameter('ts', value=dt.datetime(2020, 1, 1))
    fix = DelayedParameter('fix', value=0.5)
    d1 = load_data_1(ts())
    d2 = load_data_2(fix())
    r = add(d1, d2)

    start = dt.datetime.utcnow()
    (output,) = delayed_compute((r,))
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert 0.95 < delay < 1.95
    assert abs(output - 8.5) < eps

    start = dt.datetime.utcnow()
    (output,) = delayed_compute((r,))
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert delay < 0.95
    assert abs(output - 8.5) < eps

    ts.set(dt.datetime(2020, 2, 1))
    fix.set(1.5)
    start = dt.datetime.utcnow()
    (output,) = delayed_compute((r,))
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert 0.95 < delay < 1.95
    assert abs(output - 9.5) < eps

    start = dt.datetime.utcnow()
    (output,) = delayed_compute((r,))
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert delay < 0.95
    assert abs(output - 9.5) < eps


def test_dask_pipeline_with_parameters_2_context():
    clear_cache(cache_dir)

    @delayed()
    @cached(folder=cache_dir)
    def load_data_1(ts: dt.datetime):
        assert ts > dt.datetime(2019, 1, 1)
        return 5

    @delayed()
    @cached(folder=cache_dir)
    def load_data_2(fix: float):
        return 3 + fix

    @delayed()
    @cached(folder=cache_dir)
    def add(x, y):
        return x + y

    ts = DelayedParameter('ts', value=dt.datetime(2020, 1, 1))
    fix = DelayedParameter('fix', value=0.5)
    d1 = load_data_1(ts())
    d2 = load_data_2(fix())
    r = add(d1, d2)

    (output,) = delayed_compute((r,))
    assert abs(output - 8.5) < eps

    with ts.context(dt.datetime(2020, 2, 1)), fix.context(1.5):
        (output,) = delayed_compute((r,))
        assert abs(output - 9.5) < eps

    (output,) = delayed_compute((r,))
    assert abs(output - 8.5) < eps


def test_dask_pipeline_multiple_outputs():
    clear_cache(cache_dir)

    @delayed()
    @cached(folder=cache_dir)
    def load_data():
        # time.sleep(1)
        return [1, 1, 1, 2, 2, 2]

    @delayed(nout=2)
    @cached(folder=cache_dir, nout=2)
    def split_data(data):
        return data[:3], data[3:]

    @delayed()
    @cached(folder=cache_dir)
    def compute_sum(arr):
        # time.sleep(1)
        return sum(arr)

    data = load_data()
    x, y = split_data(data)
    xsum = compute_sum(x)
    ysum = compute_sum(y)

    # start = dt.datetime.utcnow()
    (x_, y_, xsum_, ysum_) = delayed_compute((x, y, xsum, ysum))
    # delay = (dt.datetime.utcnow() - start).total_seconds()
    # assert 0.95 < delay < 1.95
    assert x_ == [1, 1, 1]
    assert y_ == [2, 2, 2]
    assert xsum_ == 3
    assert ysum_ == 6


def test_delayed_cached_load_time():
    @delayed_cached(folder=cache_dir, override=False)
    def load_data():
        time.sleep(1)
        return 1

    clear_cache(cache_dir)

    start = dt.datetime.utcnow()
    r = load_data()
    r.compute()
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert delay > 0.95

    start = dt.datetime.utcnow()
    r = load_data()
    r.compute()
    delay = (dt.datetime.utcnow() - start).total_seconds()
    assert delay < 0.95
