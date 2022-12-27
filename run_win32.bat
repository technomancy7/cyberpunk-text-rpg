SET mypath=%~dp0
echo Currently running in %mypath:~0,-1% 
echo Python runtime is at %mypath:~0,-1%/winpy32/python-3.10.8/python.exe
echo Testing...
%mypath:~0,-1%/winpy64/python-3.10.8.amd64/python.exe --version
%mypath:~0,-1%/winpy64/python-3.10.8.amd64/python.exe %mypath:~0,-1%
