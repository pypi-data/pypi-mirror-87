from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='fn_ont_expunge',
    version='0.2',
    packages=find_packages(),
    url='https://gitlab.com/horsebridge/fn_ont_expunge.git',
    license='MIT',
    author='Nitin Sidhu',
    author_email='nitin.sidhu23@gmail.com',
    description='FN ONT expunge',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    python_requires='~=3.7',
    install_requires=[
        'netmiko>=3.3.2',
        'sqlalchemy',
        'fibrenest-db-models',
        'hns-console-logging'
    ]
)

