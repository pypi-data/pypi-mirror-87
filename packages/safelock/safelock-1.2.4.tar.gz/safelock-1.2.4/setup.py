'''
    Set up for safelock

    Copyright 2018-2020 DeNova
    Last modified: 2020-12-01
'''

import os.path
import setuptools

# read long description
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="safelock",
    version="1.2.4",
    author="denova.com",
    author_email="support@denova.com",
    maintainer="denova.com",
    maintainer_email="support@denova.com",
    description="Safelock gives you simple systemwide multithread, multiprocess, multiprogram locks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="locks multiprocess multithread multiinstance",
    license="GNU General Public License v3 (GPLv3)",
    url="https://denova.com/open_source/safelock/",
    download_url="https://github.com/denova-com/safelock/",
    project_urls={
        "Documentation": "https://denova.com/open_source/safelock/",
        "Source Code": "https://github.com/denova-com/safelock/",
    },
    include_package_data=False,
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
         ],
    py_modules=["safelock"],
    scripts=['sbin/safelock'],
    entry_points={
    },
    data_files=[('systemd/user', ['safelock.service'])],
    setup_requires=['setuptools-markdown'],
    install_requires=['denova', 'safelog'],
    python_requires=">=3.5",
)
