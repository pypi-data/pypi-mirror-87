from setuptools import setup, find_packages

VERSION = "0.1.6"
DESCRIPTION = "A minimal Automatic Machine Learning (AutoML) solution for tabular datasets based on PyTorch"
with open("README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="carefree-learn",
    version=VERSION,
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        "mypy",
        "black",
        "onnx",
        "onnxruntime",
        "optuna",
        "plotly",
        "carefree-ml>=0.1.0",
        "carefree-data>=0.2.1",
        "carefree-toolkit>=0.2.1",
        "dill",
        "future",
        "psutil",
        "tb-nightly",
        "cython>=0.29.12",
        "numpy>=1.16.2",
        "scipy>=1.2.1",
        "scikit-learn>=0.23.1",
        "matplotlib>=3.0.3",
    ],
    author="carefree0910",
    author_email="syameimaru_kurumi@pku.edu.cn",
    url="https://github.com/carefree0910/carefree-learn",
    download_url=f"https://github.com/carefree0910/carefree-learn/archive/v{VERSION}.tar.gz",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    keywords="python automl machine-learning solution PyTorch",
)
