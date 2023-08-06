# dxx


[![PyPI version](https://badge.fury.io/py/dxx.svg)](https://badge.fury.io/py/dxx)
![Build status](https://github.com/tetsuzawa/dxx-py/workflows/Build/badge.svg)
<a href="LICENSE"><img src="http://img.shields.io/badge/license-MIT-blue.svg?style=flat" alt="MIT License"></a>


## Introduction

dxx is a library for io and converting audio files with a .DXX extension.



## Features

- read/write audio files like `foo.DXX` as np.ndarray (dtype=np.float64)
- handle {.DSA, .DFA, .DDA, .DSB, .DFB, .DDB}
- include some useful CLI tools



## Installation

```bash
pip install dxx
```

## Example

```python
import dxx

data = dxx.read("audio.DSB")

# do some processing...

dxx.write("audio.DSB", data)
```

Note that an exception will be thrown if you try to read/write a file with an extension other than .DXX.

## Build and upload dxx (for developers)

```bash
pip install wheel twine

python setup.py sdist
python setup.py bdist_wheel
twine upload dist/dxx-<version>*
```

## License

[MIT](LICENSE) License

Copyright (c) 2020-present, Tetsu Takizawa and Contributors.