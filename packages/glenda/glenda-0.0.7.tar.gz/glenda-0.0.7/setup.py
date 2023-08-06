import setuptools
from glenda import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="glenda", # Replace with your own username
    version=__version__,
    author="Dmitry Mukovkin",
    author_email="mukovkin@yandex.ru",
    description="Some tools for glenda",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pudo/normality",
    install_requires=[
        "confluent-kafka==0.9.4"
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)