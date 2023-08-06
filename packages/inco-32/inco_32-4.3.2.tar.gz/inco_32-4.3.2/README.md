# inco_32 Python Binding

This is a Python 2 and 3 binding for libinco_32 (inco_32.dll/libinco_32.so), the library used for INCO communication to [Indel](https://www.indel.ch/) industrial automation systems.

To use it, you need to have [Indel Tools](https://doc.indel.ch/doku.php?id=software:application:installation) installed, which provides the library.

## Usage

The Python API is for the most part a direct translation of the C API, with the exception that errors are reported using exceptions rather than return values, and output is provided as return values rather than through pointer arguments. Therefore, refer to the [C API documentation](https://doc.indel.ch/doxygen/libinco_32/index.html) for details.

#### Example

```python
import inco_32
target = 'MyTarget'
try:
    cpuname = inco_32.GetVariable(target, 'Target.Cpu', 256)
except inco_32.INCOError as e:
    if e.m_uError == inco_32.ER_INCO_VAR_NOT_FOUND:
        print('where?')
```

For more usage examples, see the tests in `tests/test_inco_32.py`.

## Installation

The binding is already installed in the Python installations included with Indel Tools (_Indel Tools Setup_ on Windows, package `python-inco32` on Linux). These installations are intended for internal use by Indel Tools.

For larger customer applications that require more packages to be installed, it is recommended that you use your own Python installation. For those, the package is available from PyPI:

```
pip install inco_32
```

To build from source, `pip install build` and use

```
rm -rf build src/inco_32.egg-info && python3 -m build .
```
