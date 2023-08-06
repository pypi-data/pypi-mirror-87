import io
import re
from setuptools import setup

import os, sys
import shutil
try:
    os.remove(os.path.join('zippyshare_generator', '__version__.py'))
except:
    pass
shutil.copy2('__version__.py', 'zippyshare_generator')

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

# with io.open("__version__.py", "rt", encoding="utf8") as f:
    # version = re.search(r"version = \'(.*?)\'", f.read()).group(1)
import __version__
version = __version__.version

requirements = [
        'requests',
        'bs4',
        'argparse',
        'clipboard',
        'make_colors>=3.12',
        'configset',
        'configparser',
        'pywget',
        'pydebugger',
        'js2py',
        'parserheader'
    ]

if sys.platform == 'win32':
    requirements.append('idm')
    
setup(
    name="zippyshare_generator",
    version=version,
    url="https://bitbucket.org/licface/zippyshare_generator",
    project_urls={
        "Documentation": "https://bitbucket.org/licface/zippyshare_generator",
        "Code": "https://bitbucket.org/licface/zippyshare_generator",
    },
    license="BSD",
    author="Hadi Cahyadi LD",
    author_email="cumulus13@gmail.com",
    maintainer="cumulus13 Team",
    maintainer_email="cumulus13@gmail.com",
    description="Generator Zippyshare Links",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=["zippyshare_generator"],
    
    install_requires=requirements,
    entry_points = {
         "console_scripts": [
             "zippyshare_generator = zippyshare_generator.__main__:usage",
             "zippyshare = zippyshare_generator.__main__:usage",
         ]
    },
    data_files=['zippyshare_generator/__version__.py', 'README.rst', 'LICENSE.rst', 'zippyshare_generator/zippyshare.ini'],
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7"
    ],
)
