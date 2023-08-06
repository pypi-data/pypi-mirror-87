from setuptools import setup, find_packages

setup(name='apyonics',
    version='0.3.6',
    author='Aionics',
    author_email='support@aionics.io',
    description='Client for interacting with Aionics services',
    url='https://github.com/aionics-io/apyonics',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.5'
)

