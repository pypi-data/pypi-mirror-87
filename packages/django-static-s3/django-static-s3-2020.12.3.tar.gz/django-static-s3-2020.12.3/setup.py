import setuptools

setuptools.setup(
    name='django-static-s3',
    version='2020.12.3',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages(),
    scripts=['scripts/static-s3','scripts/static-s3-create-bucket','scripts/static-s3-create-env','scripts/static-s3-upload']
)
