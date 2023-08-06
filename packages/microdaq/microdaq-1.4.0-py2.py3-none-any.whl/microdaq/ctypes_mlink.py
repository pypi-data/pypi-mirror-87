# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2017-2020, www.microdaq.org

"""Py2/3 Wrapper of the MLink C library"""

__docformat__ = "restructuredtext"

import ctypes, os, sys
from ctypes import *
import platform
import inspect

_int_types = (c_int16, c_int32)

if hasattr(ctypes, "c_int64"):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types


class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [("dummy", c_int)]


def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):

        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x

        p.from_param = classmethod(from_param)

    return p


class UserString:
    def __init__(self, seq):
        if isinstance(seq, str):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return repr(self.data)

    def __int__(self):
        return int(self.data)

    def __long__(self):
        return int(self.data)

    def __float__(self):
        return float(self.data)

    def __complex__(self):
        return complex(self.data)

    def __hash__(self):
        return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)

    def __contains__(self, char):
        return char in self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.__class__(self.data[index])

    def __getslice__(self, start, end):
        start = max(start, 0)
        end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, str):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))

    def __radd__(self, other):
        if isinstance(other, str):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)

    def __mul__(self, n):
        return self.__class__(self.data * n)

    __rmul__ = __mul__

    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self):
        return self.__class__(self.data.capitalize())

    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))

    def count(self, sub, start=0, end=sys.maxsize):
        return self.data.count(sub, start, end)

    def decode(self, encoding=None, errors=None):  # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())

    def encode(self, encoding=None, errors=None):  # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())

    def endswith(self, suffix, start=0, end=sys.maxsize):
        return self.data.endswith(suffix, start, end)

    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))

    def find(self, sub, start=0, end=sys.maxsize):
        return self.data.find(sub, start, end)

    def index(self, sub, start=0, end=sys.maxsize):
        return self.data.index(sub, start, end)

    def isalpha(self):
        return self.data.isalpha()

    def isalnum(self):
        return self.data.isalnum()

    def isdecimal(self):
        return self.data.isdecimal()

    def isdigit(self):
        return self.data.isdigit()

    def islower(self):
        return self.data.islower()

    def isspace(self):
        return self.data.isspace()

    def istitle(self):
        return self.data.istitle()

    def isupper(self):
        return self.data.isupper()

    def join(self, seq):
        return self.data.join(seq)

    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))

    def lower(self):
        return self.__class__(self.data.lower())

    def lstrip(self, chars=None):
        return self.__class__(self.data.lstrip(chars))

    def partition(self, sep):
        return self.data.partition(sep)

    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))

    def rfind(self, sub, start=0, end=sys.maxsize):
        return self.data.rfind(sub, start, end)

    def rindex(self, sub, start=0, end=sys.maxsize):
        return self.data.rindex(sub, start, end)

    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))

    def rpartition(self, sep):
        return self.data.rpartition(sep)

    def rstrip(self, chars=None):
        return self.__class__(self.data.rstrip(chars))

    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)

    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)

    def splitlines(self, keepends=0):
        return self.data.splitlines(keepends)

    def startswith(self, prefix, start=0, end=sys.maxsize):
        return self.data.startswith(prefix, start, end)

    def strip(self, chars=None):
        return self.__class__(self.data.strip(chars))

    def swapcase(self):
        return self.__class__(self.data.swapcase())

    def title(self):
        return self.__class__(self.data.title())

    def translate(self, *args):
        return self.__class__(self.data.translate(*args))

    def upper(self):
        return self.__class__(self.data.upper())

    def zfill(self, width):
        return self.__class__(self.data.zfill(width))


class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""

    def __init__(self, string=""):
        self.data = string

    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")

    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data):
            raise IndexError
        self.data = self.data[:index] + sub + self.data[index + 1 :]

    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data):
            raise IndexError
        self.data = self.data[:index] + self.data[index + 1 :]

    def __setslice__(self, start, end, sub):
        start = max(start, 0)
        end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start] + sub.data + self.data[end:]
        elif isinstance(sub, str):
            self.data = self.data[:start] + sub + self.data[end:]
        else:
            self.data = self.data[:start] + str(sub) + self.data[end:]

    def __delslice__(self, start, end):
        start = max(start, 0)
        end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]

    def immutable(self):
        return UserString(self.data)

    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, str):
            self.data += other
        else:
            self.data += str(other)
        return self

    def __imul__(self, n):
        self.data *= n
        return self


