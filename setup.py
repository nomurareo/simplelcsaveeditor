import os
import sys
import shutil

from cx_Freeze import setup, Executable


# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    'excludes': ['pip', 'tkinter', 'unittest', 'setuptools', 'wheel', 'email', 'html', 'http', 'pydoc_data'],
    'bin_excludes': ['PySide6\\Qt6Network.dll'],
    'zip_include_packages': ['PySide6', 'Crypto'],
    'include_files': ['reo.jpg'],
    'optimize': 2,
}

# base='Win32GUI' should be used only for Windows GUI app
base = 'Win32GUI' if sys.platform == 'win32' else None

setup(
    name='simplelcsaveeditor',
    version='0.1',
    description='too lazy simple lethal company save editor by Reo Nomura',
    options={'build_exe': build_exe_options},
    executables=[
        Executable('app.py', base=base, icon='reo.ico', target_name='simplelcsaveeditor')
    ],
)

def remove_files_and_directories(root_directory, match_criteria):
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if match_criteria(file):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Removed file: {file_path}")

        for directory in dirs:
            if match_criteria(directory):
                dir_path = os.path.join(root, directory)
                shutil.rmtree(dir_path)
                print(f"Removed directory: {dir_path}")


def files_dirs_criteria(name):
    return name in remove_files or name in remove_dirs

remove_files = ['ascii.pyc', 'base64_codec.pyc', 'big5.pyc', 'big5hkscs.pyc', 'bz2_codec.pyc', 'charmap.pyc', 'cp037.pyc', 'cp1006.pyc', 'cp1026.pyc', 'cp1125.pyc', 'cp1140.pyc', 'cp1250.pyc', 'cp1251.pyc', 'cp1253.pyc', 'cp1254.pyc', 'cp1255.pyc', 'cp1256.pyc', 'cp1257.pyc', 'cp1258.pyc', 'cp273.pyc', 'cp424.pyc', 'cp500.pyc', 'cp720.pyc', 'cp737.pyc', 'cp775.pyc', 'cp850.pyc', 'cp852.pyc', 'cp855.pyc', 'cp856.pyc', 'cp857.pyc', 'cp858.pyc', 'cp860.pyc', 'cp861.pyc', 'cp862.pyc', 'cp863.pyc', 'cp864.pyc', 'cp865.pyc', 'cp866.pyc', 'cp869.pyc', 'cp874.pyc', 'cp875.pyc', 'cp932.pyc', 'cp949.pyc', 'cp950.pyc', 'Crypto.Cipher._raw_blowfish.pyd', 'Crypto.Cipher._raw_cast.pyd', 'Crypto.Cipher._raw_des.pyd', 'Crypto.Cipher._raw_des3.pyd', 'Crypto.Cipher._raw_eksblowfish.pyd', 'Crypto.Hash._SHA224.pyd', 'Crypto.Hash._SHA384.pyd', 'Crypto.Hash._SHA512.pyd', 'Crypto.PublicKey._ec_ws.pyd', 'Crypto.PublicKey._ed25519.pyd', 'Crypto.PublicKey._ed448.pyd', 'Crypto.PublicKey._x25519.pyd', 'euc_jisx0213.pyc', 'euc_jis_2004.pyc', 'euc_jp.pyc', 'euc_kr.pyc', 'frozen_application_license.txt', 'gb18030.pyc', 'gb2312.pyc', 'gbk.pyc', 'hex_codec.pyc', 'hp_roman8.pyc', 'hz.pyc', 'idna.pyc', 'iso2022_jp.pyc', 'iso2022_jp_1.pyc', 'iso2022_jp_2.pyc', 'iso2022_jp_2004.pyc', 'iso2022_jp_3.pyc', 'iso2022_jp_ext.pyc', 'iso2022_kr.pyc', 'iso8859_1.pyc', 'iso8859_10.pyc', 'iso8859_11.pyc', 'iso8859_13.pyc', 'iso8859_14.pyc', 'iso8859_15.pyc', 'iso8859_16.pyc', 'iso8859_2.pyc', 'iso8859_3.pyc', 'iso8859_4.pyc', 'iso8859_5.pyc', 'iso8859_6.pyc', 'iso8859_7.pyc', 'iso8859_8.pyc', 'iso8859_9.pyc', 'johab.pyc', 'koi8_r.pyc', 'koi8_t.pyc', 'koi8_u.pyc', 'kz1048.pyc', 'latin_1.pyc', 'libcrypto-3.dll', 'mac_arabic.pyc', 'mac_croatian.pyc', 'mac_cyrillic.pyc', 'mac_farsi.pyc', 'mac_greek.pyc', 'mac_iceland.pyc', 'mac_latin2.pyc', 'mac_roman.pyc', 'mac_romanian.pyc', 'mac_turkish.pyc', 'mbcs.pyc', 'oem.pyc', 'palmos.pyc', 'ptcp154.pyc', 'punycode.pyc', 'pyexpat.pyd', 'qdirect2d.dll', 'qgif.dll', 'qicns.dll', 'qico.dll', 'qminimal.dll', 'qoffscreen.dll', 'qpdf.dll', 'qsvg.dll', 'Qt6Network.dll', 'Qt6OpenGL.dll', 'Qt6Pdf.dll', 'Qt6Qml.dll', 'Qt6QmlModels.dll', 'Qt6Quick.dll', 'Qt6Svg.dll', 'Qt6VirtualKeyboard.dll', 'qtga.dll', 'qtiff.dll', 'QtNetwork.pyd', 'QtSvg.pyd', 'quopri_codec.pyc', 'qwbmp.dll', 'qwebp.dll', 'raw_unicode_escape.pyc', 'rot_13.pyc', 'select.pyd', 'shift_jis.pyc', 'shift_jisx0213.pyc', 'shift_jis_2004.pyc', 'tis_620.pyc', 'undefined.pyc', 'unicodedata.pyd', 'unicode_escape.pyc', 'utf_16.pyc', 'utf_16_be.pyc', 'utf_16_le.pyc', 'utf_32.pyc', 'utf_32_be.pyc', 'utf_32_le.pyc', 'utf_7.pyc', 'uu_codec.pyc', 'zlib_codec.pyc', '_bz2.pyd', '_decimal.pyd', '_hashlib.pyd', '_lzma.pyd', '_socket.pyd']
remove_dirs = ['generic', 'networkinformation', 'platforminputcontexts', 'tls', 'upx-4.2.1-win64', 'venv']

root_dir = 'build/exe.win-amd64-3.11'

remove_files_and_directories(root_dir, files_dirs_criteria)
