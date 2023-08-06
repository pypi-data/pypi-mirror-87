from setuptools import setup

setup(
    name='pytest_sanity',
    packages=['pytest_sanity'],
    entry_points={'pytest11': ['hailo_sanity=pytest_sanity.plugin']},
    version='0.0.1',
    long_description=open('readme.md').read()
)

