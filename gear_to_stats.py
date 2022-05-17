import json

def process(x):
    '''
    '''
    car = json.loads(x['value']['payload'])

    log(f"car:{car}")

    # count all the sightings
    execute('INCR', 'stats:cars:counter')
    # add to HLL to count unique sightings by registration
    execute('PFADD', 'stats:cars:unique', car['registration'])
    # add sightings by registration to bloom filter
    execute('BF.ADD', 'stats:cars:set', car['registration'])
    # add to bloom top-k for top 5 list of sightings by brand
    if not execute('EXISTS', 'stats:cars:leaderboard'):
        execute('TOPK.RESERVE', 'stats:cars:leaderboard', 5, 2000, 7, 0.925)

    execute('TOPK.ADD', 'stats:cars:leaderboard', car['brand'])

    # add to timeseries to trend speeds over 30 days
    if not execute('EXISTS', 'stats:cars:speed'):
        execute('TS.CREATE', 'stats:cars:speed', 'RETENTION', 86400*30)

    ts = x['id'][:x['id'].index('-')]
    execute('TS.ADD', 'stats:cars:speed', ts, car['speed'])


gb = GearsBuilder('StreamReader')
gb.foreach(process)
# gb.register('sensor:1')
gb.register(prefix='sensor:*', trimStream=False)