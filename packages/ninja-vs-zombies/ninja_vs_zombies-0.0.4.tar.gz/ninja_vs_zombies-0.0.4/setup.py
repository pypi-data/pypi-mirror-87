import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ninja_vs_zombies",
    version="0.0.4",
    author="Pedro Adrian Pereira Martinez",
    author_email="pedro.martinez@ccc.ufcg.edu.br",
    license='MIT',
    description="Um projeto de jogo de plataforma em pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adrianmartinez-cg/ninjavszombies",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
