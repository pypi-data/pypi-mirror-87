import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snake-classic-PAULO-SNAKE-UFCG", # Replace with your own username
    version="0.0.1",
    author="Paulo Filipe ALves de Vasconcelos",
    author_email="paulo.vasconcelos@ccc.ufcg.edu.br",
    description="A small example package",
    long_description="very simple snake game recreation with pygame",
    long_description_content_type="text/markdown",
    url="https://github.com/Paulo-Filipe/snakepygame",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.6',
)