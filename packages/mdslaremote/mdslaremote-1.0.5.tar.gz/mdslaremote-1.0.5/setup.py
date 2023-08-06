import setuptools
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE/"README.md").read_text()

setuptools.setup(
    name='mdslaremote',
    version='1.0.5',
    url='http://www.opalesystems.com',
    license='MIT',
    author='Opale Systems',
    description='Python API for Opale Systems MultiDSLA System',
    author_email='support@opalesystems.com',
    install_requires=[],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True
)