class String(MutableString, Union):

    _fields_ = [("raw", POINTER(c_char)), ("data", c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)

    from_param = classmethod(from_param)


def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)


# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (
        hasattr(type, "_type_")
        and isinstance(type._type_, str)
        and type._type_ != "P"
    ):
        return type
    else:
        return c_void_p


# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self, func, restype, argtypes):
        self.func = func
        self.func.restype = restype
        self.argtypes = argtypes

    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func

    def __call__(self, *args):
        fixed_args = []
        i = 0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i += 1
        return self.func(*fixed_args + list(args[i:]))


# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path
import ctypes
import ctypes.util


def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []


system_lib_32 = {
    "Windows": "MLink32.dll",
    "Darwin": "libmlink.dylib",
    "Linux": "libmlink.so",
}

system_lib_64 = {
    "Windows": "MLink64.dll",
    "Darwin": "libmlink.dylib",
    "Linux": "libmlink.so",
}

archi = {"32bit": ("x86", system_lib_32), "64bit": ("x64", system_lib_64)}

architecture = platform.architecture()[0]
system = platform.system()

try:
    arch_lookup = archi[architecture]
    root_path = os.path.abspath(os.path.dirname(__file__))

    # WA for ARM platforms
    if system == "Linux" and platform.uname()[4].startswith("arm"):
        lib_path = os.path.join(root_path, "armel", "libmlink.so")

    # Windows/Darwin/Linux
    else:
        lib_path = os.path.join(
            root_path, arch_lookup[0], arch_lookup[1][system]
        )

    _libs["MLink"] = cdll.LoadLibrary(lib_path)

except KeyError as err:
    raise RuntimeError(
        "Platform {} {} is not supported.".format(architecture, system)
    )


# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 36
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_error"):
        continue
    mlink_error = _lib.mlink_error
    mlink_error.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        mlink_error.restype = ReturnString
    else:
        mlink_error.restype = String
        mlink_error.errcheck = ReturnString
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 37
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_fw_version"):
        continue
    mlink_fw_version = _lib.mlink_fw_version
    mlink_fw_version.argtypes = [
        POINTER(c_int),
        POINTER(c_int),
        POINTER(c_int),
        POINTER(c_int),
        POINTER(c_int),
    ]
    mlink_fw_version.restype = c_int
    break

for _lib in _libs.values():
    if not hasattr(_lib, "mlink_lib_version"):
        continue
    mlink_lib_version = _lib.mlink_lib_version
    mlink_lib_version.argtypes = [
        POINTER(c_int),
        POINTER(c_int),
        POINTER(c_int),
        POINTER(c_int),
        POINTER(c_int),
    ]
    mlink_lib_version.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 38
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_hwid"):
        continue
    mlink_hwid = _lib.mlink_hwid
    mlink_hwid.argtypes = [POINTER(c_int), POINTER(c_int)]
    mlink_hwid.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 40
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_connect"):
        continue
    mlink_connect = _lib.mlink_connect
    mlink_connect.argtypes = [c_char_p, c_uint16, POINTER(c_int)]
    mlink_connect.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 41
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_disconnect"):
        continue
    mlink_disconnect = _lib.mlink_disconnect
    mlink_disconnect.argtypes = [c_int]
    mlink_disconnect.restype = c_int

    break

for _lib in _libs.values():
    if not hasattr(_lib, "mlink_disconnect_all"):
        continue
    mlink_disconnect_all = _lib.mlink_disconnect_all
    mlink_disconnect_all.restype = c_void
    break

# EXTERNC MDAQ_API int mlink_dsp_init(int *link_fd, char *dsp_binary_path, double rate, double duration);

for _lib in _libs.values():
    if not hasattr(_lib, "mlink_dsp_init"):
        continue
    mlink_dsp_init = _lib.mlink_dsp_init
    mlink_dsp_init.argtypes = [POINTER(c_int), c_char_p, c_double, c_double]
    mlink_dsp_init.restype = c_int
    break

# EXTERNC MDAQ_API int mlink_dsp_start(int *link_fd);
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_dsp_start"):
        continue
    mlink_dsp_start = _lib.mlink_dsp_start
    mlink_dsp_start.argtypes = [POINTER(c_int)]
    mlink_dsp_start.restype = c_int
    break

# EXTERNC MDAQ_API int mlink_dsp_is_done(int *link_fd);
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_dsp_is_done"):
        continue
    mlink_dsp_is_done = _lib.mlink_dsp_is_done
    mlink_dsp_is_done.argtypes = [POINTER(c_int)]
    mlink_dsp_is_done.restype = c_int
    break

