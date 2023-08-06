from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ronchang',
    version='0.1.3',
    author='Ron Chang',
    author_email='ron.hsien.chang@gmail.com',
    description='Hands on toolkits',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Ron-Chang/ronchang',
    packages=find_packages(),
    license='MIT',
    python_requires='>=3.6',
    exclude_package_date={'':['.gitignore', 'dev', 'test', 'setup.py']},
    install_requires=[
        'colorama==0.4.3',
    ]
)
