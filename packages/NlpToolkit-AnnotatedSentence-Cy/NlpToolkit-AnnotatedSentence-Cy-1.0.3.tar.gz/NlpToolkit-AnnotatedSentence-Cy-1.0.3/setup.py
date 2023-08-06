from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["AnnotatedSentence/*.pyx",
                           "AnnotatedSentence/AutoProcessor/AutoArgument/*.pyx",
                           "AnnotatedSentence/AutoProcessor/AutoNER/*.pyx",
                           "AnnotatedSentence/AutoProcessor/AutoPredicate/*.pyx",
                           "AnnotatedSentence/AutoProcessor/AutoSemantic/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-AnnotatedSentence-Cy',
    version='1.0.3',
    packages=['AnnotatedSentence', 'AnnotatedSentence.AutoProcessor', 'AnnotatedSentence.AutoProcessor.AutoNER',
              'AnnotatedSentence.AutoProcessor.AutoArgument', 'AnnotatedSentence.AutoProcessor.AutoSemantic',
              'AnnotatedSentence.AutoProcessor.AutoPredicate', 'AnnotatedSentence.AutoProcessor.AutoDisambiguation'],
    package_data={'AnnotatedSentence': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'AnnotatedSentence.AutoProcessor': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'AnnotatedSentence.AutoProcessor.AutoNER': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'AnnotatedSentence.AutoProcessor.AutoArgument': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'AnnotatedSentence.AutoProcessor.AutoSemantic': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'AnnotatedSentence.AutoProcessor.AutoPredicate': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'AnnotatedSentence.AutoProcessor.AutoDisambiguation': ['*.pxd', '*.pyx', '*.c', '*.py']},
    url='https://github.com/olcaytaner/AnnotatedSentence-Cy',
    license='',
    author='olcaytaner',
    author_email='olcaytaner@isikun.edu.tr',
    description='Annotated Sentence Processing Library',
    install_requires=['NlpToolkit-WordNet-Cy', 'NlpToolkit-NamedEntityRecognition-Cy', 'NlpToolkit-PropBank-Cy', 'NlpToolkit-DependencyParser-Cy']
)
