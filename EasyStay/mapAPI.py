
def get_key():
    key = None    
    try:
        with open('map.key', 'r') as file:
            key = file.readline().strip()
    except:
        try:
            with open('../map.key') as file:
                key = file.readline().strip()
        except:
            raise IOError('map key not found')
    if not key:
        raise KeyError('map key not found')
    
    return key

