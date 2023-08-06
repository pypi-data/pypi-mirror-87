from setuptools import setup, find_packages

version = 0.25


def get_requirements():
    with open("requirements.txt") as fp:
        return fp.read()


setup(
    name="blackopt",
    packages=find_packages("blackopt"),
    package_dir={"": "blackopt"},
    version=version,
    description="black box optimization",
    author="Ilya Kamenshchikov",
    keywords=["optimization"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    license="MIT",
    long_description="In a far, far away galaxy...",
    install_requires=get_requirements(),
    python_requires=">=3.6",
    # url="https://github.com/ikamensh/blackopt",
)
