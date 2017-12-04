from setuptools import setup, find_packages

setup(
    name='yeelight-cinema',
    version='0.14',
    packages=find_packages(),
    long_description="This script can be used with yeelight color bulb. "
                     "Script detects color of scene and changes bulb color",


    scripts=['yeelight-cinema\yeelight-cinema.py'],

    install_requires=[
        'pillow',
        'pyscreenshot',
        'yeelight',
    ]
)
