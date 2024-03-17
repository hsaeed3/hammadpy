import setuptools

setuptools.setup(
    name="suzuka",
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
'annoy',
'anthropic',
'ebooklib',
'instructor',
'pandas',
'pathlib',
'pdfminer.six',
'PyPDF2',
'sentence-transformers',
'spacy',
"Whoosh",
    ]
)