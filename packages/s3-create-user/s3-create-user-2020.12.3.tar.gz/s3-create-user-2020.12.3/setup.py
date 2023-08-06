import setuptools

setuptools.setup(
    name='s3-create-user',
    version='2020.12.3',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages(),
    scripts=['scripts/s3-create-full-access-user','scripts/s3-create-read-only-user']
)
