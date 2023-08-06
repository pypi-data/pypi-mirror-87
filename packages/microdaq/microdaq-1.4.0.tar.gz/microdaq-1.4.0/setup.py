# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2017-2020, www.microdaq.org

from setuptools import setup

setup(
    name="microdaq",
    version="1.4.0",
    packages=["microdaq"],
    package_data={
        "microdaq": [
            "x64/MLink64.dll",
            "x64/libmlink.dylib",
            "x64/libmlink.so",
            "x86/libmlink.so",
            "x86/MLink32.dll",
            "armel/libmlink.so",
        ]
    },
)
