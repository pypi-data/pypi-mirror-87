import setuptools

with open('README.md') as readme_file:
    README = readme_file.read()

setuptools.setup(
    name = 'desarte',
    version = '0.1.1',
    description = 'Simulador de eventos discretos.',
    long_description_content_type="text/markdown",
    long_desciption = README + '\n\n',
    author = 'Dr Ricado Marcelin Jimenez',
    url="https://github.com/BigData95/pip_simulator",
    keywords=["discrete-event", "event simulador", "distribuido"],
    packages=setuptools.find_packages(),
)
