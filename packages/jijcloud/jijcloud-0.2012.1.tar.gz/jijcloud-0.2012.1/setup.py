from setuptools import setup, find_packages

setup(
    name="jijcloud",
    version="0.2012.1",
    install_requires=["dimod", "requests", "toml"],
    author_email='info@j-ij.com',
    author='Jij Inc.',
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points = {
        'console_scripts': ['jijcloud=jijcloud.config.config_command:main']
    },
    test_suite='tests',
    license='MIT',
)
