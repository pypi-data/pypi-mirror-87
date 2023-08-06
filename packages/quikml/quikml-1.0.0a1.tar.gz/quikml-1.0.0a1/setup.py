from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="quikml",
    packages=find_packages(),
    version='1.0.0a1', ## alpha - pre-release
    description='a machine learning library that makes it easy to train, test, and assess ML classification models quikly.',
    long_description = long_description,
    author='Cisco AART Team',
    author_email = "brawise@cisco.com",
    long_description_content_type = "text/markdown",
    url="https://wwwin-gitlab-sjc.cisco.com/aart_ds/quikml-library",
    license='MIT',
    python_requires=">=3.6",
    install_requires=[
                        "scikit-learn==0.23.1",
                        "mlxtend",
                        "dask-ml",
                        "pandas",
                        "numpy",
                        "matplotlib",
                        "Keras",
                        "gensim",
                        "vecstack",
                        "xgboost",
                        "seaborn",
                        "tensorflow",
                        "imblearn"
                    ],
    extras_require = {'jupyter' : ["ipykernel"]},
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3'
    ]
)
