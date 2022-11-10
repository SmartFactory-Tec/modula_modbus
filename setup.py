from setuptools import setup

setup(
    name='modula_modbus',
    version='0.1.0',
    packages=['modula_modbus'],
    entry_points={
        'console_scripts': ['modula-modbus=modula_modbus.main:main']
    },
    install_requires=["certifi==2022.9.24; python_version >= '3.6'",
                      "charset-normalizer==2.1.1; python_full_version >= '3.6.0'", "idna==3.4; python_version >= '3.5'",
                      'pymodbustcp==0.2.0', 'requests==2.28.1', 'toml==0.10.2',
                      "urllib3==1.26.12; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5' and python_version < '4'"],
)
