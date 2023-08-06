import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webrobot",  # Replace with your own username
    version="1.5.0",
    author="Deity Micro",
    author_email="deitimicro@gmail.com",
    description="This is a Selenium based Web automation wheel that is more user-friendly than Selenium!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deitimicro/wheels",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = ["selenium"],
)
