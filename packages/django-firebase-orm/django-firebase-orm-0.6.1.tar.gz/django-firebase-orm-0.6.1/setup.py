from setuptools import setup, find_packages

import firebase_orm

setup(
    name="django-firebase-orm",
    version=firebase_orm.__version__,
    description="NoSQL object model database for django ORM integration",
    author="Tralah M Brian",
    author_email="musyoki.brian@tralahtek.com",
    url="https://github.com/TralahM/firebase_orm",
    packages=find_packages(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "firebase-admin==2.13.0",
        "grpcio>=1.9.1",
        "django",
    ],
    test_suite="tests",
    license="MIT",
)
