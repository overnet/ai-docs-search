from setuptools import setup, find_packages

setup(
    name="ai-docs-search",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "nltk>=3.8.1",
        "sentence-transformers>=2.2.2",
        "PyPDF2>=3.0.1",
        "tqdm>=4.65.0",
    ],
    python_requires=">=3.8",
    author="Your Name",
    description="An AI-powered document search application",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
) 