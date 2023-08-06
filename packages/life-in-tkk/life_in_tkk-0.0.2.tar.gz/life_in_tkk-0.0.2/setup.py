import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="life_in_tkk",
    version="0.0.2",
    author="mirasire",
    author_email="mes2dasuan@outlook.com",
    description="A library to help tkk(xujc)'s student feel relax on their daliy campus life",
    license="MIT License",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mirasire/Life-In-Tkk",
    packages=setuptools.find_packages(),
    install_requires=[
        'Pillow>=8.0.1',
        'selenium>=3.141.0',
        'requests>=2.22.0',
        'beautifulsoup4>=4.8.2',
        'pytesseract>=0.3.6',
        'tesseract>=0.1.3',
        'numpy>=1.17.4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
        "License :: OSI Approved :: MIT License",
    ],
)
