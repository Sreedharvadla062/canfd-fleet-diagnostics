from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="canfd-fleet-diagnostics",
    version="1.0.0",
    author="Fleet Diagnostics Team",
    description="CAN-FD + UDS Vehicle Data Collector for Fleet Diagnostics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sreedharvadla062/canfd-fleet-diagnostics",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-can>=4.0.0",
        "python-uds>=1.3.0",
        "pyyaml>=6.0",
        "loguru>=0.7.0",
        "requests>=2.28.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
)
