import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="microchain",
    version="0.0.3",
    author="Damien Corpataux",
    author_email="d@mien.ch",
    description="Toolchain for micropython and microcontrollers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/damiencorpataux/microchain",
    packages=['microchain'],
    install_requires=[
        'esptool',
        'rshell',
        'adafruit-ampy',
        'pyserial',
        'sh',
        'requests',
        'click',
        'rich'],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)