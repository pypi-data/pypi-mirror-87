import setuptools
import gcp_simple_pipeline

setuptools.setup(
    name="gcp_simple_pipeline",
    version=gcp_simple_pipeline.__version__,
    author=gcp_simple_pipeline.__author__,
    author_email="alessandra.bilardi@gmail.com",
    description="A simple GCP Python pipeline",
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    url="https://gcp-simple-pipeline.readthedocs.io/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    project_urls={
        "Source":"https://github.com/bilardi/gcp-simple-pipeline",
        "Bug Reports":"https://github.com/bilardi/gcp-simple-pipeline/issues",
        "Funding":"https://donate.pypi.org",
    },
)
