import setuptools

setuptools.setup(
    name="grapheno", # Replace with your own username
    version="0.0.4",
    license="MIT",
    author="Erik Burlingame",
    author_email="erik.burlingame@gmail.com",
    description="GPU-accelerated PhenoGraph for single-cell phenotyping",
    url="https://gitlab.com/eburling/grapheno",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)