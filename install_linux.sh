CURRENT_FILE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#export LOCAL_BASE="$CURRENT_FILE_DIR/sdl_x64_linux/" 
#export SDL_CONFIG="$CURRENT_FILE_DIR/sdl_x64_linux/sdl2-config"
$CURRENT_FILE_DIR/py3.9/bin/pypy -m pip install pygame==2.1.2 --target $CURRENT_FILE_DIR/libraries/