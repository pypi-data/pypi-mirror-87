import random
from random import randint, sample
from typing import Dict, List, Tuple, Union

import numpy

random.seed(10)
numpy.random.seed(10)


import pandas
from pandas._testing import (
    makeCustomDataframe,
    makeDataFrame,
    makeFloatSeries,
    makeMissingDataframe,
    makeMixedDataFrame,
    makeObjectSeries,
    makeTimeSeries,
)


def make_base_frame(r, c) -> pandas.DataFrame:
    return makeCustomDataframe(r, c, r_idx_type="i")


FLOAT_NANS_FRAME: pandas.DataFrame = makeMissingDataframe()
MIXED_FRAME: pandas.DataFrame = makeMixedDataFrame()


class TestingFrames:
    BASE_FRAME = makeCustomDataframe(
        5, 10, data_gen_f=lambda r, c: randint(1, 100), r_idx_type="i"
    )
    MISSING_FRAME = makeMissingDataframe()

    @staticmethod
    def complete_frame(
        base_frame: pandas.DataFrame, frames: List[pandas.DataFrame]
    ) -> pandas.DataFrame:
        rows = len(base_frame)
        print(base_frame.shape)
        for frame in frames:
            print(frame.shape)
            if len(frame) > rows:
                frame = frame.head(rows)
            else:
                frac = rows // len(frame)
                frame = pandas.concat([frame] * frac).reset_index()
                diff = rows - len(frame)
                frame = pandas.concat([frame, frame.head(diff)]).reset_index()
            base_frame = pandas.concat([base_frame, frame], axis=1, ignore_index=True)
        base_frame.columns = [str(c) for c in base_frame.columns]
        return base_frame


def make_base_array(dims: Tuple[int]) -> numpy.array:
    return numpy.random.randn(*dims)


def mask_array(x, fill_value, pct) -> numpy.array:
    num_values = int(len(x) * pct)
    idx = numpy.arange(len(x))
    numpy.random.shuffle(idx)
    x[idx[:num_values]] = fill_value
    return x


class TestingArrays:
    @classmethod
    def from_frame(cls, df: pandas.DataFrame) -> numpy.array:
        return df.to_numpy()

    @classmethod
    def labels(
        cls,
        length: int,
        as_series: bool = False,
        null_pct: float = 0,
        kind: str = "regression",
        params: Tuple = (0, 1),
        bool_labels: bool = False,
    ) -> Union[numpy.array, pandas.Series]:
        """

        Parameters
        ----------
        bool_labels
        length
        as_series
        null_pct
        kind
        params : Tuple
            u, sigma

        Returns
        -------

        """
        if kind == "regression":
            arr = params[0] + params[1] * numpy.random.random(length)

        else:
            if bool_labels:
                arr = numpy.random.choice(a=[False, True], size=length, p=[0.5, 0.5])
            else:
                arr = numpy.random.uniform(size=length)
        masked = mask_array(arr, None, null_pct)
        return pandas.Series(masked) if as_series else arr


class TestingSequence:
    @classmethod
    def from_frame(cls, df: pandas.DataFrame) -> List[Dict]:
        return df.to_dict(orient="records")

    @classmethod
    def from_array(cls, arr: numpy.array) -> List:
        return arr.tolist()


def random_sample(arr: numpy.array, size: int = 1) -> numpy.array:
    return arr[numpy.random.choice(len(arr), size=size, replace=False)]
