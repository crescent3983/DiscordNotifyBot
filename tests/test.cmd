@echo off

set PYTHON_EXC="C:\Python37\python.exe"

IF "%1"=="1" call:test_case1
IF "%1"=="2" call:test_case2
IF "%1"=="3" call:test_case3
IF "%1"=="4" call:test_case4

goto :end

rem get channels
:test_case1
    %PYTHON_EXC% "%~dp0\get_channels.py"
    goto :end

rem get members
:test_case2
    %PYTHON_EXC% "%~dp0\get_members.py"
    goto :end

rem send text
:test_case3
    %PYTHON_EXC% "%~dp0\send_text.py" ^
            --user "804285680658284565" ^
            --message "Hello World"
    goto :end

rem send embed
:test_case4
    %PYTHON_EXC% "%~dp0\send_embed.py" ^
            --user "804285680658284565" ^
            --title "Title" ^
            --description "Description" ^
            --color "0x3CD10C" ^
            --fields "Line1" "Content1" "False" ^
            --fields "Line2" "Content2" "True" ^
            --fields "Line3" "Content3"
    goto :end

:end