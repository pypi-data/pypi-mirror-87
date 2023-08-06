from setuptools import setup, find_namespace_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

PKG_NAME = 'markipy'

setup(
    name='markipy',
    author='Marco T.',
    url='https://github.com/MarkNo1/MarkPy',
    version='0.1.6',
    license=license,
    description='MarkPy LIB',
    long_description=readme,
    packages=find_namespace_packages(include=[PKG_NAME, f'{PKG_NAME}.*']),
    entry_points={'console_scripts': [f'{PKG_NAME} = {PKG_NAME}.script:Main']},
    install_requires=requirements,
    include_package_data=True,
    package_data={PKG_NAME: ['gui/resource/*', 'gui/views/qml/*', 'gui/views/qml/components/*']},
    python_requires='>=3.7'
)
