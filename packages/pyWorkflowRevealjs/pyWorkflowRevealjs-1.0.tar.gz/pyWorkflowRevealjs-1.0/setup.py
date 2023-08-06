import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyWorkflowRevealjs", 
    version="1.0",
    author="20centCroak",
    author_email="",
    description="revealjs based presentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/20centcroak/pyWorkflowRevealjs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data = True,
    install_requires=[
        'pyBaseApp', 'pySimpleWorkflow', 'pyRevealjs', 'pandas'
    ],
)