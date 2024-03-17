
### Quick-Use Document AI Module Guide

This guide provides a quick overview & tutorial, using hammadml to create a fast Document AI pipeline. This pipeline is not meant for production/enterprise use, but rather for rapid development and prototyping.

This tutorial is best followed using the provided Jupyter notebook. Run ```git clone https://github.com/hsaeed3/hammadpy/``` for a quick start. 

```zsh
pip install hammadml>=0.1.6
```

---

### Getting Started

The entire pipeline can be created using one Jupyter Notebook; and the provided one in this directory should suffice. Once youve installed the library above, run the following code in your first cell block to import the necessary modules. 
**NOTE: The first run/cycle of this code block may take a second to complete, as the VectorDatabase and CrossEncoder require spaCy and Sentence-Transformer models.

```python
from hammadml.data import Database, VectorDatabase
from hammadml.text import CrossEncoder
from hammadml.llms import Anthropic   # Or 'import Instructor' (OpenAI wrapped with instructor)
```
