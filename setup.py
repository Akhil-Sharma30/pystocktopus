from setuptools import setup

setup(
    name="pystocktopus",
    version="0.1.4",
    author="Akhil Sharma",
    author_email="akhilsharma.off@gmail.com",
    description=(
        "Help you maintain your stock dashboard, predict future stock trends based "
        "on past data, and analyze news sentiment to assess stock volatility."
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Akhil-Sharma30/pystocktopus",
    project_urls={
        "Documentation": "https://pystocktopus.readthedocs.io/en/latest/",
        "Bug Tracker": "https://github.com/Akhil-Sharma30/pystocktopus/issues",
        "Discussions": "https://github.com/Akhil-Sharma30/pystocktopus/discussions",
        "Changelog": "https://github.com/Akhil-Sharma30/pystocktopus/releases",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    install_requires=[
        "polygon-api-client",
        "scikit-learn",
        "pmdarima",
        "urllib3",
        "typing",
        "matplotlib",
        "tensorflow",
        "transformers",
        "pandas",
        "plotly",
        "mplfinance",
        "newsapi-python",
    ],
    extras_require={
        "test": ["pytest", "pytest-cov"],
        "dev": ["pytest", "pytest-cov"],
        "docs": [
            "myst_parser",
            "sphinx_copybutton",
            "sphinx_autodoc_typehints",
            "furo",
            "mkdocs-material",
        ],
    },
    packages=["pystocktopus"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "pystocktopus=pystocktopus.GUI:main",
        ],
    },
)
