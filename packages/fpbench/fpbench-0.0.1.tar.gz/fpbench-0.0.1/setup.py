import setuptools

with open('README.md', 'rt') as f:
    long_description = f.read()


setuptools.setup(
    name='fpbench',
    version='0.0.1',
    author='Bill Zorn',
    author_email='bill.zorn@gmail.com',
    url='https://github.com/billzorn/fpy',
    description='FPBench utilities in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['fpbench'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
