import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

extras_requirements = {
    "dev": ["pytest", "wheel", "black"],
}

setuptools.setup(
    name="easycheck",
    version="0.8.0",
    author="Nyggus, Ke Boan & Darsoo",
    author_email="nyggus@gmail.com",
    license="MIT",
    description="A tool for checking conditions in Python",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/nyggus/easycheck",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    extras_require=extras_requirements,
)
