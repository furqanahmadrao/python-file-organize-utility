"""
Setup script for File Organizer v2.0
Professional file organization utility
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
README_PATH = Path(__file__).parent / "README.md"
if README_PATH.exists():
    with open(README_PATH, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "Professional file organization utility with advanced features"

# Read requirements
REQUIREMENTS_PATH = Path(__file__).parent / "requirements.txt"
if REQUIREMENTS_PATH.exists():
    with open(REQUIREMENTS_PATH, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
else:
    requirements = []

setup(
    name="file-organizer-pro",
    version="2.0.0",
    author="Furqan Ahmad Rao",
    author_email="your.email@example.com",
    description="Professional file organization utility with advanced CLI features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/furqanahmadrao/python-file-organize-utility",
    project_urls={
        "Bug Reports": "https://github.com/furqanahmadrao/python-file-organize-utility/issues",
        "Source": "https://github.com/furqanahmadrao/python-file-organize-utility",
        "Documentation": "https://github.com/furqanahmadrao/python-file-organize-utility#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9", 
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "watch": [
            "watchdog>=3.0.0",
        ],
        "all": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0", 
            "black>=23.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "watchdog>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "file-organizer=file_organizer_cli:main",
            "organize-files=file_organizer_cli:main",
            "forg=file_organizer_cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "file_organizer": [
            "data/*.json",
            "templates/*.json",
        ],
    },
    keywords=[
        "file", "organizer", "organize", "files", "directory", "cleanup", 
        "automation", "cli", "utility", "management", "sorting"
    ],
    license="MIT",
    zip_safe=False,
)