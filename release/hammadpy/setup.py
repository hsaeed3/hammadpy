import setuptools

setuptools.setup(
    name="hammadpy",
    version="3.10.1",
    author="Hammad Saeed",
    author_email="hammad@supportvectors.com",
    description="Hammad's Accelarated Micro Modules for Application Development (Hammad's Python Library)",
    long_description="""
Hammad's Accelarated Micro Modules for Application Development (Hammad's Python Library)
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
    ]
)