# EXTERNC mlink_dsp_wait_until_done(int *link_fd, int timeout);
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_dsp_wait_until_done"):
        continue
    mlink_dsp_wait_until_done = _lib.mlink_dsp_wait_until_done
    mlink_dsp_wait_until_done.argtypes = [POINTER(c_int), c_int]
    mlink_dsp_wait_until_done.restype = c_int
    break

# EXTERNC MDAQ_API int mlink_dsp_signal_read(int *link_fd, int signal_id, int signal_size, double *data, int data_size, int timeout);

for _lib in _libs.values():
    if not hasattr(_lib, "mlink_dsp_signal_read"):
        continue
    mlink_dsp_signal_read = _lib.mlink_dsp_signal_read
    mlink_dsp_signal_read.argtypes = [
        POINTER(c_int),
        c_int,
        c_int,
        POINTER(c_double),
        c_int,
        c_int,
    ]
    mlink_dsp_signal_read.restype = c_int
    break

# EXTERNC MDAQ_API int mlink_dsp_mem_write(int *link_fd, int start_idx, int len, float *data);
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_dsp_mem_write"):
        continue
    mlink_dsp_mem_write = _lib.mlink_dsp_mem_write
    mlink_dsp_mem_write.argtypes = [
        POINTER(c_int),
        c_int,
        c_int,
        POINTER(c_float),
    ]
    mlink_dsp_mem_write.restype = c_int
    break

