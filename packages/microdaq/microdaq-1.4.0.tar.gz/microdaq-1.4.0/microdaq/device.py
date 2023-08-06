# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2017-2020, www.microdaq.org

import ctypes
from functools import wraps

import microdaq.ctypes_mlink as cml


class MLinkError(Exception):
    """Error returned by MLink library."""

    def __init__(self, error_code, error_desc):
        self.error_code = error_code
        self.error_desc = error_desc

    def __str__(self):
        return repr(self.error_desc)


class AIRange(object):
    """Analog input ranges in volts."""

    AI_10V = [-10, 10]
    AI_10V_UNI = [0, 10]

    AI_5V = [-5, 5]
    AI_5_12V = [-5.12, 5.12]

    AI_2V = [-2, 2]
    AI_2_56V = [-2.56, 2.56]

    AI_1V = [-1, 1]
    AI_1_24V = [-1.24, 1.24]

    AI_0_64V = [-0.64, 0.64]


class AORange(object):
    """Analog output ranges in volts."""

    AO_10V = [-10, 10]
    AO_10V_UNI = [0, 10]

    AO_5V = [-5, 5]
    AO_5V_UNI = [0, 5]

    AO_2_5V = [-2.5, 2.5]


class Triggers(object):
    """Type of analog input and output triggers."""

    AI_TRIGGER = 1
    AO_TRIGGER = 2
    DSP_START = 3
    AI_SCAN_START = 2
    AO_SCAN_START = 2
    EDGE_FALLING = 1
    EDGE_RISING = 2


def _connect_decorate(func):
    @wraps(func)
    def func_wrapper(self, *original_args, **original_kwargs):
        if self._connectionless:
            self.reconnect()
            ans = func(self, *original_args, **original_kwargs)
            self.disconnect()
        else:
            ans = func(self, *original_args, **original_kwargs)
        return ans

    return func_wrapper


