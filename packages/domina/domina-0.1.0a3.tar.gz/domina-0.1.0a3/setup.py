import setuptools
import domina_util as util

setuptools.setup(
    name='domina',
    version=util.read_file('VERSION'),
    author='hexanona',
    author_email=''.join(
        ['hexanona','+','domina','@','mailbox.org']),
    description='Game AI script framework for MMORTS screeps.com',
    long_description=util.read_file('ABOUT'),
    long_description_content_type='text/plain',
    url='https://gitlab.com/screeps-domina/domina',
    classifiers=[
        'Topic :: Games/Entertainment :: Real Time Strategy',
        'Topic :: Software Development :: Version Control',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: JavaScript',
        'Development Status :: 1 - Planning',
    ],
    license='GPLv3',
    py_modules=[
        'domina',
        'domina_util',
    ],
    install_requires=['Click'],
    entry_points='''
    [console_scripts]
    domina=domina:cli
    ''',
    python_requires='>=3.7'
)
