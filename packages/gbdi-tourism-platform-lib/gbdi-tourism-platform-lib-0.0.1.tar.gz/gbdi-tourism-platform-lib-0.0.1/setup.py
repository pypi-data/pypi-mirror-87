from setuptools import setup, find_packages
import os

requirements = [
        "bson==0.5.10",
        "pymongo==3.11.1",
        "python-dateutil==2.8.1",
        "six==1.15.0"
        ]

extras = {
    "place_search":[
        "certifi==2020.11.8",
        "chardet==3.0.4",
        "click==7.1.2",
        "idna==2.10",
        "joblib==0.17.0",
        "numpy==1.19.4",
        "pandas==1.1.4",
        "pythainlp==2.2.5",
        "python-crfsuite==0.9.7",
        "python-dateutil==2.8.1",
        "pytz==2020.4",
        "regex==2020.11.13",
        "requests==2.25.0",
        "scikit-learn==0.23.2",
        "scipy==1.5.4",
        "sklearn==0.0",
        "threadpoolctl==2.1.0",
        "tinydb==4.3.0",
        "tqdm==4.54.0",
        "urllib3==1.26.2"
    ],
    "recommender":[],
    "full":[
        "certifi==2020.11.8",
        "chardet==3.0.4",
        "click==7.1.2",
        "idna==2.10",
        "joblib==0.17.0",
        "numpy==1.19.4",
        "pandas==1.1.4",
        "pythainlp==2.2.5",
        "python-crfsuite==0.9.7",
        "python-dateutil==2.8.1",
        "pytz==2020.4",
        "regex==2020.11.13",
        "requests==2.25.0",
        "scikit-learn==0.23.2",
        "scipy==1.5.4",
        "sklearn==0.0",
        "threadpoolctl==2.1.0",
        "tinydb==4.3.0",
        "tqdm==4.54.0",
        "urllib3==1.26.2"
    ]
}



setup(
    name="gbdi-tourism-platform-lib", # Replace with your own username
    version="0.0.1",
    author="Nanont Noparat, Chainarong Tumapha",
    author_email="nanont.no@depa.or.th, chainarong.tu@depa.or.th",
    description="private python packages for tourism-platform",
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=requirements,
    extras_require=extras
)