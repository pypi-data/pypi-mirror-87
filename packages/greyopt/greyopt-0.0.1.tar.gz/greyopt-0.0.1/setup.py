# بسم الله الرحمن الرحيم
#
# In the name of Allah, the Compassionate, the Merciful
#
# In jurisdictions that recognize copyright laws, this work is
# distributed under the following terms:
#
# Copyright A.H. 1442 Mohamad Omar Nachawati <mnachawa@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pathlib

from setuptools import setup

if (__name__ == "__main__"):

    setup(
        name="greyopt",
        version="0.0.1",
        description="GreyOpt is a software package for large-scale grey-box optimization.",
        long_description=(pathlib.Path(__file__).parent/"README.md").read_text(),
        long_description_content_type="text/markdown",
        url="https://greyopt.github.io",
        author="Mohamad Omar Nachawati",
        author_email="mnachawa@gmail.com",
        license="Apache License 2.0",
        classifiers=[
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Topic :: Scientific/Engineering :: Mathematics"
        ],
        package_dir={"": "src/python"},
        packages=["greyopt"],
        install_requires=[
            "casadi >= 3.5.5",
            "click >= 7.1.2",
            "crlibm >= 1.0.3",
            "joblib >= 0.17.0",
            "numpy >= 1.19.4",
            "pyinterval >= 1.2.0",
            "scikit-learn >= 0.23.2",
            "scipy >= 1.5.4",
            "sortedcontainers >= 2.3.0",
            "threadpoolctl >= 2.1.0"
        ],
        entry_points={
            "console_scripts": [
                "greyopt=greyopt.__main__:main",
            ]
        }
    )
