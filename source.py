#!/usr/bin/env python3

from os import getenv as _getenv, path as _path
from dotenv import load_dotenv
from sys import exit as _exit

#setup scrip paths
home = _getenv('HOME')
script_path = _path.dirname(_path.realpath(__file__))
env_deploy_script = script_path + "/.env"
env_docker_script = script_path + "/Docker/.env.docker"

def load_variables(variable: str, env_dict: dict) -> str:
    loaded = []
    i=0
    while i < len(env_dict):
        key = str(list(env_dict.keys())[i])
        value = str(env_dict.get(list(env_dict.keys())[i]))
        if (key == '' or key == None) and value == "True":
            error = key + " was not declared in env file"
            _exit(error)
        if key == variable:
            return _getenv(key)
        i += 1
    print("{variable} is not found in env")
    return 1

#load .env content
load_dotenv(env_deploy_script)
project_variables = {
    "PROJECT_NAME" : True, 
    "AWS_ACCESS_KEY_ID" : True, 
    "AWS_SECRET_KEY" : True, 
    "AWS_BUCKET_NAME" : True,
    "PROJECT_CUSTOM_NAME" : False,
    "CUSTOM_HOME" : False,
    "REPOSITORY" : False,
    "GITC_OPTIONS" : False,
    "MYSQL_USER" : False,
    "MYSQL_PASSWORD" : False }

project_name = load_variables("PROJECT_NAME", project_variables)
aws_access_key_id = load_variables("AWS_ACCESS_KEY_ID", project_variables)
aws_secret_key = load_variables("AWS_SECRET_KEY", project_variables)
aws_bucket_name = load_variables("AWS_BUCKET_NAME", project_variables)
project_custom_name = load_variables("PROJECT_CUSTOM_NAME", project_variables)
if project_custom_name == '' or None:
    project_custom_name = project_name
custom_home = load_variables("CUSTOM_HOME", project_variables)
if custom_home == '' or None:
    custom_home = "public/"
repository = load_variables("REPOSITORY", project_variables)
if repository == '' or None:
    repository = "git@gitlab.cosmos-web.ru:developers/{prokect_name}.git"
gitc_options = load_variables("GITC_OPTIONS", project_variables)
mysql_user = load_variables("MYSQL_USER", project_variables)
mysql_password = load_variables("MYSQL_PASSWORD", project_variables)

#load .env.docker content
load_dotenv(env_docker_script)
docker_variables = {
    "NGINX_PROJECT_PORT" : True, 
    "NGINX_VERSION" : True, 
    "MYSQL_DATABASE_PORT" : True, 
    "DB_VERSION" : True,
    "MYSQL_ROOT_PASSWORD" : False,
    "COMPOSER_VERSION" : False,
    "COMPOSER_INSTALL_FLAGS" : False,
    "NODE_VERSION" : False,
    "PHP_VERSION" : False,
    "PHP_MODULES" : False }

#home + "/projects/" + project_custom_name + "/"
env_docker_project = home + "/projects/" + project_custom_name + "/Docker/.env.docker"
env_delpoy_project = home + "/projects/" + project_custom_name + "/.env"