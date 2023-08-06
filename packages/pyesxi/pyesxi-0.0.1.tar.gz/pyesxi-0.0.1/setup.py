import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = ['pyesxi']

setup_args = dict(
    name="pyesxi",
    version="0.0.1",
    author="Maliao",
    author_email="maliaotw@gmail.com",
    description="DELL ESXI SDK package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Maliaotw/pyesxi.git",
    package_dir={'pyesxi': 'pyesxi'},
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

install_requires = [
    'ansible==2.8.8',
    'pysnmp>=4.4.1',
    'requests>=2.12.3',
    'PyYAML>=3.12',
    'future>=0.16.0',
    'pysnmp_mibs>=0'
]

dependency_links=[
        'https://github.com/Maliaotw/pyesxi/omsdk-1.2.445-py2.py3-none-any.whl',
]

if __name__ == '__main__':
    setuptools.setup(**setup_args, install_requires=install_requires)
