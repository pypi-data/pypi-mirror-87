import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mongo-system-log",
    version="0.0.9",
    author="Ronaldo Duarte",
    author_email="ronaldoduarte@globo.com",
    description="A log package that works with MongoDB.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ronaldodduarte/mongo_system_log",
    install_requires=["pymongo"],
    packages=["mongo_system_log"],
    license="GNU",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)