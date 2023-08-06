import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setup_args = dict(
    name="ansiblerunnerapi",
    version="0.0.1",
    author="Maliao",
    author_email="maliaotw@gmail.com",
    description="Ansible Runner API package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Maliaotw/ansiblerunner.git",
    package_dir={'ansiblerunner': 'ansiblerunner'},
    packages=['ansiblerunner'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

install_requires = [
    'ansible==2.8.8',
]

dependency_links=[
]

if __name__ == '__main__':
    setuptools.setup(**setup_args, install_requires=install_requires)
