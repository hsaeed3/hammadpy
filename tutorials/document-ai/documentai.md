
### Quick-Use Document AI Module Guide

This guide provides a quick overview & tutorial, using hammadml to create a fast Document AI pipeline. This pipeline is not meant for
production/enterprise use, but rather for rapid development and prototyping.

This tutorial is best followed using the provided Jupyter notebook. Run ```git clone https://github.com/hsaeed3/hammadpy/``` for a quick start. 

```zsh
pip install hammadml>=0.1.6
```

```zsh
pip install hammadpy>=3.10
```

---

```python
from hammadml.data import Database, VectorDatabase
from hammadml.text import CrossEncoder
from hammadml.llms import Anthropic   # Or 'import Instructor' (OpenAI wrapped with instructor)
```
