import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="json2pytocol",
    version="0.0.4",
    author="Gabriel Piacenti",
    author_email="piacenti10@gmail.com",
    description="Generate Python Protocol Classes From Json",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    url='https://github.com/piacenti/json2pytocol',
    install_requires=[
        "dotmap"
    ],
    test_require=["pytest"],
    entry_points={
        'console_scripts': [
            'json2pytocol = json2pytocol.json_to_python_protocol:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
