import setuptools

with open('README.rst') as file:
    readme = file.read()

name = 'incise'

version = '1.0.1'

author = 'Exahilosys'

url = 'https://github.com/{0}/{1}'.format(author, name)

setuptools.setup(
    name = name,
    python_requires = '>=3.5',
    version = version,
    url = url,
    packages = setuptools.find_packages(),
    license = 'MIT',
    description = 'Segmentation framework.',
    long_description = readme,
    extras_require = {
        'docs': [
            'sphinx',
            'sphinx_rtd_theme'
        ]
    },
    entry_points = {
        'console_scripts': [
            f'{name} = {name}.vendor:serve',
        ]
    }
)
