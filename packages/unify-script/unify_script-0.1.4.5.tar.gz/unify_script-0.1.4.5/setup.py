import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='unify_script',
    version='0.1.4.5',
    author='Lukas Kristianto | Yehezkiel',
    author_email='lukas.kristianto@tokopedia.com',
    description='Unify color script automation converter',
    packages=['unify_package'],
    install_requires=['numpy','webcolors','scipy', 'pathlib'],
    script=['unify_package/unify_script'],
    include_package_data=True,
    classifier=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)