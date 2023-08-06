from setuptools import setup

setup(
    name='error_analysis',
    version='0.1.2',
    packages=['error_analysis'],
    install_requires=[
        'numpy',
        'scipy',
        'sympy',
        'matplotlib',
        'varname'
    ],
    url='https://github.com/finnschwall/ErrorAnalysis',
    license='Apache License 2.0 ',
    author='Finn',
    author_email='finn1@web.de',
    description='Small library for easier propagation of uncertainty',
    long_description='In progress',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
