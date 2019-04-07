from setuptools import setup

setup(
    name="helloworld",
    version='1.0',
    py_modules=['hello'],
    install_requires=[
        'Click',
    ],
    entry_points='''
    [console_scripts]
    hello=bhavCopyDownloader:main
    ''',
)