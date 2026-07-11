from configparser import ConfigParser
import os

def load_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    # Ищем database.ini в текущей папке TSIS1
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    
    if not os.path.exists(file_path):
        raise Exception(f"Config file {filename} not found at {file_path}")
        
    parser.read(file_path)
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f"Section [{section}] not found in the {filename} file.")
    return config