import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="checkit",
    version="0.1.0",
    author="Nyggus & Ke Boan",
    author_email="nyggus@gmail.com",
    license='MIT',
    description="A tool for simple functionalized assertions in Python",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/nyggus/checkit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
)
