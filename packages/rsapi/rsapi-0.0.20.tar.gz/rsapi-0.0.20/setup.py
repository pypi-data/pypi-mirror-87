import setuptools

with open("requirements.txt") as fp:
    requirements = fp.readlines()

setuptools.setup(
    name="rsapi",
    version="0.0.20",
    author="ostracker.xyz",
    author_email="admin@ostracker.xyz",
    description="Python library for accessing Runescape APIs",
    long_description_content_type="text/markdown",
    url="https://github.com/ostracker-xyz/pyrsapi",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    python_requires='>=3.6',
)
