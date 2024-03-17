
*The hammadml docAI pipeline is built off of incredibly well designed python packages*<br>
[Annoy - Approximate Nearest Neighbors in C++/Python](https://github.com/spotify/annoy)<br>
[Instructor - Structured Outputs for LLMs](https://github.com/jxnl/instructor)<br>
[Sentence-Transformers - Multilingual Sentence & Image Embeddings with BERT](https://github.com/UKPLab/sentence-transformers)<br>
[Whoosh - Pure-Python Full-Text Search Library](https://github.com/mchaput/whoosh)<br>

## hammadml *'One Notebook'* Document AI Tutorial

This guide provides a quick overview & tutorial, using hammadml to create a fast Document AI pipeline. This pipeline is not meant for production/enterprise use, but rather for rapid development and prototyping.

This tutorial is best followed using the provided Jupyter notebook. Run ```git clone https://github.com/hsaeed3/hammadpy/``` for a quick start. 

```zsh
pip install hammadml>=0.1.6 --upgrade
# The library will handle & install all required torch/transformer dependencies on its own.
```

---

### Getting Started

The entire pipeline can be created using one Jupyter Notebook; and the provided one in this directory should suffice. Once youve installed the library above, run the following code in your first cell block to import the necessary modules. **NOTE: The first run/cycle of this code block may take a second to complete, as the VectorDatabase and CrossEncoder require spaCy and Sentence-Transformer models.**

```python
from hammadml.data import Database, VectorDatabase
from hammadml.text import CrossEncoder
from hammadml.llms import Anthropic   # Or 'import Instructor' (OpenAI wrapped with instructor)
```
<br>

The provided ```tutorials/documentai``` folder contains 4 sample movie script we'll use in this tutorial. The next code block utilizes the parsing functionality built into the Database class, which will automatically read through a directory, pick up all documents (.txt,.pdf), and properly import them into a new/existing ```Whoosh``` database.
