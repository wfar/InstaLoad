from cx_Freeze import setup, Executable

''' Converts source for InstaLoad into an .exe using cx_freeze. '''

target = Executable(
    script = 'InstaLoad.py',
    icon = 'icon.ico')

setup(name = 'Instaload',
      options = {"build_exe": {"packages":["idna",'urllib','urllib.request',
                'shutil','time','os', 'bs4','selenium', "requests", 'lxml']}},
      version = '1.1',
      description = 'Downlaods all images and videos from Instagram account.',
      executables = [target])

