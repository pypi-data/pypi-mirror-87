import setuptools

pypi_url = 'https://pypi.org/project/pyfactor'
github_url = 'https://github.com/felix-hilden/pyfactor'
documentation_url = github_url

setuptools.setup(
    name='pyfactor',
    version='0.0.1',
    description='A script dependency visualiser.',

    url=documentation_url,
    download_url=pypi_url,
    project_urls={
        'Source': github_url,
        'Issues': github_url + '/issues',
        'Documentation': documentation_url,
    },

    author='Felix Hildén',
    author_email='felix.hilden@gmail.com',
    maintainer='Felix Hildén',
    maintainer_email='felix.hilden@gmail.com',

    license='MIT',
    keywords='dependency visualiser',
    packages=[],
    python_requires='>=3.6',
)
