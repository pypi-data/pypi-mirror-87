from setuptools import find_packages, setup


with open('README.md') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='django-allauth-d120',
    version='0.0.5',
    packages=find_packages(),
    include_package_data=True,
    license='AGPL',
    description='Allauth provider for the D120 SSO',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/d120/django-allauth-d120',
    author='ckleemann',
    author_email='ckleemann@d120.de',
    install_requires=requirements,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
