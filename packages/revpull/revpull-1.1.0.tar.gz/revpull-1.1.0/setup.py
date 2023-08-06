from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name="revpull",
    version="1.1.0",
    author="Mikalai Lisitsa",
    author_email="Mikalai.Lisitsa@ibm.com",
    description="revpull is a tool for pulling data from IBM eReview.",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords='ereview ibm',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        "docopt == 0.6.2",
        "requests == 2.22.0",
        "schema == 0.7.2",
    ],
    include_package_data=True,
    python_requires='>=3.6',
    scripts=['bin/revpull'],
)
