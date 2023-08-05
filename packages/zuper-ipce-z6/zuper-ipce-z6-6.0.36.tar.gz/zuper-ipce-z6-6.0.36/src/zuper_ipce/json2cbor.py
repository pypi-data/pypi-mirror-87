import io
import json
import select
import time
import traceback
from io import BufferedReader
from json import JSONDecodeError
from typing import Iterator

import base58
import cbor2
from cbor2 import CBORDecodeEOF

from . import logger
from .json_utils import (
    decode_bytes_before_json_deserialization,
    encode_bytes_before_json_serialization,
)
from .utils_text import oyaml_dump

__all__ = [
    "read_cbor_or_json_objects",
    "json2cbor_main",
    "cbor2json_main",
    "cbor2yaml_main",
    "read_next_cbor",
    "read_next_either_json_or_cbor",
    "tag_hook",
]


def json2cbor_main() -> None:
    fo = open("/dev/stdout", "wb", buffering=0)
    fi = open("/dev/stdin", "rb", buffering=0)
    # noinspection PyTypeChecker
    fi = BufferedReader(fi, buffer_size=1)
    for j in read_cbor_or_json_objects(fi):
        c = cbor2.dumps(j)
        fo.write(c)
        fo.flush()


def cbor2json_main() -> None:
    fo = open("/dev/stdout", "wb", buffering=0)
    fi = open("/dev/stdin", "rb", buffering=0)

    for j in read_cbor_objects(fi):
        j = encode_bytes_before_json_serialization(j)
        ob = json.dumps(j)
        ob = ob.encode("utf-8")
        fo.write(ob)
        fo.write(b"\n")
        fo.flush()


def cbor2yaml_main() -> None:
    fo = open("/dev/stdout", "wb")
    fi = open("/dev/stdin", "rb")
    for j in read_cbor_objects(fi):
        ob = oyaml_dump(j)
        ob = ob.encode("utf-8")
        fo.write(ob)
        fo.write(b"\n")
        fo.flush()


def read_cbor_or_json_objects(f, timeout=None) -> Iterator:
    """ Reads cbor or line-separated json objects from the binary file f."""
    while True:
        try:
            ob = read_next_either_json_or_cbor(f, timeout=timeout)
            yield ob
        except StopIteration:
            break
        except TimeoutError:
            raise


def read_cbor_objects(f, timeout=None) -> Iterator:
    """ Reads cbor or line-separated json objects from the binary file f."""
    while True:
        try:
            ob = read_next_cbor(f, timeout=timeout)
            yield ob
        except StopIteration:
            break
        except TimeoutError:
            raise


def read_next_either_json_or_cbor(f, timeout=None, waiting_for: str = None) -> dict:
    """ Raises StopIteration if it is EOF.
        Raises TimeoutError if over timeout"""
    fs = [f]
    t0 = time.time()
    intermediate_timeout = 3.0

    while True:
        try:
            readyr, readyw, readyx = select.select(fs, [], fs, intermediate_timeout)
        except io.UnsupportedOperation:
            break
        if readyr:
            break
        elif readyx:
            logger.warning("Exceptional condition on input channel %s" % readyx)
        else:
            delta = time.time() - t0
            if (timeout is not None) and (delta > timeout):
                msg = "Timeout after %.1f s." % delta
                logger.error(msg)
                raise TimeoutError(msg)
            else:
                msg = "I have been waiting %.1f s." % delta
                if timeout is None:
                    msg += " I will wait indefinitely."
                else:
                    msg += " Timeout will occurr at %.1f s." % timeout
                if waiting_for:
                    msg += " " + waiting_for
                logger.warning(msg)

    first = f.peek(1)[:1]
    if len(first) == 0:
        msg = "Detected EOF on %s." % f
        if waiting_for:
            msg += " " + waiting_for
        raise StopIteration(msg)

    # logger.debug(f'first char is {first}')
    if first in [b" ", b"\n", b"{"]:
        line = f.readline()
        line = line.strip()
        if not line:
            msg = "Read empty line. Re-trying."
            logger.warning(msg)
            return read_next_either_json_or_cbor(f)
        # logger.debug(f'line is {line!r}')
        try:
            j = json.loads(line)
        except JSONDecodeError:
            msg = f"Could not decode line {line!r}: {traceback.format_exc()}"
            logger.error(msg)
            return read_next_either_json_or_cbor(f)
        j = decode_bytes_before_json_deserialization(j)
        return j

    else:

        j = cbor2.load(f, tag_hook=tag_hook)

        return j


def tag_hook(decoder, tag, shareable_index=None) -> dict:
    if tag.tag != 42:
        return tag

    d = tag.value
    val = base58.b58encode(d).decode("ascii")
    val = "z" + val[1:]
    return {"/": val}


def wait_for_data(f, timeout=None, waiting_for: str = None):
    """ Raises StopIteration if it is EOF.
            Raises TimeoutError if over timeout"""
    # XXX: StopIteration not implemented
    fs = [f]
    t0 = time.time()
    intermediate_timeout = 3.0

    while True:
        try:
            readyr, readyw, readyx = select.select(fs, [], fs, intermediate_timeout)
        except io.UnsupportedOperation:
            break
        if readyr:
            break
        elif readyx:
            logger.warning(f"Exceptional condition on input channel {readyx}")
        else:
            delta = time.time() - t0
            if (timeout is not None) and (delta > timeout):
                msg = f"Timeout after {delta:.1f} s."
                logger.error(msg)
                raise TimeoutError(msg)
            else:
                msg = f"I have been waiting {delta:.1f} s."
                if timeout is None:
                    msg += " I will wait indefinitely."
                else:
                    msg += f" Timeout will occurr at {timeout:.1f} s."
                if waiting_for:
                    msg += " " + waiting_for
                logger.warning(msg)


def read_next_cbor(f, timeout=None, waiting_for: str = None) -> dict:
    """ Raises StopIteration if it is EOF.
        Raises TimeoutError if over timeout"""
    wait_for_data(f, timeout, waiting_for)

    try:
        j = cbor2.load(f, tag_hook=tag_hook)
        return j
    except CBORDecodeEOF:
        raise StopIteration from None
    except OSError as e:
        if e.errno == 29:
            raise StopIteration from None
        raise
