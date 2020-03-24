"""Setuptools installation script."""

import setuptools

setuptools.setup(
    name="vta",
    author="brobeson",
    author_email="brobeson@users.noreply.github.com",
    description="A collection of tools for visual tracking research.",
    url="https://github.com/brobeson/vta",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: You may not use this, yet.",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": "vta = vta.vta:main"},
)
