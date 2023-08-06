import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="collect_framework",
    version="0.0.1",
    author="Woiyter",
    author_email="iseefire3009@gmail.com",
    description="Counter of unique chars",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.foxminded.com.ua/Woiyter/task_5",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
