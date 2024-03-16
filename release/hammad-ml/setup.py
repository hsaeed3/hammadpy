import setuptools

setuptools.setup(
    name="hammadml",
    version="0.0.1",
    author="Hammad Saeed",
    author_email="hammad@supportvectors.com",
    description="ML",
    long_description="""
ML
    """,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.9',
    install_requires=[
"hammadpy>=3.0.1",
'pandas',
'pathlib',
"Whoosh",
    ]
)