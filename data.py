
def read_config(file_name):

    config = {}
    
    with open(file_name) as file:
        for line in file:
            param = line[0]
            if not (param in ('#','\n')):
                if param not in config:
                    config[param] = {}
                list = line.split('\n')[0].split(' ')
                desc = list[1]
                config[param][desc] = list[2:]

    return config