import setuptools

setuptools.setup(
    name = 'Python-Gravity',
    version = '1.0.0',
    url = 'https://github.com/gaming32/pygravity',
    author = 'Gaming32',
    author_email = 'gaming32i64@gmail.com',
    license = 'License :: OSI Approved :: MIT License',
    description = 'Library for calculating stuff having to do with gravity',
    long_description = '',
    long_description_content_type = 'text/markdown',
    package_data = {
        'pygravity': [
            'py.typed',
            'math.pyi',
        ],
        'pygravity.twod': [
            'py.typed', 
            'vector.pyi',
            'physics.pyi',
            'gravity.pyi',
        ],
    },
    packages = [
        'pygravity',
        'pygravity.twod',
    ],
    ext_modules = [
        setuptools.Extension('pygravity.math', ['pygravity/math.c']),
        setuptools.Extension('pygravity.twod.gravity', ['pygravity/twod/gravity.c']),
        setuptools.Extension('pygravity.twod.physics', ['pygravity/twod/physics.c']),
        setuptools.Extension('pygravity.twod.vector', ['pygravity/twod/vector.c']),
    ],
    zip_safe = False,
)
