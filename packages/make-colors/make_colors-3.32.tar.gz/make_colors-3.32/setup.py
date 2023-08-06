import io
import re
from setuptools import setup

import os
import shutil
try:
    os.remove(os.path.join('make_colors', '__version__.py'))
except:
    pass
shutil.copy2('__version__.py', 'make_colors')

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

# with io.open("__version__.py", "rt", encoding="utf8") as f:
    # version = re.search(r"version = \'(.*?)\'", f.read()).group(1)
import __version__
version = __version__.version

setup(
    name="make_colors",
    version=version,
    url="https://github.com/licface/make_colors",
    project_urls={
        "Documentation": "https://github.com/licface/make_colors",
        "Code": "https://github.com/licface/make_colors",
        "Issue tracker": "https://github.com/licface/make_colors/issues",
    },
    license="BSD",
    author="Hadi Cahyadi LD",
    author_email="cumulus13@gmail.com",
    maintainer="cumulus13 Team",
    maintainer_email="cumulus13@gmail.com",
    description="Make command line text colored",
    long_description=readme,
    long_description_content_type="text/markdown", 
    packages=["make_colors"],
    data_files=['__version__.py', 'README.rst', 'LICENSE.rst'],
    include_package_data=True,
    python_requires=">=2.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
