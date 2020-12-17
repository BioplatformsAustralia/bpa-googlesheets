from setuptools import setup, find_packages

setup(
    author="Matthew Mulholland <matt@redboxresearchdata.com.au>",
    author_email="info@redboxresearchdata.com.au",
    description="Download Googlesheet using Googlesheets API credentials",
    license="GPL3",
    keywords="",
    url="https://github.com/BioplatformsAustralia/bpa-googlesheets",
    name="bpagooglesheets",
    version="0.1.2",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    entry_points={
        "console_scripts": [
            "bpa-googlesheets=bpagooglesheets.cli:main",
        ]
    },
)
