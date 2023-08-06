import setuptools

setuptools.setup(
    name='django-update-from-dict',
    version='2020.12.3',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
