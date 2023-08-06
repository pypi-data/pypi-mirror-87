import setuptools

setuptools.setup(
    name='import-env-file',
    version='2020.12.3',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
