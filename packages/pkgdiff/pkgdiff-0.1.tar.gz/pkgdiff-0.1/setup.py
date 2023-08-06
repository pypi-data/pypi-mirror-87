from pathlib import Path
from setuptools import setup,Extension
from subprocess import check_output

def pkgconfig(*args):
    return check_output(('pkg-config',) + args, text=True).strip().split()

setup(
    name='pkgdiff',
    description='Compare FreeBSD pkg files by metadata.',
    long_description=(Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    version='0.1',
    author='Florian Wagner',
    author_email='florian@wagner-flo.net',
    url='https://github.com/wagnerflo/pkgdiff',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Programming Language :: C',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: System :: Systems Administration',
    ],
    license_files=['LICENSE'],
    python_requires='>=3.8',
    ext_modules=[
        Extension(
            'pkgdiff',
            sources=[
                'src/python-module.c',
                'src/pkgdiff.c',
                'ext/libmba-0.9.1/allocator.c',
                'ext/libmba-0.9.1/diff.c',
                'ext/libmba-0.9.1/msgno.c',
                'ext/libmba-0.9.1/suba.c',
                'ext/libmba-0.9.1/varray.c',
            ],
            include_dirs=[
                'ext/libmba-0.9.1',
            ],
            extra_compile_args=[
                *pkgconfig('--cflags', 'pkg'),
            ],
            extra_link_args=[
                *pkgconfig('--libs', 'pkg'),
            ],
        ),
    ],
)
