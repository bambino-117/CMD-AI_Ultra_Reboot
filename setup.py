#!/usr/bin/env python3
"""
Setup script pour CMD-AI Ultra Reboot
"""

from setuptools import setup, find_packages
import os

# Lire le README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Lire les requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cmd-ai-ultra-reboot",
    version="2.0.0",
    author="CMD-AI Team",
    author_email="contact@cmd-ai.dev",
    description="Application de chat/terminal IA modulaire et portable",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bambino-117/CMD-AI_Ultra_Reboot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Shells",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
        "full": [
            "netifaces>=0.11.0",
            "py-cpuinfo>=8.0.0",
            "geopy>=2.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cmd-ai=main:main",
            "cmdai=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.md", "*.txt", "*.ico", "*.png"],
        "ressources": ["*"],
        "extensions": ["*.py"],
        "language_models": ["*.py"],
    },
    zip_safe=False,
    keywords="ai chat terminal extensions marketplace",
    project_urls={
        "Bug Reports": "https://github.com/bambino-117/CMD-AI_Ultra_Reboot/issues",
        "Source": "https://github.com/bambino-117/CMD-AI_Ultra_Reboot",
        "Documentation": "https://github.com/bambino-117/CMD-AI_Ultra_Reboot/wiki",
    },
)