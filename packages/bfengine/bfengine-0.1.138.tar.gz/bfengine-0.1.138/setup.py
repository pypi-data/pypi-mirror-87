import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="bfengine",
    version="0.1.138",
    author="JeremyXin",
    author_email="chengjiexin@emotibot.com",
    description="bf engine sdk for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={
        '': ['data/*']
    },
    install_requires=[
        "requests",
        "tqdm"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    encoding='utf-8'
)
