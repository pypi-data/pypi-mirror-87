import setuptools


about = {}
with open('sour_cereal/__about__.py') as fd:
    exec(fd.read(), about)


with open('README.md', 'r') as fd:
    long_description = fd.read()


setuptools.setup(
    name=about['name'],
    version=about['version'],
    author=about['author'],
    author_email=about['author_email'],
    description=about['description'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=about['keywords'],
    url=about['url'],
    download_url=about['download_url'],
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=about['classifiers'],
    license=about['license']
)
