from cx_Freeze import setup, Executable

options = {
    'build_exe': {
        'include_files': ['bg.jpg', 'space_marker.py', 'som.mp3', 'space.ico', 'space.png'],
    },
}

executables = [
    Executable('space_marker.py', base=None, icon='space.ico'),  # Adicione a opção 'icon' aqui
]

setup(
    name='NomeDoSeuApp',
    version='1.0',
    description='Descrição do seu aplicativo',
    options=options,
    executables=executables
)
