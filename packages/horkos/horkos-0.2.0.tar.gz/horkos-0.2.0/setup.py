from os import path
import collections
import setuptools

MY_DIR = path.abspath(path.dirname(__file__))
with open(path.join(MY_DIR, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name='horkos',
    version='0.2.0',
    description=(
        'A library for validating data at the edges of data systems.'
    ),
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Kevin Schiroo',
    author_email='kjschiroo@gmail.com',
    license='MIT',
    url='https://gitlab.com/kjschiroo/horkos',

    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['horkos=horkos.cmdline:main'],
    },
    project_urls=collections.OrderedDict(
        (
            ('Documentation', 'https://horkos.readthedocs.io/'),
            ('Code', 'https://gitlab.com/kjschiroo/horkos'),
            ('Issues', 'https://gitlab.com/kjschiroo/horkos/-/issues'),
        )
    ),
    install_requires=['pyyaml'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
