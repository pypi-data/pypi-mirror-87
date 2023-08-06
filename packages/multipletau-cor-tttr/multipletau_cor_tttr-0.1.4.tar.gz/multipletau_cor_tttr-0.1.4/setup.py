from setuptools import setup, Extension

#  https://stackoverflow.com/questions/4529555/building-a-ctypes-based-c-library-with-distutils
from distutils.command.build_ext import build_ext as build_ext_orig


class CTypesExtension(Extension):
    pass


class build_ext(build_ext_orig):

    def build_extension(self, ext):
        self._ctypes = isinstance(ext, CTypesExtension)
        return super().build_extension(ext)

    def get_export_symbols(self, ext):
        if self._ctypes:
            return ext.export_symbols
        return super().get_export_symbols(ext)

    def get_ext_filename(self, ext_name):
        if self._ctypes:
            return ext_name + '.so'
        return super().get_ext_filename(ext_name)


module = CTypesExtension('multipletau_cor_tttr/CCF',
                         sources=['multipletau_cor_tttr/CCF.c'])

setup(
    name='multipletau_cor_tttr',
    version='0.1.4',
    author='Anders Barth',
    license='MIT',
    author_email='anders.barth@gmail.com',
    packages=['multipletau_cor_tttr'],
    package_data={'multipletau_cor_tttr': ['sample_data.npy']},
    url='http://testpypi.python.org/pypi/multipletau_cor_tttr/',
    description='Library for correlation of time-tagged time-resolved photon '
                'data for fluorescence correlation spectroscopy (FCS) '
                'analysis.',
    long_description=open('README').read(),
    ext_modules=[module],
    install_requires=['numpy', 'matplotlib'],
    classifiers=['Programming Language :: Python :: 3',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent'],
    cmdclass={'build_ext': build_ext},
    keywords=['FCS Fluorescence Correlation Spectroscopy Single Photon '
              'Counting TTTR Multiple-tau algorithm']
)
