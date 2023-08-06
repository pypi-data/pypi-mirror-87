from setuptools import setup, find_packages

VERSION = __import__('test_package').__version__

setup(
    name='swz-test-package',
    version=VERSION,
    author='swz',
    license='Apache LICENSE 2.0',
    # scripts=['test_package/bin/cmdt.py'],
    platforms='any',
    packages=find_packages(exclude=['tests*']),
    package_data={
        '': ['*']
    },
    install_requires='cryptography<=2.8',
    entry_points="""
    [console_scripts]
    cmdt=test_package.bin.cmdt:run
    """,
    python_requires=">=3.8"
    # entry_points={
    #     'console_scripts': [
    #         'cmdt=est_package.bin.cmdt:run',
    #     ],
    # }
)
