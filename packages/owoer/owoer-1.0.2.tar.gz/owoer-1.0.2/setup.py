import setuptools

with open('./README.md', 'r', encoding="utf-8") as f:
    long_desc = f.read()


setuptools.setup(
    name="owoer",
    version="1.0.2",
    author="Zidaan Hayat",
    author_email="doczidaan@gmail.com",
    description="A little useless module to 'owoify' your text, aka turn it into a furro poetic masterpiece",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/Zidaan-Hayat/owoifyer.",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)

