# -*- coding: utf-8 -*-

import os
from typing import List
from enum import IntEnum, auto

import numpy as np


class Dtype(IntEnum):
    DSA = auto()
    DFA = auto()
    DDA = auto()
    DSB = auto()
    DFB = auto()
    DDB = auto()

    @staticmethod
    def from_filename(filename: str) -> "Dtype":
        ext = os.path.splitext(filename)[1].strip(".")

        for dtype in Dtype:
            if dtype.name == ext:
                return dtype
        raise BadDataStyleError(f"Invalid file extension. want: {Dtype.list_names}, got: {ext}")

    @staticmethod
    def list_names() -> List[str]:
        return [e.name for e in Dtype]

    @property
    def byte_width(self) -> int:
        if self in [Dtype.DSA, Dtype.DSB]:
            return 2
        if self in [Dtype.DFA, Dtype.DFB]:
            return 4
        if self in [Dtype.DDA, Dtype.DDB]:
            return 8

    @property
    def _format_specifiers(self) -> str:
        if self in [Dtype.DSA, Dtype.DSB]:
            return "%d"
        if self in [Dtype.DFA, Dtype.DFB]:
            return "%e"
        if self in [Dtype.DDA, Dtype.DDB]:
            return "%le"

    @property
    def numpy_dtype(self) -> np.dtype:
        if self in [Dtype.DSA, Dtype.DSB]:
            return np.int16
        if self in [Dtype.DFA, Dtype.DFB]:
            return np.float32
        if self in [Dtype.DDA, Dtype.DDB]:
            return np.float64

    @property
    def is_DXA(self) -> bool:
        """Check if self is DXA (ascii string)"""
        return self in [Dtype.DSA, Dtype.DFA, Dtype.DDA]

    @property
    def is_DXB(self) -> bool:
        """Check if self is DXB (binary)"""
        return self in [Dtype.DSB, Dtype.DFB, Dtype.DDB]

    def __str__(self):
        return self.name


class BadDataStyleError(Exception):
    """Exception class for the invalid file extension error"""
    pass


def len_file(filename: str) -> int:
    """Check the length of data

    If the extension of filename is not .DXX, it throws exception.

    example:
        import dxx
        num_sample = dxx.len_file("example.DSB")
    """
    dtype = Dtype.from_filename(filename)
    return int(os.path.getsize(filename) / dtype.byte_width)


def read(filename: str) -> np.ndarray:
    """Read .DXX file

    If the extension of filename is not .DXX, it throws exception.

    example:
        import dxx
        data = dxx.read("example.DSB")
    """

    dtype = Dtype.from_filename(filename)

    if dtype.is_DXA:
        with open(filename, "r") as f:
            data = np.fromfile(f, dtype.numpy_dtype, -1)

    else:
        with open(filename, "rb") as f:
            data = np.fromfile(f, dtype.numpy_dtype, -1)
    return data


def write(filename: str, data: np.ndarray):
    """Write .DXX file

    If the extension of filename is not .DXX, it throws exception.

    example:
        import dxx
        data = np.random.rand(1024)
        dxx.write("example.DDB", data)
    """

    dtype = Dtype.from_filename(filename)

    data_type = data.dtype
    output_type = dtype.numpy_dtype
    if (data_type == np.float32 or data_type == np.float64) and output_type == np.int16:
        data = _float_to_int16(data)
    elif data_type == np.int16 and output_type == np.float32:
        data = _int16_to_float32(data)
    elif data_type == np.int16 and output_type == np.float64:
        data = _int16_to_float64(data)
    else:
        BadDataStyleError(f"Invalid data type. want: np.int16 or np.float32 or np.float64, got: ", data_type)

    if dtype.is_DXA:
        # save data separated by line breaks
        data.tofile(filename, sep="\n", format=dtype._format_specifiers)

    else:
        data.tofile(filename)


def _float_to_int16(data: np.ndarray) -> np.ndarray:
    amp = 2 ** 15 - 1  # default amp for .DSB
    max_data = np.abs(data).max()
    min_data = np.abs(data).min()
    data = (data - min_data) / (max_data - min_data) * amp
    return data.astype(np.int16)


def _int16_to_float32(data: np.ndarray) -> np.ndarray:
    amp = 10000.0  # default amp for .DFB
    data = data.astype(np.float32)
    max_data = np.abs(data).max()
    min_data = np.abs(data).min()
    data = (data - min_data) / (max_data - min_data) * amp
    return data


def _int16_to_float64(data: np.ndarray) -> np.ndarray:
    amp = 10000.0  # default amp for .DDB
    data = data.astype(np.float64)
    max_data = np.abs(data).max()
    min_data = np.abs(data).min()
    data = (data - min_data) / (max_data - min_data) * amp
    return data
