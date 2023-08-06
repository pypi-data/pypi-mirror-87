import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="hopfenmatrix",
    version="0.1.9",
    author="Wolfgang Fischer, Niklas Pfister",
    author_email="kontakt@omikron.dev",
    description="A library to make matrix-nio easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hopfenspace/hopfenmatrix/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "matrix-nio[e2e]",
        "Pillow",
        "python-magic",
        "aiofiles",
        "mutagen",
    ]
)
