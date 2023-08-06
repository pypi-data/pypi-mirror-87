# from distutils.core import setup
# from setuptools import find_packages
import setuptools

with open("README.md", "r", encoding="utf8") as f:
    long_description = f.read()

setuptools.setup(name='codebear',  # 包名
      version='1.0.3',  # 版本号
      description='A pygame role package',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='yyb',
      author_email='877665814@qq.com',
      install_requires=[],
      license='MIT',
      packages=setuptools.find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )

# with open("README.md", "r") as fh:
#     long_description = fh.read()
#
# setuptools.setup(
#     name="example-pkg-YOUR-USERNAME-HERE",  # Replace with your own username
#     version="0.0.1",
#     author="Example Author",
#     author_email="author@example.com",
#     description="A small example package",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/pypa/sampleproject",
#     packages=setuptools.find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires='>=3.6',
# )
