import setuptools

setuptools.setup(
    name="forza",
    version="0.0.1",
    author="Hammad Saeed",
    author_email="hammad@supportvectors.com",
    description="forza",
    long_description="""
FORZA
    """,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.9',
    install_requires=[
"art",
"libhammadpy-text",
"prompt_toolkit",
"wcwidth",
    ],
    extras_require={
        'ml' : [
            'suzuka',
        ]
    }
)