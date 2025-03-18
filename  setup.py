#!/usr/bin/env python3
"""
Setup script for Telegram Always Online
"""

from setuptools import setup, find_packages

setup(
    name="telegram-always-online",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Telethon>=1.28.5",
        "python-dotenv>=1.0.0",
    ],
    scripts=[
        "scripts/telegram-online",
    ],
    author="Your Name",  # Replace with your name
    author_email="your.email@example.com",  # Replace with your email
    description="A tool to keep your Telegram account online 24/7",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/telegram-always-online",  # Replace with your GitHub repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)