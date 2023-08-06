import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vn100-inm-pt",
    version="0.0.rc3",
    author="Palcort Tech S.A.S.",
    author_email="info@palcort.com",
    description="VectorNav VN-100 INM interface server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/palcort-tech/internal-vn100",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
          'pyserial<=3.4',
      ],
)