# EXTERNC MDAQ_API int mlink_dsp_stop(int *link_fd );
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_dsp_stop"):
        continue
    mlink_dsp_stop = _lib.mlink_dsp_stop
    mlink_dsp_stop.argtypes = [POINTER(c_int)]
    mlink_dsp_stop.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 50
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_dio_set_func"):
        continue
    mlink_dio_set_func = _lib.mlink_dio_set_func
    mlink_dio_set_func.argtypes = [POINTER(c_int), c_uint8, c_uint8]
    mlink_dio_set_func.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 51
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_dio_set_dir"):
        continue
    mlink_dio_set_dir = _lib.mlink_dio_set_dir
    mlink_dio_set_dir.argtypes = [POINTER(c_int), c_uint8, c_uint8, c_uint8]
    mlink_dio_set_dir.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 52
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_dio_write"):
        continue
    mlink_dio_write = _lib.mlink_dio_write
    mlink_dio_write.argtypes = [
        POINTER(c_int),
        POINTER(c_uint8),
        POINTER(c_uint8),
        c_uint8,
    ]
    mlink_dio_write.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 53
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_dio_read"):
        continue
    mlink_dio_read = _lib.mlink_dio_read
    mlink_dio_read.argtypes = [
        POINTER(c_int),
        POINTER(c_uint8),
        POINTER(c_uint8),
        c_uint8,
    ]
    mlink_dio_read.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 54
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_led_write"):
        continue
    mlink_led_write = _lib.mlink_led_write
    mlink_led_write.argtypes = [POINTER(c_int), c_uint8, c_uint8]
    mlink_led_write.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 55
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_func_read"):
        continue
    mlink_func_read = _lib.mlink_func_read
    mlink_func_read.argtypes = [POINTER(c_int), c_uint8, POINTER(c_uint8)]
    mlink_func_read.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 58
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_enc_read"):
        continue
    mlink_enc_read = _lib.mlink_enc_read
    mlink_enc_read.argtypes = [
        POINTER(c_int),
        c_uint8,
        POINTER(c_uint8),
        POINTER(c_int32),
    ]
    mlink_enc_read.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 59
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_enc_init"):
        continue
    mlink_enc_init = _lib.mlink_enc_init
    mlink_enc_init.argtypes = [POINTER(c_int), c_uint8, c_uint8, c_int32]
    mlink_enc_init.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 62
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_pwm_init"):
        continue
    mlink_pwm_init = _lib.mlink_pwm_init
    mlink_pwm_init.argtypes = [
        POINTER(c_int),
        c_uint8,
        c_uint32,
        c_uint8,
        c_float,
        c_float,
    ]
    mlink_pwm_init.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 63
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_pwm_write"):
        continue
    mlink_pwm_write = _lib.mlink_pwm_write
    mlink_pwm_write.argtypes = [POINTER(c_int), c_uint8, c_float, c_float]
    mlink_pwm_write.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 66
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_pru_exec"):
        continue
    mlink_pru_exec = _lib.mlink_pru_exec
    mlink_pru_exec.argtypes = [POINTER(c_int), c_char_p, c_uint8, c_uint8]
    mlink_pru_exec.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 67
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_pru_stop"):
        continue
    mlink_pru_stop = _lib.mlink_pru_stop
    mlink_pru_stop.argtypes = [POINTER(c_int), c_uint8]
    mlink_pru_stop.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 68
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_pru_reg_get"):
        continue
    mlink_pru_reg_get = _lib.mlink_pru_reg_get
    mlink_pru_reg_get.argtypes = [
        POINTER(c_int),
        c_uint8,
        c_uint8,
        POINTER(c_uint32),
    ]
    mlink_pru_reg_get.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 69
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_pru_reg_set"):
        continue
    mlink_pru_reg_set = _lib.mlink_pru_reg_set
    mlink_pru_reg_set.argtypes = [POINTER(c_int), c_uint8, c_uint8, c_uint32]
    mlink_pru_reg_set.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 72
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_uart_config"):
        continue
    mlink_uart_config = _lib.mlink_uart_config
    mlink_uart_config.argtypes = [
        POINTER(c_int),
        c_uint8,
        c_uint8,
        c_uint8,
        c_uint8,
        c_uint32,
    ]
    mlink_uart_config.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 73
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_uart_read"):
        continue
    mlink_uart_read = _lib.mlink_uart_read
    mlink_uart_read.argtypes = [
        POINTER(c_int),
        c_uint8,
        c_char_p,
        c_uint32,
        c_int32,
    ]
    mlink_uart_read.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 74
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_uart_write"):
        continue
    mlink_uart_write = _lib.mlink_uart_write
    mlink_uart_write.argtypes = [POINTER(c_int), c_uint8, c_char_p, c_uint32]
    mlink_uart_write.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 75
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_uart_close"):
        continue
    mlink_uart_close = _lib.mlink_uart_close
    mlink_uart_close.argtypes = [POINTER(c_int), c_uint8]
    mlink_uart_close.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 78
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_hs_ai_init"):
        continue
    mlink_hs_ai_init = _lib.mlink_hs_ai_init
    mlink_hs_ai_init.argtypes = [POINTER(c_int)]
    mlink_hs_ai_init.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 79
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_hs_ai_read"):
        continue
    mlink_hs_ai_read = _lib.mlink_hs_ai_read
    mlink_hs_ai_read.argtypes = [
        POINTER(c_int),
        c_uint32,
        c_uint32,
        c_uint32,
        POINTER(c_double),
    ]
    mlink_hs_ai_read.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 82
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_ai_read"):
        continue
    mlink_ai_read = _lib.mlink_ai_read
    # mlink_ai_read(int * link_fd, uint8_t * ch, uint8_t ch_count, double * range, uint8_t * mode, double * data );
    mlink_ai_read.argtypes = [
        POINTER(c_int),
        POINTER(c_uint8),
        c_uint8,
        POINTER(c_double),
        POINTER(c_uint8),
        POINTER(c_double),
    ]
    mlink_ai_read.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 83
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_ao_write"):
        continue
    mlink_ao_write = _lib.mlink_ao_write
    # int mlink_ao_write( int *link_fd, uint8_t *ch, uint8_t ch_count, double *range, uint8_t mode, double *data );
    mlink_ao_write.argtypes = [
        POINTER(c_int),
        POINTER(c_uint8),
        c_uint8,
        POINTER(c_double),
        c_uint8,
        POINTER(c_double),
    ]
    mlink_ao_write.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 84
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_ao_ch_config"):
        continue
    mlink_ao_ch_config = _lib.mlink_ao_ch_config
    mlink_ao_ch_config.argtypes = [
        POINTER(c_int),
        POINTER(c_uint8),
        c_uint8,
        POINTER(c_uint8),
    ]
    mlink_ao_ch_config.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 86
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_ai_scan_init"):
        continue
    mlink_ai_scan_init = _lib.mlink_ai_scan_init
    # mlink_ai_scan_init(int *link_fd, uint8_t *ch, uint8_t ch_count, double *range, uint8_t *mode, float *rate, float duration);
    mlink_ai_scan_init.argtypes = [
        POINTER(c_int),
        POINTER(c_uint8),
        c_uint8,
        POINTER(c_double),
        POINTER(c_uint8),
        POINTER(c_float),
        c_float,
    ]
    mlink_ai_scan_init.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 87
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_ai_scan"):
        continue
    mlink_ai_scan = _lib.mlink_ai_scan
    mlink_ai_scan.argtypes = [
        POINTER(c_int),
        POINTER(c_double),
        c_uint32,
        c_int32,
    ]
    mlink_ai_scan.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 88
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_ai_scan_stop"):
        continue
    mlink_ai_scan_stop = _lib.mlink_ai_scan_stop
    mlink_ai_scan_stop.argtypes = []
    mlink_ai_scan_stop.restype = c_int
    break

