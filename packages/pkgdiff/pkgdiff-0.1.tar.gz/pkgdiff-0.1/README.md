# Compare FreeBSD pkg files by metadata

**pkgdiff** is a plugin for the FreeBSD package manager
[pkg](https://www.freebsd.org/cgi/man.cgi?pkg(7)) as well as a Python
extension for comparing package files by their metadata.

To that end it uses libpkg (distributed along with the **pkg**
commandline tools), to open and parse package files and either a basic
string compare or a line-by-line diff algorithm to complare the
metadata fields.

How to install
--------------

The Python extension is easily installed by running:

```bash
pip install pkgdiff
```

Basic usage
-----------

```python
import pkgdiff

if pkgdiff.compare('pkg-1.14.5.txz', 'pkg-1.14.6.txz', exclude=['version']):
    print('packages are equal (ignoring version)')
```
