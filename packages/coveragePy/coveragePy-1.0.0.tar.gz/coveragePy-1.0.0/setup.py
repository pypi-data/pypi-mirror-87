from setuptools import setup, find_packages


setup(
    name='coveragePy',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        "console_scripts": ['main = pythonDemoFlash.main:main']
    },
    install_requires=[
        "flask==1.0.2",
        "coverage==4.5.3",
        "requests==2.25.0"
    ],
    url='https://github.com/chexiedaping/coveragePy.git',
    license='GNU General Public License v3.0',
    author='yapong.jia',
    author_email='yapong.jia@huifu.com',
    description='measure code coverage of Python programs '
)