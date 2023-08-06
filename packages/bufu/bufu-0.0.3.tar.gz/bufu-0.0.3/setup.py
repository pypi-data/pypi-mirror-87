import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='bufu',
    version='0.0.3',
    author='indigo13love',
    author_email='indigo13love@gmail.com',
    description='Minimal file upload for Snowflake internal stage',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files='LICENSE',
    url='https://github.com/indigo13love/bufu',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent'
    ],
    install_requires = [
        'snowflake-connector-python>=2.3.6',
        'fire>=0.3.1'
    ],
    entry_points = {
        'console_scripts': ['bufu = bufu.bufu:main']
    },
    python_requires='>=3.6,<3.9',
)
