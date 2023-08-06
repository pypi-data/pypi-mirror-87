''' just for docstring sake '''
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="abgleich-pkg-wasix",  # Replace with your own username
    version="0.3.14",
    author="WasiX",
    author_email="wasix01@gmail.com",
    description="A small string comparison package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wasix01/abgleich-pkg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    test_suite='nose.collector',
    tests_require=['nose'],
    install_requires=['csvkit',
                      'fuzzywuzzy',
                      'numpy',
                      'p-tqdm',
                      'tqdm',
                      'pandas',
                      'psycopg2-binary',
                      'pylint',
                      'python-Levenshtein',
                      'SQLAlchemy',
                      'xlrd',
                      'psutil'],
    package_data={'abgleich_pkg': ['input/Abgleich_KUSY_Vorlage.xlsx', 'docker/docker-compose.yml', 'docker/do_csv_upload.sh'], },
)

print("Finished!")