class Device:
    """
    Description:
        Main class of MLink binding. Represents MicroDAQ device.
    Usage:
        MLink(ip, maintain_connection=False)
        ip - IP address of MicroDAQ device
        maintain_connection - True or False
            True  - more convenient, no needs to keep connection (each function call connect()
                    method), slightly less performance
            False - better performance, user has to worry about connection timeout (depends on OS)
                    To keep connection call method reconnect() or any other method.
    """

    def __init__(self, ip="10.10.1.1", maintain_connection=False):
        self._linkfd = -1
        self._ip = ip
        self._connectionless = maintain_connection
        self._ao_scan_ch = 0
        self._mdaq_hwid = 0
        self.disconnect()
        self._ai_scan_channels = None
        self.connect(ip)
        self._hwid()
        self.disconnect()

        if not self._connectionless:
            self.connect(ip)

    @staticmethod
    def _get_error(errcode):
        return cml.mlink_error(errcode)

    def _raise_exception(self, res):
        if res == -1:
            raise MLinkError(
                res,
                "Session timeout, restore connection with reconnect()"
                " or connect(ip) method.",
            )
        elif res < -1:
            raise MLinkError(res, self._get_error(res))

    @_connect_decorate
    def _hwid(self):
        hwid_raw = ctypes.c_int * 5
        hwid_raw = hwid_raw(0)

        res = cml.mlink_hwid(
            ctypes.pointer(self._linkfd), ctypes.byref(hwid_raw)
        )

        self._mdaq_hwid = hwid_raw
        self._raise_exception(res)

    def disconnect(self):
        """
        Description:
            Disconnects from MicroDAQ device
        Usage:
            disconnect()
        """

        cml.mlink_disconnect_all()

    def connect(self, ip):
        """
        Description:
            Connects to MicroDAQ device
        Usage:
            connect(ip)
            ip - MicroDAQ IP address
        """

        self._linkfd = ctypes.c_int32()
        self._ip = ip

        res = cml.mlink_connect(
            ip.encode(), 4343, ctypes.pointer(self._linkfd)
        )
        self._raise_exception(res)

    def reconnect(self):
        """
        Description:
            Connects to MicroDAQ device with most recent IP address
            obtained from class constructor or connect method
        Usage:
            reconnect()
        """

        if self._ip is not None:
            self.disconnect()
            self.connect(self._ip)

    @_connect_decorate
    def get_fw_version(self):
        """
        Description:
            Returns the MicroDAQ firmware version
        Usage:
            (major, minor, fix, build) = get_fw_version()
        """

        major = ctypes.c_int()
        minor = ctypes.c_int()
        fix = ctypes.c_int()
        build = ctypes.c_int()

        res = cml.mlink_fw_version(
            ctypes.pointer(self._linkfd),
            ctypes.pointer(major),
            ctypes.pointer(minor),
            ctypes.pointer(fix),
            ctypes.pointer(build),
        )

        self._raise_exception(res)

        return major.value, minor.value, fix.value, build.value

    def get_lib_version(self):
        """
        Description:
            Returns the MLink library version
        Usage:
            (major, minor, fix, build) = get_lib_version()
        """
        major = ctypes.c_int()
        minor = ctypes.c_int()
        fix = ctypes.c_int()
        build = ctypes.c_int()

        res = cml.mlink_lib_version(
            ctypes.pointer(self._linkfd),
            ctypes.pointer(major),
            ctypes.pointer(minor),
            ctypes.pointer(fix),
            ctypes.pointer(build),
        )

        self._raise_exception(res)

        return major.value, minor.value, fix.value, build.value

    def get_str_hw_info(self):
        """
        Description:
            Returns string with model of a connected MicroDAQ device
            example output: 'MicroDAQ E2000-ADC09-DAC06-12'
        Usage:
            model = get_str_hw_info()

        """

        return "MicroDAQ E%d-ADC%d-DAC%d-%d%d" % tuple(self._mdaq_hwid)

    def get_hw_info(self):
        """
        Description:
            Returns tuple with model description of a connected MicroDAQ device
        Usage:
            (series, adc, dac, cpu, mem) = get_hw_info()
        """

        return tuple(self._mdaq_hwid)

    @_connect_decorate
    def dsp_init(self, dsp_application, rate, duration):
        """
        Description:
            Initializes DSP processor with given applicaiton
        Usage:
            dsp_init(dsp_firmware, rate, duration)
            dsp_application - XCos generated DSP application
            rate - DSP application step per second rate (-1 - keep Xcos settings)
            duration - task duration in seconds (-1 - infinity)
        """

        res = cml.mlink_dsp_init(
            ctypes.pointer(self._linkfd),
            dsp_application.encode(),
            rate,
            duration,
        )

        self._raise_exception(res)

    @_connect_decorate
    def dsp_start(self):
        """
        Description:
            Starts execution of DSP application
        Usage:
            dsp_start()
        """

        res = cml.mlink_dsp_start(ctypes.pointer(self._linkfd))

        self._raise_exception(res)

    @_connect_decorate
    def dsp_is_done(self):
        """
        Description:
            Cheks if DSP execution is done.
        Usage:
            dsp_is_done()
        """

        res = cml.mlink_dsp_is_done(ctypes.pointer(self._linkfd))

        self._raise_exception(res)

        if res == 0:
            return False
        elif res == 1:
            return True

    @_connect_decorate
    def dsp_wait_until_done(self, timeout):
        """
        Description:
            Waits until DSP application is done.
        Usage:
            dsp_wait_until_done(timeout)
            timeout - amount of time in seconds to wait (-1 - wait indefinitely)
        """

        if timeout > 0:
            timeout = timeout * 1000

        res = cml.mlink_dsp_wait_until_done(
            ctypes.pointer(self._linkfd), timeout
        )

        self._raise_exception(res)

    @_connect_decorate
    def dsp_mem_write(self, index, data):
        """
        Description:
            Writes data to MicroDAQ memory accesable by XCos
            MEM read block.
        Usage:
            dsp_mem_write(index, data)
            index - memory beggining index
            data - data to be written
        """

        if not isinstance(data, list):
            data = [data]

        data_c = ctypes.c_float * len(data)
        data_c = data_c(*data)

        res = cml.mlink_dsp_mem_write(
            ctypes.pointer(self._linkfd), index, len(data), data_c
        )

        self._raise_exception(res)

    @_connect_decorate
    def dsp_signal_read(self, signal_id, vector_size, vector_count, timeout=1):
        """
        Description:
            Reads data from DSP application during its execution
        Usage:
            data = dsp_signal_read(signal_id, vector_size, vector_count, timeout=1)
            signal_id - SIGNAL block identification number from XCOS model.
            vector_size - SIGNAL block data size.
            vector_count - vectors to read.
            timeout - maximum amount of time to wait for data in seconds
        """

        timeout = timeout * 1000
        data_size = vector_size * vector_count
        data = ctypes.c_double * data_size
        data = data()
        res = cml.mlink_dsp_signal_read(
            ctypes.pointer(self._linkfd),
            signal_id,
            vector_size,
            ctypes.byref(data),
            data_size,
            timeout,
        )

        self._raise_exception(res)
        val_list = []

        for vec in range(0, vector_count):
            val_list.append(
                [data[i + (vec * vector_size)] for i in range(0, vector_size)]
            )

        return val_list

    @_connect_decorate
    def dsp_stop(self):
        """
        Description:
            Stops DSP program
        Usage:
            dsp_stop()
        """

        res = cml.mlink_dsp_stop(ctypes.pointer(self._linkfd))
        self._raise_exception(res)

    @_connect_decorate
    def dio_func(self, func, state):
        """
        Description:
            Sets DIO alternative function
        Usage:
            dio_func(func, state)
            func - DIO alternative function
                1 - ENC1: DIO1 - Channel A, DIO2 - Channel B (enabled by default)
                2 - ENC2: DIO3 - Channel A, DIO4 - Channel B (enabled by default)
                3 - PWM1: DIO10 - Channel A, DIO11 - Channel B (enabled by default)
                4 - PWM2: DIO12 - Channel A, DIO13 - Channel B (enabled by default)
                5 - PWM3: DIO14 - Channel A, DIO15 - Channel B (enabled by default)
                6 - UART: DIO8 - Rx, DIO9 - Tx (enabled by default)
            state - function state (True/False to enable/disable function)
        """

        res = cml.mlink_dio_set_func(ctypes.pointer(self._linkfd), func, state)
        self._raise_exception(res)

    @_connect_decorate
    def dio_dir(self, bank, direction):
        """
        Description:
            Sets MicroDAQ DIO bank direction
        Usage:
            dio_dir(bank, direction)
            bank - bank number (1-4)
            direction - bank direction (True - output, False - input)
        """

        res = cml.mlink_dio_set_dir(
            ctypes.pointer(self._linkfd), bank, direction, 0
        )
        self._raise_exception(res)

    @_connect_decorate
    def dio_read(self, dio):
        """
        Description:
            Reads DIO state
        Usage:
            dio_read(dio)
            dio - DIO number
        """
        if not isinstance(dio, list):
            dio = [dio]

        dio_idx = ctypes.c_uint8 * len(dio)
        dio_idx = dio_idx(*dio)

        dio_val = ctypes.c_uint8 * len(dio)
        dio_val = dio_val()

        res = cml.mlink_dio_read(
            ctypes.pointer(self._linkfd),
            ctypes.byref(dio_idx),
            ctypes.byref(dio_val),
            len(dio),
        )
        self._raise_exception(res)

        val_list = list(dio_val)

        if len(val_list) == 1:
            return val_list[0]
        else:
            return val_list

    @_connect_decorate
    def dio_write(self, dio, state):
        """
        Description:
            Writes DIO state
        Usage:
            dio_write(dio, state)
            dio - DIO numbers
            state - DIO output states
        """

        if not isinstance(dio, list):
            dio = [dio]
        if not isinstance(state, list):
            state = [state]

        if len(dio) != len(state):
            raise ValueError(
                "dio_write: Number of channels and data is not equal!"
            )

        dio_idx = ctypes.c_uint8 * len(dio)
        dio_idx = dio_idx(*dio)

        dio_val = ctypes.c_uint8 * len(dio)
        dio_val = dio_val(*state)

        res = cml.mlink_dio_write(
            ctypes.pointer(self._linkfd),
            ctypes.byref(dio_idx),
            ctypes.byref(dio_val),
            len(dio),
        )
        self._raise_exception(res)

    @_connect_decorate
    def func_key_read(self, key):
        """
        Description:
            Reads MicroDAQ function key state
        Usage:
            func_key_read(key)
            key - key number (1 or 2)
        """

        value = ctypes.c_uint8()
        res = cml.mlink_func_read(
            ctypes.pointer(self._linkfd), key, ctypes.pointer(value)
        )
        self._raise_exception(res)

        return value.value

    @_connect_decorate
    def led_write(self, led, state):
        """
        Description:
            Sets MicroDAQ LEDs state
        Usage:
            led_write(led, state)
            led - LED number (1 or 2)
            state - LED state (True - ON, False - OFF)
        """

        res = cml.mlink_led_write(ctypes.pointer(self._linkfd), led, state)
        self._raise_exception(res)

    @_connect_decorate
    def enc_init(self, module, mode=0, init_value=0):
        """
        Description:
            Initializes encoder module
        Usage:
            enc_init(encoder, init_value)
            module - encoder module (1 or 2)
            mode - mode - encoder counter mode
                0 - quadrature - ENCxA and ENCxB inputs are used for A and B channels
                1 - dir - ENCxA input will provide the clock for position counter and the ENCxB
                          input will have the direction information. The position counteris
                          incremented on every rising edge of ENCxA input when the direction
                          input is high and decremented when the direction input is low.
                2 - up - position counter is incremented on both edges of the ENCxA input.
                3 - down - position counter is decremented on both edges of the ENCxA input.
            init_value - initial encoder value
        """

        res = cml.mlink_enc_init(
            ctypes.pointer(self._linkfd), module, mode, init_value
        )
        self._raise_exception(res)

    @_connect_decorate
    def enc_read(self, module):
        """
        Description:
            Reads encoder position and motion direction
        Usage:
            enc_read(encoder)
            module - encoder module (1 or 2)
        """

        enc_dir = ctypes.c_uint8()
        position = ctypes.c_int32()
        res = cml.mlink_enc_read(
            ctypes.pointer(self._linkfd),
            module,
            ctypes.pointer(enc_dir),
            ctypes.pointer(position),
        )

        self._raise_exception(res)
        return position.value, enc_dir.value

    @_connect_decorate
    def pwm_init(self, module, period, active_low=False, duty_a=0, duty_b=0):
        """
        Description:
            Setup MicroDAQ PWM outputs
        Usage:
            pwm_init(module, period, active_low=False, duty_a=0, duty_b=0)
            module - PWM module (1, 2 or 3)
            period - PWM module period in microseconds(1-1000000)
            active_low - PWM waveform polarity (True or False)
            duty_a - PWM channel A duty (0-100)
            duty_b - PWM channel B duty (0-100)
        """

        res = cml.mlink_pwm_init(
            ctypes.pointer(self._linkfd),
            module,
            period,
            active_low,
            duty_a,
            duty_b,
        )

        self._raise_exception(res)

    @_connect_decorate
    def pwm_write(self, module, duty_a, duty_b):
        """
        Description:
            Sets MicroDAQ PWM outputs
        Usage:
            pwm_write(module, duty_a, duty_b)
            module - PWM module (1, 2 or 3)
            duty_a - PWM channel A duty (0-100)
            duty_b - PWM channel B duty (0-100)
        """

        res = cml.mlink_pwm_write(
            ctypes.pointer(self._linkfd), module, duty_a, duty_b
        )

        self._raise_exception(res)

    @_connect_decorate
    def ai_read(
        self, channels, ai_range=AIRange.AI_10V, is_differential=False
    ):
        """
        Description:
            Reads MicroDAQ analog inputs
        Usage:
            ai_read(channels, range=AIRange.AI_10V, is_differential=False)
            channels - analog input channels to read
            ai_range - analog input range:
                AI_10V     - [-10, 10]
                AI_10V_UNI - [0, 10]
                AI_5V      - [-5, 5]
                AI_5_12V   - [-5.12, 5.12]
                AI_2V      - [-2, 2]
                AI_2_56V   - [-2.56, 2.56]
                AI_1V      - [-1, 1]
                AI_1_24V   - [-1.24, 1.24]
                AI_0_64V   - [-0.64, 0.64]
                AIRange.AI_10V  -    single-range argument applied for all used channels
                AIRange.AI_10V  + AIRange.AI_5V  - multi-range argument for two channels

            is_differential - scalar or array with measurement mode settings:
                              True  - differential
                              False - single-ended mode

        Return:
            Voltage on every 'channel'. Float type if 'channel' parameter is
            a single int (scalar), a list of floats if 'channel' parameter
            is a list of ints.

            [value1, value2] = ai_read([1, 2])
            [value] =  ai_read([1])
            value = ai_read(1)
        """

        if not isinstance(channels, list):
            channels = [channels]

        if not isinstance(is_differential, list):
            is_differential = [is_differential]

        if len(is_differential) == 1 and len(channels) != 1:
            is_differential_cpy = is_differential
            for i in range(len(channels) - 1):
                is_differential = is_differential + is_differential_cpy
        elif len(channels) != len(is_differential):
            raise ValueError(
                "ai_read: Mode (is_differential parameter) vector"
                " should match selected AI channels"
            )

        if len(ai_range) == 2 and len(channels) != 1:
            range_cpy = ai_range
            for i in range(len(channels) - 1):
                ai_range = ai_range + range_cpy
        elif len(channels) != len(ai_range) / 2:
            raise ValueError(
                "ai_read: Range vector should match selected AI channels!"
            )

        channels_idx = ctypes.c_int8 * len(channels)
        channels_idx = channels_idx(*channels)
        channels_val = ctypes.c_double * (len(channels))
        channels_val = channels_val()
        channels_range = ctypes.c_double * (len(ai_range))
        channels_range = channels_range(*ai_range)

        diff = ctypes.c_int8 * len(is_differential)
        diff = diff(*is_differential)

        res = cml.mlink_ai_read(
            ctypes.pointer(self._linkfd),
            ctypes.byref(channels_idx),
            len(channels),
            ctypes.byref(channels_range),
            ctypes.byref(diff),
            ctypes.byref(channels_val),
        )

        self._raise_exception(res)

        val_list = [channels_val[i] for i in range(len(channels))]

        if not isinstance(channels, list):
            return val_list[0]
        else:
            return val_list

    @_connect_decorate
    def ai_scan_init(
        self, channels, ai_range, is_differential, rate, duration
    ):
        """
        Description:
            Initiates analog input scanning session
        Usage:
            ai_scan_init(channels, ai_range, is_differential, rate, duration)
            channels - analog input channels to read
            ai_range - analog input range:
                AI_10V     - [-10, 10]
                AI_10V_UNI - [0, 10]
                AI_5V      - [-5, 5]
                AI_5_12V   - [-5.12, 5.12]
                AI_2V      - [-2, 2]
                AI_2_56V   - [-2.56, 2.56]
                AI_1V      - [-1, 1]
                AI_1_24V   - [-1.24, 1.24]
                AI_0_64V   - [-0.64, 0.64]
                AIRange.AI_10V  -    single-range argument applied for all used channels
                AIRange.AI_10V  + AIRange.AI_5V  - multi-range argument for two channels

            is_differential - scalar or array with terminal configuration settings:
                              True  - differential
                              False - single-ended mode
            rate - analog input scan frequency [Hz]
            duration - analog input scan duration in seconds
        """
        if not isinstance(channels, list):
            channels = [channels]
        if not isinstance(is_differential, list):
            is_differential = [is_differential]

        if len(is_differential) == 1 and len(channels) != 1:
            is_differential_cpy = is_differential
            for i in range(len(channels) - 1):
                is_differential = is_differential + is_differential_cpy
        elif len(channels) != len(is_differential):
            raise ValueError(
                "ai_scan_init: Mode (is_differential parameter) "
                "vector should match selected AI channels"
            )

        if len(ai_range) == 2 and len(channels) != 1:
            range_cpy = ai_range
            for i in range(len(channels) - 1):
                ai_range = ai_range + range_cpy
        elif len(channels) != len(ai_range) / 2:
            raise ValueError(
                "ai_scan_init: Range vector should"
                " match selected AI channels!"
            )

        if duration < 0:
            duration = -1

        self._ai_scan_channels = channels
        channels_idx = ctypes.c_int8 * len(channels)
        channels_idx = channels_idx(*channels)
        channels_range = ctypes.c_double * (len(ai_range))
        channels_range = channels_range(*ai_range)
        diff = ctypes.c_int8 * len(is_differential)
        diff = diff(*is_differential)
        rate = ctypes.c_float(rate)

        res = cml.mlink_ai_scan_init(
            ctypes.pointer(self._linkfd),
            ctypes.byref(channels_idx),
            len(channels),
            channels_range,
            ctypes.byref(diff),
            ctypes.pointer(rate),
            duration,
        )

        self._raise_exception(res)

    @_connect_decorate
    def ai_scan(self, scan_count, timeout):
        """
        Description:
            Starts scanning and reads scan data
        Usage:
            ai_scan(scan_count, timeout)
            scan_count - number of scans to read
            timeout - amount of time in seconds to wait for samples (-1 - wait indefinitely)
        """
        if timeout > -1:
            timeout = timeout * 1000

        data_len = scan_count * len(self._ai_scan_channels)
        channels_val = ctypes.c_double * data_len
        channels_val = channels_val()

        res = cml.mlink_ai_scan(
            ctypes.pointer(self._linkfd),
            ctypes.byref(channels_val),
            scan_count,
            timeout,
        )

        self._raise_exception(res)

        val_list = []
        for channel in range(0, len(self._ai_scan_channels)):
            val_list.append(
                [
                    channels_val[i + channel]
                    for i in range(0, scan_count, len(self._ai_scan_channels))
                ]
            )

        if len(val_list) == 1:
            return val_list[0]
        else:
            return val_list

    @_connect_decorate
    def ao_write(self, channels, ao_range, data):
        """
        Description:
            Writes data to MicroDAQ analog outputs
        Usage:
            ao_write(channels, range, data)
            channels - analog output channels
            ao_range - analog output range matrix e.g.
                AO_10V      - [-10, 10]
                AO_10V_UNI  - [0, 10]
                AO_5V       - [-5, 5]
                AO_5V_UNI   - [0, 5]
                AO_2_5V     - [-2.5, 2.5]
                AORange.AO_5V_UNI - single-range argument applied for all used channels
                AORange.AO_5V + AORange.AO_10V  - multi-range argument for two channels

            data - data to be written
        """

        if not isinstance(channels, list):
            channels = [channels]
        if not isinstance(data, list):
            data = [data]
        if not isinstance(ao_range, list):
            ao_range = [ao_range]

        if len(channels) != len(data):
            raise ValueError(
                "ao_read: Data vector should match selected AI channels!"
            )

        if len(ao_range) == 2 and len(channels) != 1:
            range_cpy = ao_range
            for i in range(len(channels) - 1):
                ao_range = ao_range + range_cpy
        elif len(channels) != len(ao_range) / 2:
            raise ValueError(
                "ao_read: Range vector should match selected AI channels!"
            )

        channels_idx = ctypes.c_int8 * len(channels)
        channels_idx = channels_idx(*channels)
        channels_val = ctypes.c_double * len(channels)
        channels_val = channels_val(*data)
        channels_range = ctypes.c_double * (len(ao_range))
        channels_range = channels_range(*ao_range)

        res = cml.mlink_ao_write(
            ctypes.pointer(self._linkfd),
            ctypes.byref(channels_idx),
            len(channels),
            ctypes.byref(channels_range),
            1,
            ctypes.byref(channels_val),
        )

        self._raise_exception(res)

    @_connect_decorate
    def ao_scan_init(
        self, channels, initial_data, ao_range, is_stream_mode, rate, duration
    ):
        """
        Description:
            Initiates analog output scanning session
        Usage:
            ao_scan_init(channels, initial_data, ao_range, is_stream_mode, rate, duration)
            channels - analog output channels to write
            initial_data - output data
            ao_range - analog output range matrix e.g.
                AO_10V      - [-10, 10]
                AO_10V_UNI  - [0, 10]
                AO_5V       - [-5, 5]
                AO_5V_UNI   - [0, 5]
                AO_2_5V     - [-2.5, 2.5]
                AORange.AO_5V_UNI - single-range argument applied for all used channels
                AORange.AO_5V + AORange.AO_10V  - multi-range argument for two channels

            is_stream_mode - mode of operation (True - stream, False - periodic)
            rate - scans per second rate (scan frequency) [Hz]
            duration - analog output scan duration in seconds
        """

        if not isinstance(channels, list):
            channels = [channels]

        if not isinstance(initial_data, list):
            initial_data = [initial_data]

        ch_len = len(channels)
        self._ao_scan_ch = ch_len

        if len(ao_range) == 2 and len(channels) != 1:
            range_cpy = ao_range
            for i in range(len(channels) - 1):
                ao_range = ao_range + range_cpy
        elif len(channels) != len(ao_range) / 2:
            raise ValueError(
                "ao_read: Range vector should match selected AI channels!"
            )

        data_size = 0
        if isinstance(initial_data[0], list):
            data_size_ch = len(initial_data[0])
            if all(len(x) == data_size_ch for x in initial_data):
                pass
            else:
                raise ValueError("Wrong AO scan data size.")

            for ch_data in initial_data:
                data_size = data_size + len(ch_data)
            # make a flat list
            initial_data = sum(initial_data, [])
        else:
            if len(channels) > 1:
                raise ValueError("Wrong AO scan data size.")
            data_size = len(initial_data)

        ao_data = ctypes.c_float * data_size
        ao_data = ao_data(*initial_data)
        channels_idx = ctypes.c_uint8 * ch_len
        channels_idx = channels_idx(*channels)
        channels_range = ctypes.c_double * (len(ao_range))
        channels_range = channels_range(*ao_range)

        res = cml.mlink_ao_scan_init(
            ctypes.pointer(self._linkfd),
            ctypes.byref(channels_idx),
            len(channels),
            ctypes.byref(ao_data),
            ctypes.c_int(data_size),
            ctypes.byref(channels_range),
            ctypes.c_uint8(is_stream_mode),
            ctypes.c_float(rate),
            ctypes.c_float(duration),
        )

        self._raise_exception(res)

    @_connect_decorate
    def ao_scan_data(self, channels, data, opt=True):
        """
        TODO:
        Description:
           Queues data to be output
        Usage:
            ao_data_queue(channels, data, opt=True)
            channels - analog output channels to write
            data - data to be output
            opt - reset buffer index to 0 (True/False) - periodic mode
                  blocking/non-blocking   (True/False) - stream mode
        """

        if not isinstance(data, list):
            data = [data]

        if not isinstance(channels, list):
            channels = [channels]

        data_size = 0
        if isinstance(data[0], list):
            data_size_ch = len(data[0])
            if all(len(x) == data_size_ch for x in data):
                pass
            else:
                raise ValueError("Wrong AO scan data size.")

            for ch_data in data:
                data_size = data_size + len(ch_data)
            # make a flat list
            data = sum(data, [])
        else:
            if len(channels) > 1:
                raise ValueError("Wrong AO scan data size.")
            data_size = len(data)

        ch_len = len(channels)

        ao_data = ctypes.c_float * data_size
        ao_data = ao_data(*data)
        channels_idx = ctypes.c_uint8 * ch_len
        channels_idx = channels_idx(*channels)

        res = cml.mlink_ao_scan_data(
            ctypes.pointer(self._linkfd),
            ctypes.byref(channels_idx),
            ctypes.c_int(ch_len),
            ctypes.byref(ao_data),
            ctypes.c_int(data_size),
            ctypes.c_uint8(opt),
        )

        self._raise_exception(res)

    @_connect_decorate
    def ao_scan(self):
        """
        Description:
            Starts signal generation.
        Usage:
            ao_scan()
        """

        res = cml.mlink_ao_scan(ctypes.pointer(self._linkfd))
        self._raise_exception(res)

    @_connect_decorate
    def ao_scan_wait_until_done(self, timeout):
        """
        description:
            Waits until signal generation is done.
        usage:
            ao_scan_wait_until_done(timeout)
            timeout - amount of time in seconds to wait (-1 - wait indefinitely)
        """

        if timeout > -1:
            timeout = timeout * 1000

        res = cml.mlink_ao_scan_wait_until_done(
            ctypes.pointer(self._linkfd), timeout
        )
        self._raise_exception(res)

        if res == 0:
            return False
        elif res == 1:
            return True

    @_connect_decorate
    def ao_scan_is_done(self):
        """
        description:
            Checks if signal generation is completed.
        usage:
            ao_scan_is_done()
        """

        res = cml.mlink_ao_scan_is_done(ctypes.pointer(self._linkfd))
        self._raise_exception(res)

        if res == 0:
            return False
        elif res == 1:
            return True

    @_connect_decorate
    def ao_scan_stop(self):
        """
        Description:
            Stops signal generation.
        Usage:
            ao_scan_stop()
        """

        res = cml.mlink_ao_scan_stop(ctypes.pointer(self._linkfd))
        self._raise_exception(res)

    @_connect_decorate
    def ai_scan_stop(self):
        """
        Description:
            Stops AI scanning.
        Usage:
            ai_scan_stop()
        """

        res = cml.mlink_ai_scan_stop(ctypes.pointer(self._linkfd))
        self._raise_exception(res)

    @_connect_decorate
    def ai_scan_trigger_dio(self, dio, level):
        """
        Description:
            Sets a trigger for analog input scan session.
        Usage:
            ai_scan_trigger_dio(dio, level)
            dio - DIO channel number
            level - 0 or 1
        """

        res = cml.mlink_scan_trigger_dio(
            ctypes.pointer(self._linkfd), Triggers.AI_TRIGGER, dio, level
        )

        self._raise_exception(res)

    @_connect_decorate
    def ai_scan_trigger_clear(self):
        """
        Description:
            Clear triggers for analog input scan session.
        Usage:
            ai_scan_trigger_clear()
        """

        res = cml.mlink_scan_trigger_clear(
            ctypes.pointer(self._linkfd), Triggers.AI_TRIGGER
        )

        self._raise_exception(res)

    @_connect_decorate
    def ai_scan_trigger_dio_pattern(self, pattern):
        """
        Description:
            Sets a trigger for analog input scan session.
            Trigger occurs when defined digital pattern matches DIO1...8
            digital input channels state
        Usage:
            ai_scan_trigger_dio_pattern(pattern)
            pattern - 8 character string:
                1 - high state
                0 - low state
                x - undefined
                eg. "0xxx1x11"
        """

        res = cml.mlink_scan_trigger_dio_pattern(
            ctypes.pointer(self._linkfd),
            Triggers.AI_TRIGGER,
            pattern.encode("ascii"),
            len(pattern),
        )

        self._raise_exception(res)

    @_connect_decorate
    def ai_scan_trigger_encoder(self, module, position, condition):
        """
        Description:
            Sets a trigger for analog input scan session.
            Trigger occurs when value of selected encoder module
            is greater or lower then provided value
        Usage:
            ai_scan_trigger_encoder(module, position, condition)
            module - encoder module (1|2)
            position - encoder threshold value for trigger
            condition - 1: trigger when encoder value is greater than position parameter
                        0: trigger when encoder value is lower than position parameter
        """

        res = cml.mlink_scan_trigger_encoder(
            ctypes.pointer(self._linkfd),
            Triggers.AI_TRIGGER,
            module,
            position,
            condition,
        )

        self._raise_exception(res)

    @_connect_decorate
    def ai_scan_trigger_ext_start(self, source):
        """
        Description:
            Sets a trigger for analog input scan session based on external start event.
        Usage:
            ai_scan_trigger_ext_start(source)
            source - source of start event:
                     Triggers.AO_SCAN_START - start analog output scan session
                     Triggers.AI_SCAN_START - start analog input scan session
                     Triggers.DSP_START - start DSP program
        """

        res = cml.mlink_scan_trigger_external_start(
            ctypes.pointer(self._linkfd), Triggers.AI_TRIGGER, source
        )

        self._raise_exception(res)

    @_connect_decorate
    def ao_scan_trigger_dio(self, dio, level):
        """
        Description:
            Sets a trigger for analog output scan session.
        Usage:
            ao_scan_trigger_dio(dio, level)
            dio - DIO channel number
            level - 0 or 1
        """

        res = cml.mlink_scan_trigger_dio(
            ctypes.pointer(self._linkfd), Triggers.AO_TRIGGER, dio, level
        )

        self._raise_exception(res)

    @_connect_decorate
    def ao_scan_trigger_clear(self):
        """
        Description:
            Clear triggers for analog output scan session.
        Usage:
            ao_scan_trigger_clear()
        """

        res = cml.mlink_scan_trigger_clear(
            ctypes.pointer(self._linkfd), Triggers.AO_TRIGGER
        )

        self._raise_exception(res)

    @_connect_decorate
    def ao_scan_trigger_dio_pattern(self, pattern):
        """
        Description:
            Sets a trigger for analog output scan session.
            Trigger occurs when defined digital pattern matches DIO1...8
            digital input channels state
        Usage:
            ao_scan_trigger_dio_pattern(pattern)
            pattern - 8 character string:
                1 - high state
                0 - low state
                x - undefined
                eg. "0xxx1x11"
        """

        res = cml.mlink_scan_trigger_dio_pattern(
            ctypes.pointer(self._linkfd),
            Triggers.AO_TRIGGER,
            pattern.encode("ascii"),
            len(pattern),
        )

        self._raise_exception(res)

    @_connect_decorate
    def ao_scan_trigger_encoder(self, module, position, condition):
        """
        Description:
            Sets a trigger for analog output scan session.
            Trigger occurs when value of selected encoder module
            is greater or lower then provided value
        Usage:
            ao_scan_trigger_encoder(module, position, condition)
            module - encoder module (1|2)
            position - encoder threshold value for trigger
            condition - 1: trigger when encoder value is greater than position parameter
                        0: trigger when encoder value is lower than poisiotn parameter
        """
        res = cml.mlink_scan_trigger_encoder(
            ctypes.pointer(self._linkfd),
            Triggers.AO_TRIGGER,
            module,
            position,
            condition,
        )

        self._raise_exception(res)

    @_connect_decorate
    def ao_scan_trigger_ext_start(self, source):
        """
        Description:
            Sets a trigger for analog output scan session based on external start event.
        Usage:
            ao_scan_trigger_ext_start(source)
            source - source of start event:
                     Triggers.AO_SCAN_START - start analog output scan session
                     Triggers.AI_SCAN_START - start analog input scan session
                     Triggers.DSP_START - start DSP program
        """

        res = cml.mlink_scan_trigger_external_start(
            ctypes.pointer(self._linkfd), Triggers.AO_TRIGGER, source
        )

        self._raise_exception(res)
