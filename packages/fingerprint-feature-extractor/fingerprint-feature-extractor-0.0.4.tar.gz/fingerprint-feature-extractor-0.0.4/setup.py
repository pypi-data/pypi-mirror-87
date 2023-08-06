from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
     name='fingerprint-feature-extractor',
     version='0.0.4',
     author="utkarsh-deshmukh",
     author_email="utkarsh.deshmukh@gmail.com",
     description="extract fingerprint minutiae features",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Utkarsh-Deshmukh/Fingerprint-Feature-Extraction",
     download_url="https://github.com/Utkarsh-Deshmukh/Fingerprint-Feature-Extraction/archive/master.zip",
     install_requires=['numpy==1.19.0', 'opencv-python', 'scipy', 'scikit-image'],
     license='MIT',
     keywords='Fingerprint Minutiae Feature Extraction',
     packages=find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )