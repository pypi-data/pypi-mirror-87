from setuptools import setup, find_packages

minimal_requirements = [
    "Flask==1.1.2",
    "Click==7.1.2",
    "pyyaml==5.3.1",
    "flask-babel==2.0.0",
    "adafruit-circuitpython-dht==3.5.1",
    "rpi.gpio==0.7.0"
]


def get_long_description():
    """
    Return the README.
    """
    return open("README.md", "r", encoding="utf8").read()


setup(
    description="Charcuterie dashboard and controller for the Raspberry PI",
    license="MIT",
    name="raspcuterie",
    version="0.1.26",
    py_modules=["raspcuterie"],
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/foarsitter/raspcuterie",
    include_package_data=True,
    entry_points={
        "console_scripts": ["raspcuterie=raspcuterie.cli:cli"],
    },
    install_requires=minimal_requirements,
)
