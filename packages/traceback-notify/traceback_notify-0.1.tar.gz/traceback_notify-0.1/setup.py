import setuptools

dependencies = [
    'sendgrid==6.4.8',
    'Jinja2==2.11.2'
]

setuptools.setup(
    name='traceback_notify',
    version='0.1',
    author='Ihor Vnukov',
    packages=['traceback_notifier'],
    package_data={"": ["*.html", ]},
    license='MIT',
    install_requires=dependencies,
    python_requires='>=3.6'
)
