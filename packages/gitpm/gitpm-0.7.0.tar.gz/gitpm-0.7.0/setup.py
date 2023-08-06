import setuptools

long_description = """
Git Project Manager
===================

|PyPI - Version| |Downloads| |Code style: black|

GitPM helps you **manage your projects** using Git's version management.

-  `Docs`_
-  `Source`_
-  `Contact`_

License
-------

`MIT License. Copyright 2020 Finn M Glas.`_

.. _Docs: https://gitpm.readthedocs.io/
.. _Source: https://github.com/finnmglas/GitPM
.. _Contact: https://contact.finnmglas.com
.. _MIT License. Copyright 2020 Finn M Glas.: https://choosealicense.com/licenses/mit/

.. |PyPI - Version| image:: https://img.shields.io/pypi/v/gitpm?color=000
   :target: https://pypi.org/project/gitpm/
.. |Downloads| image:: https://img.shields.io/badge/dynamic/json?style=flat&color=000&maxAge=10800&label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fgitpm
   :target: https://pepy.tech/project/gitpm
.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
"""

setuptools.setup(
    name="gitpm",
    version="0.7.0",
    description="Efficient code-base management based on git.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Software Development :: Version Control",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    keywords="git management repositories manager efficiency",
    url="http://github.com/finnmglas/gitPM",
    author="Finn M Glas",
    author_email="finn@finnmglas.com",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=[
        "cliprint",  # Managed by Finn - https://github.com/finnmglas/cliprint
    ],
    entry_points={
        "console_scripts": [
            "gitpm=gitpm.tools.gitpm:GitPM.main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
