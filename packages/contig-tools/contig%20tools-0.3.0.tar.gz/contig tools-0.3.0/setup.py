import setuptools

def readme():
    with open('README.md') as f:
        return f.read()

setuptools.setup(
    name='contig tools',
    version='0.3.0',
    description='Utility package to parse multi fasta files resulting from de novo assembly',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author='Anthony Underwood',
    author_email='au3@sanger.ac.uk',
    license='MIT',
    packages=setuptools.find_packages(),
    scripts=['contig_tools/scripts/contig-tools'],
    install_requires=['biopython', 'colorlog', 'pyyaml'],
    python_requires='>=3.7',
    test_suite='nose.collector',
    tests_require=['nose', 'coverage'],
    include_package_data=True,
    classifiers=[ 
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Science/Research', 
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)