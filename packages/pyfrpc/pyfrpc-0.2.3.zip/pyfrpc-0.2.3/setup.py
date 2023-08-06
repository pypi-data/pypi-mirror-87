import os

from setuptools import setup


PYFRPC_NOEXT = bool(int(os.environ.get('PYFRPC_NOEXT', '0')))

setup_args = dict(
    name='pyfrpc',
    version='0.2.3',
    description='Python implementation of fastrpc protocol',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Vladimir Burian',
    license='MIT',
    url='https://gitlab.com/vladaburian/pyfrpc',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='frpc fastrpc',
    packages=['pyfrpc'],
    package_dir={'':'src'},
    package_data={'pyfrpc':['*.pyx']},
    install_requires=['requests', 'six'],
    extras_require={'nc': ['ipython']},
    entry_points={
        'console_scripts': [
            'pyfrpc = pyfrpc.netcat:main',
        ],
    },
)

if not PYFRPC_NOEXT:
    try:
        from Cython.Build import cythonize

        setup_args.update(dict(
            ext_modules=cythonize('src/pyfrpc/_coding_base_c.pyx'),
        ))

    except ImportError:
        print(
            "\n"
            "Error: cython module is missing. Do one of the following:\n"
            "  A) Install Cython and C toolchain to compile C extension\n"
            "     with fast decoder implementation.\n"
            "  B) Set env PYFRPC_NOEXT=1 to disable C extension and use\n"
            "     slower but pure python implementation.\n"
        )

        raise


if __name__ == "__main__":
    setup(**setup_args)
