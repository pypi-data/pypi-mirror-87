import setuptools


setuptools.setup(
    name='django-fs-email',
    version='1.0.2',
    packages=['fs_email'],
    include_package_data=True,
    install_requires=['html2text'],
    author='Yuri Lya',
    author_email='yuri.lya@fogstream.ru',
    url='https://github.com/fogstream/django-fs-email',
    license='The MIT License (MIT)',
    description='The Django-related reusable app provides the ability to send multipart emails and store them in a database.',
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    python_requires='>=3.6'
)
