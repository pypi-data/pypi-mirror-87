from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name="manny",
    version="0.1.0",
    author="q0w",
    license="MIT",
    description="Django scaffold like in Ruby on Rails",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/q0w/manny/",
    packages=[
        "scaffold",
        "scaffold.kit",
        "scaffold.management",
        "scaffold.management.commands",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=["Django>=1.11", "black", "astor"],
    zip_safe=False,
    keywords="Django scaffold",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
