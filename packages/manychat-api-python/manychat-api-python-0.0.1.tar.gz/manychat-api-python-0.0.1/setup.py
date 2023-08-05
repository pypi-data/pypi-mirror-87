import setuptools

with open('README.md', 'r') as fp:
    long_description = fp.read()

setuptools.setup(
    name='manychat-api-python',
    version='0.0.1',
    author='Yury Gavrilov',
    author_email='yuriy@manychat.com',
    description='ManyChat API Python library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/manychat/manychat-api-python',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
