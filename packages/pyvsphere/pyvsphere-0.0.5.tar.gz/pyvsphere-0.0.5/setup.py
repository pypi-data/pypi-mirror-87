import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name="pyvsphere",
    version="0.0.5",
    author="Maliao",
    author_email="maliaotw@gmail.com",
    description="Vsphere SDK package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Maliaotw/pyvsphere.git",
    package_dir={'pyvsphere': 'pyvsphere'},
    packages=["pyvsphere"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

install_requires = [
    'ansible==2.8.8',
    'pyvmomi'
]

dependency_links=[
]

if __name__ == '__main__':
    setuptools.setup(**setup_args, install_requires=install_requires)
