import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bert-text-classifier",
    version="0.0.1a1",
    author="James Conley",
    author_email="jconley1+textclassifier@alumni.conncoll.edu",
    description="Train modern text classification models in just a few lines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JamesDConley/TextClassifier",
    packages=setuptools.find_packages(),
    install_requires=['matplotlib', 'pandas', 'torch', 'torchtext', 'transformers', 'scikit-learn', 'seaborn'],
    classifiers=[
        "Programming Language :: Python :: 3",
        #"License :: Be Nice",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
