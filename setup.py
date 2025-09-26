"""
FileNest - Intelligent File Organizer
A simple, powerful file organization tool that automatically sorts files into categories.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "readme_docs.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else __doc__

setup(
    name="filenest",
    version="1.0.0",
    author="FileNest Team",
    author_email="support@filenest.dev",
    description="Intelligent file organizer with automatic categorization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/python-file-organize-utility",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/python-file-organize-utility/issues",
        "Documentation": "https://github.com/yourusername/python-file-organize-utility#readme",
        "Source": "https://github.com/yourusername/python-file-organize-utility",
    },
    
    packages=find_packages(),
    py_modules=["organizer", "config_setup", "log_viewer"],
    
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Archiving",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    
    python_requires=">=3.8",
    
    install_requires=[
        # Core functionality uses only standard library
        # Optional dependencies for enhanced features
    ],
    
    extras_require={
        "watch": ["watchdog>=3.0.0"],
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "all": ["watchdog>=3.0.0"],
    },
    
    entry_points={
        "console_scripts": [
            "organize=organizer:main",
            "filenest=organizer:main",
            "file-organize=organizer:main",
            "config-setup=config_setup:main",
            "log-viewer=log_viewer:main",
        ],
    },
    
    include_package_data=True,
    zip_safe=False,
    
    keywords=[
        "file", "organizer", "automation", "cli", "utility", 
        "sorting", "categorization", "filesystem", "cleanup"
    ],
    
    # Additional metadata
    license="MIT",
    platforms=["any"],
)