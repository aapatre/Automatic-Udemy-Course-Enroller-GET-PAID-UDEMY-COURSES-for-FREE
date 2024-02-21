"""Setup."""
import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="udemy-enroller",
    version="4.1.3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="aapatre",
    author_email="udemyenroller@gmail.com",
    maintainer="fakeid cullzie",
    url="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="udemy, education, enroll",
    packages=find_packages(
        exclude=["*tests*"],
    ),
    python_requires=">=3.8, <4",
    install_requires=[
        "aiohttp[speedups]==3.8.4",
        "beautifulsoup4==4.11.1",
        "ruamel.yaml==0.17.32",
        "requests==2.31.0",
        "cloudscraper==1.2.71",
        "webdriver-manager==3.8.6",
        "selenium==4.10.0",
        "price-parser==0.3.4",
    ],
    setup_requires=["pytest-runner"],
    extras_require={
        "dev": ["black", "isort"],
        "test": ["pytest", "pytest-cov"],
    },
    entry_points={
        "console_scripts": [
            "udemy_enroller=udemy_enroller.cli:main",
        ],
    },
)
