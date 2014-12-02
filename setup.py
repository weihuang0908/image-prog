from setuptools import setup
setup(
    name="image-prog",
    version='0.1',
    description='Haze Remove',
    author='Wei Huang',
    author_email='weihuang0908@qq.com',
    packages=["image-prog"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pymongo',
    	'pil',
        'numpy',
        'matplotlib',
        'pandas',
        'BeautifulSoup',
        'requests'
        # 'scikit-learn',
    ],
    test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries'
    ]
)