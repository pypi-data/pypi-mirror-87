import setuptools

setuptools.setup(
    name='launchd-add-logs',
    version='2020.12.3',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages(),
    scripts=['scripts/launchd-add-logs']
)
