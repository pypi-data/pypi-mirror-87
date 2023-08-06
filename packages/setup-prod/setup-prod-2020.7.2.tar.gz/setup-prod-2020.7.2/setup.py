import setuptools

setuptools.setup(
    name='setup-prod',
    version='2020.7.2',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages(),
    scripts=['scripts/setup-prod']
)
