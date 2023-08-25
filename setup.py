from setuptools import find_packages, setup

setup(
    name="QtCommon",
    version="0.1.2",
    author="Fadiga Ibrahima",
    author_email="ibfadiga@gmail.com",
    description="A sample package",
    packages=find_packages(),
    py_modules=["QtCommon"],
    install_requires=[
        "peewee>=3.0.0",
        "PyQt5>=5.0.0",
        "requests>=2.0.0",
        "psutil>=5.9.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
