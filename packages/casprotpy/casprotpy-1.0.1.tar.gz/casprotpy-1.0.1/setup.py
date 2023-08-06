import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="casprotpy",
    version="1.0.1",
    author="Fred William",
    author_email="fred.william.prates@gmail.com",
    description="Python project for generate CAS Protocol TGTs and STs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://code.locaweb.com.br/fred.silva/casprotpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
