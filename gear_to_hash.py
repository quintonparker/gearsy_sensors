import json

def process(x):
    '''
    '''
    debug_mode = (execute('GET', 'config:debug_mode') == '1')
    hash_ttl = int(execute('GET', 'config:hash_ttl') or 0)

    if debug_mode:
        log(f"stream:{x['key']} id: {x['id']} payload:'{x['value']['payload']}'")

    hash_key = f'car:{x["id"]}'
    hash_dict = json.loads(x['value']['payload'])
    execute('HMSET', hash_key, *sum([[k,v] for k,v in hash_dict.items()],[]))

    if hash_ttl > 0:
        execute('EXPIRE', hash_key, hash_ttl)

gb = GearsBuilder('StreamReader')
gb.foreach(process)
# gb.register('sensor:1')
gb.register(prefix='sensor:*', trimStream=False)