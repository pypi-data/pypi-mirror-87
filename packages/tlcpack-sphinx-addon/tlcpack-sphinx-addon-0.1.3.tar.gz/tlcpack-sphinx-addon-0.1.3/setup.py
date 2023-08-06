# pylint: disable=invalid-name, exec-used
"""Setup TLCPack."""
from setuptools import setup, find_packages

__version__ = "0.1.3"


setup(
    name="tlcpack-sphinx-addon",
    version=__version__,
    license="Apache-2.0",
    description="TLCPack Sphinx addon",
    zip_safe=False,
    install_requires=[],
    packages=find_packages(),
    package_data={
        "tlcpack_sphinx_addon": [
            "_templates/*.html",
            "_static/css/*.css",
            "_static/img/*.svg",
            "_static/js/*.js",
        ]
    },
    url="https://github.com/tlc-pack/tlcpack-sphinx-addon",
    author="tlcpack",
    author_email="tianqi.tchen@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)
