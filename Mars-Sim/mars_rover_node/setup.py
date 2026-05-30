from setuptools import find_packages, setup

package_name = 'mars_simulation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Nate',
    description='Advanced Mars Exploration Simulation Node',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'rover_node = mars_simulation.mars_rover_node:main'
        ],
    },
)
