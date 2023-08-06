import setuptools


# with open('README.md') as f:
#     README = f.read()

setuptools.setup(
    author="Abhay Kumar",
    author_email="abhay@trell.in",
    name='trell_ai_gender_prediction',
    description='Gender Prediction based on name',
    version='v0.0.0',
    url='https://gitlab.com/abhay7/trell-ai-gender-pred',
    packages=setuptools.find_packages(),
    python_requires=">=3.6.9",
    install_requires=[ "scikit-learn",
                      ],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'

    ],
)


