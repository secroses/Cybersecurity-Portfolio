from setuptools import setup, find_packages

setup(
    name="magic-sniffer",
    version="0.1.0",
    description="Inspector determinista de file-spoofing mediante análisis de magic numbers",
    author="secroses",
    author_email="",
    url="https://github.com/secroses/cybersecurity-portfolio",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "magic-sniffer=magic_sniffer.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Security",
    ],
)