for _lib in _libs.values():
    if not hasattr(_lib, "mlink_ai_scan_sync"):
        continue
    mlink_ai_scan_sync = _lib.mlink_ai_scan_sync
    mlink_ai_scan_sync.argtypes = [POINTER(c_int), c_uint8, c_int8]
    mlink_ai_scan_sync.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 90
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_pru_mem_set"):
        continue
    mlink_pru_mem_set = _lib.mlink_pru_mem_set
    mlink_pru_mem_set.argtypes = [
        POINTER(c_int),
        c_uint8,
        c_uint32,
        POINTER(c_uint8),
        c_uint32,
    ]
    mlink_pru_mem_set.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 91
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_pru_mem_get"):
        continue
    mlink_pru_mem_get = _lib.mlink_pru_mem_get
    mlink_pru_mem_get.argtypes = [
        POINTER(c_int),
        c_uint8,
        c_uint32,
        POINTER(c_char),
        c_uint32,
    ]
    mlink_pru_mem_get.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 92
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_get_obj_size"):
        continue
    mlink_get_obj_size = _lib.mlink_get_obj_size
    mlink_get_obj_size.argtypes = [POINTER(c_int), c_char_p, POINTER(c_uint32)]
    mlink_get_obj_size.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 93
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_get_obj"):
        continue
    mlink_get_obj = _lib.mlink_get_obj
    mlink_get_obj.argtypes = [
        POINTER(c_int),
        c_char_p,
        POINTER(None),
        c_uint32,
    ]
    mlink_get_obj.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 94
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_set_obj"):
        continue
    mlink_set_obj = _lib.mlink_set_obj
    mlink_set_obj.argtypes = [
        POINTER(c_int),
        c_char_p,
        POINTER(None),
        c_uint32,
    ]
    mlink_set_obj.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 95
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_mem_open"):
        continue
    mlink_mem_open = _lib.mlink_mem_open
    mlink_mem_open.argtypes = [POINTER(c_int), c_uint32, c_uint32]
    mlink_mem_open.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 96
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_mem_close"):
        continue
    mlink_mem_close = _lib.mlink_mem_close
    mlink_mem_close.argtypes = [POINTER(c_int), c_uint32, c_uint32]
    mlink_mem_close.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 97
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_mem_set"):
        continue
    mlink_mem_set = _lib.mlink_mem_set
    mlink_mem_set.argtypes = [
        POINTER(c_int),
        c_uint32,
        POINTER(c_int8),
        c_uint32,
    ]
    mlink_mem_set.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 98
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_mem_get"):
        continue
    mlink_mem_get = _lib.mlink_mem_get
    mlink_mem_get.argtypes = [
        POINTER(c_int),
        c_uint32,
        POINTER(c_int8),
        c_uint32,
    ]
    mlink_mem_get.restype = c_int
    break

for _lib in _libs.values():
    if not hasattr(_lib, "mlink_ao_scan_init"):
        continue
    # mlink_ao_scan_init(int *link_fd, uint8_t *ch, uint8_t ch_count, float *data, int data_size, double *range,
    # uint8_t stream_mode, float rate, float duration);
    mlink_ao_scan_init = _lib.mlink_ao_scan_init
    mlink_ao_scan_init.argtypes = [
        POINTER(c_int),
        POINTER(c_uint8),
        c_uint8,
        POINTER(c_float),
        c_int,
        POINTER(c_double),
        c_uint8,
        c_float,
        c_float,
    ]
    mlink_ao_scan_init.restype = c_int
    break

# EXTERNC MDAQ_API int mlink_ao_scan_is_done(int *link_fd);
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_ao_scan_is_done"):
        continue
    mlink_ao_scan_is_done = _lib.mlink_ao_scan_is_done
    mlink_ao_scan_is_done.argtypes = [POINTER(c_int)]
    mlink_ao_scan_is_done.restype = c_int
    break

