import setuptools


setuptools.setup(
    name='django-fs-leonid',
    version='1.0.0',
    packages=['fs_leonid'],
    include_package_data=True,
    install_requires=[],
    author='Yuri Lya',
    author_email='yuri.lya@fogstream.ru',
    url='https://github.com/fogstream/django-fs-leonid',
    license='The MIT License (MIT)',
    description='The Django-related reusable app provides the ability to create and store in a database files such as robots.txt, sitemap.xml and so on.',
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
