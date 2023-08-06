from setuptools import setup, find_packages


def version():
    with open('VERSION', 'r') as f:
        return f.read().strip()


def readme():
    with open('README.md', 'r') as f:
        return f.read()


def requirements():
    with open('requirements.txt', 'r') as f:
        return f.read().split('\n')



setup(
    name='raspi_logger',
    version=version(),
    author='Mirko Mälicke',
    author_email='mirko@hydrocode.de',
    description='Raspberry Pi data logging software toolkit',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=requirements(),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'raspi_logger = raspi_logger.__main__' 
        ]
    },
    zip_safe=False
)