from setuptools import setup, find_packages

setup(
    name="ascii_to_html",
    version="0.1",
    license="MIT",
    author="jlhs1001 (aka Liam Seewald)",
    author_email="jlhsdev@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/jlhs1001/ascii-to-html",
    keywords="ANSI,HTML,python3,parse,parsing,convert,conversion,ansitohtml,Ansi,Html"
             "translation,translate,ascii,fast,simple,easy,web,tool,python,html,ansi,ansi2html"
)
