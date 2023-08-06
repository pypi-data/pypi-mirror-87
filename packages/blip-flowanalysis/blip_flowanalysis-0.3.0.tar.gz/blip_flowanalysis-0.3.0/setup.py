from setuptools import find_packages, setup
import blip_flowanalysis as bfs

long_description = open("README.md").read()
short_description = "A solution for chatbot constructors to identify problems in flow structure."
install_requires = [
    req
    for req in [
        line.split("#", 1)[0].strip()
        for line in open("requirements.txt", "r", encoding="utf-8")
    ]
    if req and not req.startswith("--")
]

classifiers = [
    "Programming Language :: Python :: 3.7",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License"
]

license= "MIT License"

setup(
    name="blip_flowanalysis",
    version=bfs.__version__,
    author=bfs.__author__,
    description=short_description,
    author_email="anaytics.dar@take.net",
    maintainer="daresearch",
    maintainer_email="anaytics.dar@take.net",
    keywords=["chatbot", "flow", "analysis"],
    license=license,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    install_requires=install_requires,
    classifiers=classifiers
)
