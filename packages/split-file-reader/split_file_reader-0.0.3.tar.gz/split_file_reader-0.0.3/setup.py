import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="split_file_reader",
    version="0.0.3",
    author="Xavier Halloran",
    author_email="sfr@reivax.us",
    description="A package to read parted files on disk.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Reivax/split_file_reader",
    # packages=setuptools.find_packages(),
    packages=["split_file_reader"],
    entry_points={
        "console_scripts": [
            "split_file_reader = split_file_reader.__main__:main"
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: System :: Filesystems",
    ],
    python_requires='>=3.5',
    platforms=['any'],
    install_requires=[
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    project_urls={
        'Source': "https://gitlab.com/Reivax/split_file_reader",
    },
)
