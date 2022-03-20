#!/bin/sh
PYTHON_EXC=/usr/bin/python3

dir=`dirname \`readlink -f $0\``

# get channels
function test_case1(){
    $PYTHON_EXC "$dir/get_channels.py"
}

# get members
function test_case2(){
    $PYTHON_EXC "$dir/get_members.py"
}

# send text
function test_case3(){
    $PYTHON_EXC "$dir/send_text.py" \
        --user "804285680658284565" \
        --message "Hello World"
}

# send embed
function test_case4(){
    $PYTHON_EXC "$dir/send_embed.py" \
        --user "804285680658284565" \
        --title "Title" \
        --description "Description" \
        --color "0x3CD10C" \
        --fields "Line1" "Content1" "False" \
        --fields "Line2" "Content2" "True" \
        --fields "Line3" "Content3"
}

if ! [ -z "$1" ]; then
    func=test_case$1
    if type -t $func > /dev/null; then
        $func
    else
        echo case $1 not found
    fi
else
    echo case number not found
fi