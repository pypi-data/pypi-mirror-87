import os
import boto3
import configparser
import json

def load_config(source_type, environment = None, project = 'BASA', file_name = None, region = None):
    if source_type == 'ssm' and environment:
        return load_config_from_ssm(environment, region)

    if source_type == 'env' and environment:
        return load_config_from_env(project, environment) 

    if source_type == 'file' and file_name:
        return load_config_from_file(file_name)

    raise Exception(f'No confguration loader source defined for {source_type}') 

def load_config_from_ssm(environment, region):
    configuration = configparser.ConfigParser()
    add_environment(configuration,environment)
    client = boto3.client('ssm', region_name = region)  
    param_details = client.get_parameters_by_path(Path="/"+environment+"/", Recursive = True)
    
    if 'Parameters' in param_details and len(param_details.get('Parameters')) > 0:
        for param in param_details.get('Parameters'):
            param_path_array = param.get('Name').split("/")
            section_position = len(param_path_array) - 1
            section_name = param_path_array[section_position]
            config_values = json.loads(param.get('Value'), parse_int = int)
            config_dict = {section_name: config_values}
            configuration.read_dict(config_dict)
    return configuration

def load_config_from_env(project, environment):
    '''
    Obtain all environment variables that has corresponding prefix PROJECT_PRE|PRO_ and loads all those in ConfigParses configuration, grouped by section
    Ej:
    MYPROJECT_PRO_DDBB_HOST=ddbbname.host.com will be loaded as section:ddbb, key:host, value:ddbbname.host.com
    '''
    prefix = f'{project.upper()}_{environment.upper()}_'
    configuration = configparser.ConfigParser()
    add_environment(configuration,environment)
    
    for k in os.environ:
        if k.startswith(prefix):
            var_value = os.environ[k]
            section_name,var_name = k.lstrip(prefix).split('_', maxsplit=1) # maxsplit=1 to allow properties with underscore in its name.
            section = {section_name.lower() : {var_name.lower() : var_value} }
            configuration.read_dict(section)
    return configuration        

def load_config_from_file(file_name):
    config = configparser.RawConfigParser()
    config.read(file_name)
    return config

def add_environment(configuration, environment):
    configuration.add_section('global')
    configuration.set('global','environment',environment)