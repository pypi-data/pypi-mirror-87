import distutils.cmd
import distutils.log
import setuptools
import subprocess
from setuptools.command.sdist import sdist
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools import setup, find_packages, Extension
import sys
import os

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

cpp_module = Extension('PySlice_Tools.slice',
                        sources=['.PySlice/PySlice_Tools/slice/_slice.cpp','.PySlice/PySlice_Tools/slice/_slice.o'],
                        include_dirs=['/usr/local/include'],
                        library_dirs=['/usr/local/lib/boost'],
                        runtime_library_dirs=['/usr/local/lib/boost'],
                        libraries=['boost_python'])


class wxCommand(distutils.cmd.Command):
    sys.path.append('PySlice/PySlice_Tools/slice')
    description = ''
    user_options = []
    def initialize_options(self):
        return
    def finalize_options(self):
        return

    def run(self):
        # sudo apt-get install libboost-python-dev
        subprocess.run(["sudo", "apt-get","-y","install", "libboost-python-dev"], check=True)
        # pip3 install -U \-f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 \ wxPython
        subprocess.run(["pip3", "install", "-U", "-f", "https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04", "wxPython"], check=True)
        # sudo apt install libgtk-3-0
        subprocess.run(["sudo", "apt","-y", "install", "libgtk-3-0"], check=True)
        # sudo apt-get install libnotify4
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt-get","-y", "install", "libnotify4"], check=True)
        # sudo apt-get install libsdl2-2.0-0
        subprocess.run(["sudo", "apt-get","-y", "install", "libsdl2-2.0-0"], check=True)
        # pip3 install matplotlib
        subprocess.run(["pip3", "install", "matplotlib"], check=True)
        subprocess.run(["pip3", "install", "matplotlib", "--upgrade"], check=True)
        # sudo add-apt-repository ppa:linuxuprising/libpng12
        subprocess.run(["sudo", "add-apt-repository","-y", "ppa:linuxuprising/libpng12"], check=True)
        try:
            # sudo apt update
            subprocess.run(["sudo", "apt", "update"], check=True)
            # sudo apt install libpng12-0
            subprocess.run(["sudo", "apt", "install", "libpng12-0"], check=True)  
        except:
            command1 = "sudo wget http://se.archive.ubuntu.com/ubuntu/pool/main/libp/libpng/libpng12-0_1.2.54-1ubuntu1_amd64.deb".split()
            command2 = "sudo dpkg -i libpng12-0_1.2.54-1ubuntu1_amd64.deb".split()
            subprocess.run(command1, check=True)
            subprocess.run(command2, check=True)
    
class Develop(develop):
    def run(self):
        develop.run(self)

# class SrcDistro(sdist):
#   def run(self):
#     self.run_command('wx')
#     sdist.run(self)

class Installer(install):
    def run(self):
        self.run_command('wx')
        install.run(self)

if __name__ == "__main__":
    setup(
        setup_requires=['wheel != 0.1'],
        cmdclass={
            'wx': wxCommand,
            # 'sdist': SrcDistro,
            'install': Installer,
            #'develop': Develop,
        },
        long_description=long_description,
        long_description_content_type='text/markdown',
        name="PySlice_Tools",
        version="1.6",
        packages=find_packages(),
        package_data={'': ['*.so','*.cpp','*.o']},
        include_package_data=True,
        data_files=[('PySlice_Tools', ['PySlice_Tools/command_help.json']),
        ('PySlice_Tools', ['PySlice_Tools/slice/_slice.cpp','PySlice_Tools/slice/_slice.so','PySlice_Tools/slice/_slice.o'])],
        install_requires=[
            "wheel",
            "matplotlib"
        ],
        ext_module = [cpp_module],
        entry_points = {
            "console_scripts": [
                "pyslice = PySlice_Tools.app:main"
            ]
        }
    )