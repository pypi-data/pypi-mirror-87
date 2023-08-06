from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = []
    for line in f.readlines():
        line = line.strip()
        if line:
            install_requires.append(line)

setup(
    name='dida',
    version='0.0.2',
    author="Lee",
    author_email="294622946@qq.com",
    url='https://github.com/Dog-Egg/dida',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['dida=dida.cmdline:main']
    }
)
