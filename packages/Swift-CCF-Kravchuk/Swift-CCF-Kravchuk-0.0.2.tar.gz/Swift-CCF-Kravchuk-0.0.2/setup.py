import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Swift-CCF-Kravchuk",
    version="0.0.2",
    author="Kravchuk Pavlo",
    author_email="pashanoy@gmail.com",
    description="A swift code convention fixer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hybridlo/Metaprog",
    packages=setuptools.find_packages(),
    entry_points={
            'console_scripts': [
                'k-swift-ccf = exec.main:main'
            ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
