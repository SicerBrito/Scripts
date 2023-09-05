import os.path
import shutil

home_folder = os.path.expanduser('~')
folder404 = "404NotFoundMyFriend"

def formatRuta(ruta):
    newHome = ''
    for a in ruta:
        if a == '\\':
            newHome = newHome + '/'
        else:
            newHome = newHome + a

    return newHome

newhome = formatRuta(home_folder) + '/'
rutaActual = os.path.abspath(os.getcwd())
rutaActual = formatRuta(rutaActual)

if __name__ == '__main__':
    for filename in os.listdir(newhome):
        name, extension = os.path.splitext(newhome + filename + '/')
        if filename == 'Pictures':
            shutil.copytree(name, rutaActual + '/recovery_data_Pictures')
        elif filename == 'Documents':
            shutil.copytree(name, rutaActual + '/recovery_data_Documents')
        elif filename == 'Music':
            shutil.copytree(name, rutaActual + '/recovery_data_Music')
        elif filename == 'Videos':
            shutil.copytree(name, rutaActual + '/recovery_data_Videos')
        elif filename == 'Downloads':
            shutil.copytree(name, rutaActual + '/recovery_data_Downloads')
        else:
            new_folder_path = os.path.join(rutaActual, folder404)
            os.makedirs(new_folder_path)