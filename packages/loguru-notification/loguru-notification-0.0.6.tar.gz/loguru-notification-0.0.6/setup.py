import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loguru-notification",
    version="0.0.6",
    author="RoyXing",
    author_email="x254724521@hotmail.com",
    description="Project logging printout",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/supplayer/loguru-notification",
    packages=setuptools.find_packages(exclude=('tests', 'requirements.txt')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        'amqp',
        'attrs',
        'billiard',
        'celery',
        'certifi',
        'chardet',
        'click',
        'click-didyoumean',
        'click-repl',
        'CMRESHandler2',
        'elasticsearch',
        'idna',
        'jsonschema',
        'kombu',
        'loguru',
        'notifiers',
        'prompt-toolkit',
        'pyrsistent',
        'pytz',
        'redis',
        'requests',
        'rfc3987',
        'sentry-sdk',
        'six',
        'tornado',
        'urllib3',
        'vine',
        'wcwidth'
        ]
)
