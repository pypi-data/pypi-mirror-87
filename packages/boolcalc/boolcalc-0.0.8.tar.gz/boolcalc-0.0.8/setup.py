from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='boolcalc',
    version='0.0.8',
    description='basic boolean calculator',
    long_description=open('README.txt').read(),
    url='',
    author='Otsuka Yuno',
    author_email='moreseus@outlook.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
)
