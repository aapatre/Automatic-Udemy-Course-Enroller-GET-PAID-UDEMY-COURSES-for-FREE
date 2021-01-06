import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

with open("requirements.txt") as f:
    install_reqs = f.read().splitlines()

setup(
    name="udemy-enroller",
    version="2.0.0",
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
    packages=find_packages(exclude=["pyproject.toml"]),
    python_requires=">=3.8, <4",
    install_requires=install_reqs,
    setup_requires=["pytest-runner"],
    extras_require={
        "dev": ["black", "isort"],
        "test": ["pytest", "pytest-cov"],
    },
    entry_points={
        "console_scripts": [
            "udemy_enroller=scripts.udemy_enroller:main",
        ],
    },
)
