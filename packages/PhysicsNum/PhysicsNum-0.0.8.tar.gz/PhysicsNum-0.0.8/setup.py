from setuptools import setup, find_packages

with open("readme.md", 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name = "PhysicsNum",
    version = "0.0.8",
    author = "Andreas Evensen",
    author_email = "Andreas.evensen11@gmail.com",
    description = "Numerical methods provided to solve different methods in university studies",
    long_description = long_description,
    long_description_content_type='text/markdown',
    py_module = ["GaussianFit", "Linearreg"],
    include_package_data = True,
    packages = find_packages(),
    license = "MIT",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
)
