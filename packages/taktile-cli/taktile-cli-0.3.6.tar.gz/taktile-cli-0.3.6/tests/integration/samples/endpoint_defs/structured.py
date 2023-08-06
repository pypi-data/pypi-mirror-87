import random

import numpy

from tktl import Tktl

from ..data.sample_data import (
    FLOAT_NANS_FRAME,
    MIXED_FRAME,
    TestingArrays,
    TestingFrames,
    make_base_frame,
    random_sample,
)

tktl = Tktl()
# initialize dictionaries
model = {}
X_test = {}
y_test = {}

random.seed(10)
numpy.random.seed(10)

base_frame = make_base_frame(100, 5)
test_df = TestingFrames.complete_frame(base_frame, [MIXED_FRAME, FLOAT_NANS_FRAME])

test_labels = TestingArrays.labels(
    length=len(test_df), kind="regression", null_pct=0.2, as_series=True
)

test_labels_arr = test_labels.values

test_labels_bool_series = TestingArrays.labels(
    length=len(test_df), kind="binary", null_pct=0.2, bool_labels=True, as_series=True
)

test_labels_bool_arr = test_labels_bool_series.values


@tktl.endpoint(kind="regression", X=test_df, y=test_labels_bool_series)
def pandas_regression_df_series(df):
    return test_labels.sample(len(df))


@tktl.endpoint(kind="binary", X=test_df, y=test_labels_bool_series)
def pandas_binary_df_series(df):
    return test_labels_bool_series.sample(len(df))


@tktl.endpoint(kind="custom", X=test_df, y=test_labels_bool_series)
def pandas_custom_df_series(df):
    return test_labels_bool_series.sample(len(df))


@tktl.endpoint(kind="regression", X=test_df, y=test_labels_bool_series)
def pandas_regression_df_arr(df):
    return random_sample(test_labels_arr, size=len(df))


@tktl.endpoint(kind="binary", X=test_df, y=test_labels_bool_series)
def pandas_binary_df_arr(df):
    return random_sample(test_labels_bool_arr, size=len(df))


@tktl.endpoint(kind="custom", X=test_df, y=test_labels_bool_series)
def pandas_custom_df_arr(df):
    return random_sample(test_labels_bool_arr, size=len(df))
