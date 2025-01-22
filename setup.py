from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tamga",
    version="0.1.8",
    author="Doğukan Ürker",
    author_email="dogukanurker@icloud.com",
    description="A modern, async-capable logging utility with multiple output formats and colorful console output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dogukanurker/tamga",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Logging",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "motor<3.6",
        "pymongo<4.9",
        "requests>=2.31.0"
    ],
    keywords="logging, async, mongodb, colorful, console, file, json, sql, email",
)
