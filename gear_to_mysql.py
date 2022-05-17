from rgsync import RGWriteBehind, RGWriteThrough
from rgsync.Connectors import MySqlConnector, MySqlConnection

'''
Create MySQL connection object
'''
connection = MySqlConnection('demo_rw', '4lly0urb4s3', '10.132.0.52:3306/demo')

'''
Create MySQL cars connector
'''
carsConnector = MySqlConnector(connection, 'cars', 'car_id')

carsMappings = {
	'registration': 'registration',
	'brand': 'brand',
	'color': 'color',
	'body_type': 'body_type',
	'speed': 'speed'
}

RGWriteBehind(GB, keysPrefix='car', mappings=carsMappings, connector=carsConnector, name='CarsWriteBehind', version='99.99.99')