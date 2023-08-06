from setuptools import setup, find_packages

setup(
    name='dida',
    version='0.0.1',
    author="Lee",
    author_email="294622946@qq.com",
    url='https://github.com/Dog-Egg/dida',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['tornado', 'apscheduler', 'marshmallow'],
    entry_points={
        'console_scripts': ['dida=dida.cmdline:main']
    }
)
