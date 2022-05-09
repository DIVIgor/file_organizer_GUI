import PySimpleGUI as sg
import shutil
import os
from datetime import datetime


sg.theme('DarkBlue17')
# sg.theme_button_color()
button_size = (8, 1)


MESSAGE_IN = 'Choose an input folder that needs to organize.'
MESSAGE_OUT = 'Choose an output folder. By default the same path as an input.'
FOUND_FILES = 'Found files:'
CHECK_MODES = [os.F_OK, os.R_OK, os.W_OK]
ERRORS = {
    'Incorrect path': "The path doesn't exist. Please input a correct path.",
    'Not readable': "The folder is not readable. Please choose another folder.",
    'Not writeable': "The folder is not writable. Please choose another folder.",
    'No path': "You need to input a path to organize your files.",
    'Empty folder': "The folder is empty."
}
FILE_FORMATS = {
    "PDF": (
        '.pdf',
        ),
    "Text (changable)": (
        '.doc', '.docx', '.odt',
        '.rtf','.tex', '.txt', '.wpd'
        ),
    "Spreadsheet": (
        '.xls', '.xlsx', '.xlsm', '.ods'
        ),
    "Programming": (
        '.py', '.c', '.cgi', '.class',
        '.cpp', '.cs', '.css', '.h',
        '.htm', '.html', '.java', '.js',
        '.jsp' '.php', '.pl', '.sh',
        '.swift', '.vb', '.xhtml'
        ),
    "Data and database": (
        '.csv', '.dat', '.db', '.dbf',
        '.log', '.mdb', '.sav', '.sql',
        '.tar', '.xml'
        ),
    "Compressed": (
        '.7z', '.arj', '.deb', '.pkg',
        '.rpm', '.tar.gz', '.z', '.zip',
        '.rar'
        ),
    "Audio": (
        '.aac', '.aif', '.cda', '.flac',
    	'.mid', '.midi', '.mp3', '.mpa',
    	'.ogg', '.wav', '.wma', '.wpl'
        ),
    "Disc images": (
        '.bin', '.dmg', '.iso', '.toast', '.vcd'
        ),
    "E-mail": (
        '.email', '.eml', '.emlx',
    	'.msg', '.oft', '.ost', '.pst', '.vcf'
        ),
    "Executables": (
        '.apk', '.bat', '.bin', '.com',
    	'.exe', '.gadget', '.jar', '.msi',
    	'.wsf'
        ),
    "Images": (
        '.ai', '.bmp', '.gif', '.ico',
    	'.jpeg', '.jpg', '.png', '.ps',
    	'.psd', '.svg', '.tif', '.tiff'
        ),
    "Presentations": (
        '.key', '.odp', '.pps', '.ppt', '.pptx'
        ),
    "Video": (
        '.3g2', '.3gp', '.avi', '.flv',
    	'.h264', '.m4v', '.mkv', '.mov',
    	'.mp4', '.mpg', '.mpeg', '.rm',
    	'.swf', '.vob', '.wmv'
        ),
    "System related": (
        '.bak', '.cab', '.cfg', '.cpl',
    	'.cur', '.dll', '.dmp', '.drv',
    	'.icns', '.ico', '.ini', '.lnk',
    	'.msi', '.sys', '.tmp'
        ),
    "Torrents": (
        '.torrent', 
        ),
    "Autocad": (
        '.dwg', '.dxf', '.dst', '.dwf', 
        '.dwfx', '.dws', '.dwt', '.dxb',
        '.sv$'
    )
}


layout = [
    # [sg.Menu(menu_layout)],
    [sg.Text(MESSAGE_IN, key='-MESSAGE-')],
    [
        sg.Input(key='-PATH-IN-', enable_events=True),
        sg.Button('Open', key='-OPEN-IN-', size=button_size)
    ],
    [sg.Text(MESSAGE_OUT, key='-MESSAGE-')],
    [
        sg.Input(key='-PATH-OUT-', enable_events=True),
        sg.Button('Open', key='-OPEN-OUT-', size=button_size)
    ],
    [sg.Button('Organize', size=button_size, expand_x=True)]
]


window = sg.Window('File Organizer', layout)

def check_access(path: str, modes: list, errors: dict):
    if not path:
        return sg.popup(errors['No path'])
    else:
        er_lst = list(errors.values())
        for mode in modes:
            if not os.access(path, mode):
                return sg.popup(er_lst[modes.index(mode)])

def check_files(path: str, error):
    file_list = os.listdir(path)
    if not file_list:
        return sg.popup(error)
    else:
        return file_list

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == '-OPEN-IN-':
        path = sg.popup_get_folder('Open', default_path=values['-PATH-IN-'])
        window['-PATH-IN-'].update(path)
    elif event == '-OPEN-OUT-':
        path = sg.popup_get_folder('Open', default_path=values['-PATH-IN-'])
        window['-PATH-OUT-'].update(path)


    if event == 'Organize':
        check_access(values['-PATH-IN-'], CHECK_MODES, ERRORS)

        if values['-PATH-IN-'] and os.access(values['-PATH-IN-'], CHECK_MODES[0]):
            path_in = values['-PATH-IN-']
            file_list = check_files(path_in, ERRORS['Empty folder'])
            quantity = len(file_list)

            if not values['-PATH-OUT-']:
                values['-PATH-OUT-'] = path_in
                window['-PATH-OUT-'].update(path_in)
            path_out = values['-PATH-OUT-']
            output = os.path.join(path_out,
                    'Organized files (' 
                    + datetime.now().strftime("%d-%B-%Y %H.%M.%S") 
                    + ')')
            os.mkdir(output)

            for f_type in FILE_FORMATS.keys():
                folder = os.path.join(output, f_type)
                os.mkdir(folder)
                files_by_type = []
                for file in reversed(file_list):
                    if file.rstrip().lower().endswith(FILE_FORMATS[f_type]):
                        files_by_type.append(file)
                        shutil.move(os.path.join(path_in, file), folder)
                        file_list.remove(file)
                if not files_by_type:
                    os.rmdir(folder)


            if file_list:
                folder = os.path.join(output, 'Other')
                os.mkdir(folder)
                for file in file_list:
                    shutil.move(os.path.join(path_in, file), folder)
            
            sg.popup(f"Organized {quantity} files and directories.")

window.close()