#!/usr/bin/env python3

import source as _source
from os import makedirs as _makedirs, system as _system
from random import sample as _sample
from fileinput import FileInput as _fileinput
from re import sub as _sub

def getports(rlow=51001, rhigh=51999):
    first = True
    ports = _sample(range(rlow, rhigh), 2)
    while is_port_in_use(ports[0]) and is_port_in_use(ports[1]):
        ports = _sample(range(rlow, rhigh), 2)
        first = False
    nginx_port = "NGINX_PROJECT_PORT="+str(ports[0])
    mysql_port = "MYSQL_DATABASE_PORT="+str(ports[1])
    with _fileinput(_source.env_docker_project, inplace=True) as file:
        for line in file:
            line = _sub('^NGINX_PROJECT_PORT=.*', nginx_port, line)
            line = _sub('^MYSQL_DATABASE_PORT=.*', mysql_port, line)
            print(line, end='')

def is_port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def mkdir(path: str):
    try:
        _makedirs(path)
        print(f"Nested directories '{path}' created successfully.")
    except FileExistsError:
        print(f"One or more directories in '{path}' already exist.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def setupinitial():
    project_directories = \
    ["/projects", 
    "/projects/"+_source.project_custom_name+"/www", 
    "/projects/"+_source.project_custom_name+"/database",
    "/projects/"+_source.project_custom_name+"/Docker/"]
    for dir in project_directories:
        if not _source._path.exists(_source.home+dir):
            mkdir(_source.home+dir)
    
    script_directories = \
    ["./site",
    "./database", 
    "./logs"]
    for dir in script_directories:
        if not _source._path.exists(dir):
            mkdir(dir)
    
    files_to_copy = \
    ["cp " + _source.script_path + "/Docker/docker-compose.yml " \
    + _source.home + "/projects/" + _source.project_custom_name + "/Docker/docker-compose.yml",
    "cp " + _source.script_path + "/Docker/Dockerfile " \
    + _source.home + "/projects/" + _source.project_custom_name + "/Docker/Dockerfile"]
    for file in files_to_copy:
        if not _source._path.exists(file):
            _system(file)
    return 0

#setupinitial()
#getports()