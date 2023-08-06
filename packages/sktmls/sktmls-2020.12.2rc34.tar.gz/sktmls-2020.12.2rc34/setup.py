import setuptools
import os

SKTMLS_VERSION = os.getenv("SKTMLS_VERSION")
if not SKTMLS_VERSION:
    raise TypeError("NO SKTMLS_VERSION")


def load_long_description():
    with open("README.md", "r") as f:
        long_description = f.read()
    return long_description


setuptools.setup(
    name="sktmls",
    version=SKTMLS_VERSION,
    author="SKTMLS",
    author_email="mls@sktai.io",
    description="MLS SDK",
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/sktaiflow/mls-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "catboost<1.0.0",
        "joblib",
        "lightgbm>=2.3.1,<2.4.0",
        "numpy",
        "pandas>=1.1.1,<1.2.0",
        "pytz",
        "requests",
        "scikit-learn>=0.23.2,<0.24",
        "scipy>=1.4.1,<1.5.0",
        "xgboost>=1.2.1,<1.3",
        "python-dateutil",
    ],
)
