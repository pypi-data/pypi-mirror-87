import src.lotusCore
import os

def main():
    xlaunch_location = os.path.abspath(os.path.dirname( __file__ ))
    os.chdir(xlaunch_location)
    #os.system('cmd.exe /C taskkill /IM lotus.xlaunch /F') lotus.xlaunch not found - - more research reqd
    os.system('cmd.exe /C lotus.xlaunch')
    os.system('env:QT_QPA_PLATFORM_PLUGIN_PATH="C:\Python33\Lib\site-packages\PyQt5\plugins\platforms"')
    src.lotusCore.main()

if __name__ == '__main__':
    main()
