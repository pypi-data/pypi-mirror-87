from setuptools import setup

setup(
    name="birdjson",
    version="0.23.0",
    author="Anthony Casagrande",
    author_email="birdapi@gmail.com",
    description="Generic json to object parser for python",
    license="MIT",
    keywords="json birdapi",
    url="https://pypi.python.org/pypi/birdjson",
    py_modules=['birdjson'],
    install_requires=[
        'inflection',
        'simplejson'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)
