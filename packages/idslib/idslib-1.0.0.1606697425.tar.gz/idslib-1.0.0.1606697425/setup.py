import setuptools
import time

v_time = str(int(time.time()))

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as r:
    requirements = r.read().split("\n")[0:-1]

setuptools.setup(
    name="idslib",
    version="1.0.0."+v_time,
    author="Daniel Doña",
    author_email="ddona@delicias.dia.fi.upm.es",
    license="Apache 2.0",
    description="IDS Python lib to interact with piveau-hub API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MGDS-development/idslib",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.6',
)
