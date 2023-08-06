import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
import git

repo = git.Repo('./')
tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
version = tags[-1] if len(tags) > 0 else "0.0.0-TEST"

setuptools.setup(
    name="EuroPy",
    version=str(version),
    author="Matthew Alvarez, Jenny Lam, Sundar Rajan, Blaine Rothrock",
    author_email="author@example.com",
    description="EuroPy testing framework for Machine Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EuroPy/EuroPyt",
    packages=setuptools.find_packages(),
    # entry_points={
    #     "pytest11": [
    #         "europy = europy.pytest_europy"
    #     ]
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Framework :: Pytest"
    ],
    python_requires='>=3.6',
)
