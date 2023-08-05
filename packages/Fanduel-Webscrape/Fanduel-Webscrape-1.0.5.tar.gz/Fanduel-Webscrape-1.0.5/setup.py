from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="Fanduel-Webscrape",
    version="1.0.5",
    description="A python script that will webscrape historical NBA Fanduel salary info.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/nathanhilton/NBAFanduel",
    author="Nathan Hilton",
    author_email="nathanhilton24@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Fanduel_Webscrape"],
    include_package_data=True,
    install_requires=[
        "requests",
        "beautifulsoup4>=4.0.0"
    ],
    entry_points={
        "console_scripts": [
            "Fanduel-Webscrape=Fanduel_Webscrape.MyApp:main",
        ]
    },
)