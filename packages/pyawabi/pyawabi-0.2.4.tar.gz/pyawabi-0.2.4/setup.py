import sys

from setuptools import setup

try:
    from setuptools_rust import RustExtension
except ImportError:
    import subprocess

    errno = subprocess.call([sys.executable, "-m", "pip", "install", "setuptools-rust"])
    if errno:
        print("Please install setuptools-rust package")
        raise SystemExit(errno)
    else:
        from setuptools_rust import RustExtension

setup_requires = ["setuptools-rust>=0.10.1", "wheel"]
install_requires = []

setup(
    name="pyawabi",
    version="0.2.4",
    description='A morphological analyzer using mecab dictionary.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url='http://github.com/nakagami/pyawabi/',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Rust",
        "Operating System :: POSIX",
    ],
    keywords=['MeCab'],
    license='MIT',
    author='Hajime Nakagami',
    author_email='nakagami@gmail.com',
    packages=["pyawabi"],
    scripts=['bin/pyawabi'],
    rust_extensions=[RustExtension("pyawabi.awabi")],
    setup_requires=setup_requires,
    zip_safe=False,
)
