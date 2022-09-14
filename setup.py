from setuptools import setup, find_packages

setup(
    name='starpy',
    version="0.0.001",
    extras_require=dict(tests=['pytest']),
    packages=find_packages(where='starpy'),
    package_dir={"": "starpy"},
)
