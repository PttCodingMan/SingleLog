from setuptools import setup

setup(
    name='SingleLog',  # Required
    # https://packaging.python.org/en/latest/single_source_version.html
    version='2.0.10',

    description=open('README.md', encoding="utf-8").read(),
    description_content_type='text/markdown',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    url='https://github.com/PttCodingMan/SingleLog',
    author='CodingMan',  # Optional
    author_email='pttcodingman@gmail.com',
    # https://pypi.org/classifiers/
    classifiers=[  # Optional
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],

    keywords=['log', 'logger', 'library'],

    python_requires='>=3.8',
    packages=['SingleLog'],
    install_requires=['AutoStrEnum', 'colorama'],
)
