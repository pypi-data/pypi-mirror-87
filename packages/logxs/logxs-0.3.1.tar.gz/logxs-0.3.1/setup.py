import setuptools
import os

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'rich'
]

about = {}
with open(os.path.join(here, 'logxs', '__version__.py'), 'r') as f:
    exec(f.read(), about)

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=about['__url__'],
    packages=['logxs'],
    package_dir={'logxs':'logxs'},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    python_requires='>=3.5',
    install_requires=requires,
    license=about['__license__'],
    scripts=[]

)