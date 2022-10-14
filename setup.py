from setuptools import setup, find_packages

setup(
    name="ascii_to_html",
    version="0.1",
    license="MIT",
    author="jlhs1001 (aka Liam Seewald)",
    author_email="jlhsdev@gmail.com",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/'
)