# EXTERNC MDAQ_API int mlink_ao_scan_wait_until_done(int *link_fd, int timeout);
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_ao_scan_wait_until_done"):
        continue
    mlink_ao_scan_wait_until_done = _lib.mlink_ao_scan_wait_until_done
    mlink_ao_scan_wait_until_done.argtypes = [POINTER(c_int), c_int]
    mlink_ao_scan_wait_until_done.restype = c_int
    break

for _lib in _libs.values():
    if not hasattr(_lib, "mlink_ao_scan_data"):
        continue
    mlink_ao_scan_data = _lib.mlink_ao_scan_data
    # mlink_ao_scan_data(int *link_fd, uint8_t *ch, int ch_count, float *data, int data_size, uint8_t opt);
    mlink_ao_scan_data.argtypes = [
        POINTER(c_int),
        POINTER(c_uint8),
        c_int,
        POINTER(c_float),
        c_int,
        c_uint8,
    ]
    mlink_ao_scan_data.restype = c_int
    break

for _lib in _libs.values():
    if not hasattr(_lib, "mlink_ao_scan"):
        continue
    mlink_ao_scan = _lib.mlink_ao_scan
    mlink_ao_scan.argtypes = [POINTER(c_int)]
    mlink_ao_scan.restype = c_int
    break

for _lib in _libs.values():
    if not hasattr(_lib, "mlink_ao_scan_stop"):
        continue
    mlink_ao_scan_stop = _lib.mlink_ao_scan_stop
    mlink_ao_scan_stop.argtypes = [POINTER(c_int)]
    mlink_ao_scan_stop.restype = c_int
    break

# int mlink_scan_trigger_clear(int *link_fd, uint8_t trigger);
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_scan_trigger_clear"):
        continue
    mlink_scan_trigger_clear = _lib.mlink_scan_trigger_clear
    mlink_scan_trigger_clear.argtypes = [POINTER(c_int), c_uint8]
    mlink_scan_trigger_clear.restype = c_int
    break

# int mlink_scan_trigger_dio(int *link_fd, uint8_t trigger, uint8_t dio, uint8_t level);
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_scan_trigger_dio"):
        continue
    mlink_scan_trigger_dio = _lib.mlink_scan_trigger_dio
    mlink_scan_trigger_dio.argtypes = [
        POINTER(c_int),
        c_uint8,
        c_uint8,
        c_uint8,
    ]
    mlink_scan_trigger_dio.restype = c_int
    break

# int mlink_scan_trigger_dio_pattern(int *link_fd, uint8_t trigger,  char *pattern, int len);
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_scan_trigger_dio_pattern"):
        continue
    mlink_scan_trigger_dio_pattern = _lib.mlink_scan_trigger_dio_pattern
    mlink_scan_trigger_dio_pattern.argtypes = [
        POINTER(c_int),
        c_uint8,
        POINTER(c_char),
        c_uint8,
    ]
    mlink_scan_trigger_dio_pattern.restype = c_int
    break

# int mlink_scan_trigger_encoder(int *link_fd, uint8_t trigger, uint8_t module, int32_t position, uint8_t slope);
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_scan_trigger_encoder"):
        continue
    mlink_scan_trigger_encoder = _lib.mlink_scan_trigger_encoder
    mlink_scan_trigger_encoder.argtypes = [
        POINTER(c_int),
        c_uint8,
        c_uint8,
        c_int32,
        c_uint8,
    ]
    mlink_scan_trigger_encoder.restype = c_int
    break

# int mlink_scan_trigger_external_start(int *link_fd, uint8_t trigger, uint8_t src);
for _lib in _libs.values():
    if not hasattr(_lib, "mlink_scan_trigger_external_start"):
        continue
    mlink_scan_trigger_external_start = _lib.mlink_scan_trigger_external_start
    mlink_scan_trigger_external_start.argtypes = [
        POINTER(c_int),
        c_uint8,
        c_uint8,
    ]
    mlink_scan_trigger_external_start.restype = c_int
    break
# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 15

try:
    AO_0_TO_5V = 0
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 16
try:
    AO_0_TO_10V = 1
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 17
try:
    AO_PLUS_MINUS_5V = 2
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 18
try:
    AO_PLUS_MINUS_10V = 3
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 19
try:
    AO_PLUS_MINUS_2V5 = 4
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 22
try:
    AI_10V = 0
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 23
try:
    AI_5V = 1
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 27
try:
    AI_BIPOLAR = 0
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 28
try:
    AI_UNIPOLAR = 1
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 31
try:
    AI_SINGLE = 0
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 32
try:
    AI_DIFF = 1
except:
    pass

# No inserted files
