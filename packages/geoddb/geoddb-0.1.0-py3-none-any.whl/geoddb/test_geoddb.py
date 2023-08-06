'''
Given lat, lon -> store location with geohash and attributes
from contextlib import suppress
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

from geohash import encode, neighbors
from geoddb import GeoDDB

ddbTableName = 'DriveCoin-Backend-DDBTable-O6JGHHX91JZP'
session = boto3.Session(profile_name='drivecoin', region_name='us-west-2')
ddb = session.resource('dynamodb')
table = ddb.Table(ddbTableName);


# Delete all locations, expensive scan!
def deleteAllLocations():
    scanResp = table.scan(
        FilterExpression=Attr('PK').begins_with('loc#')
    )

    for item in scanResp['Items']:
        table.delete_item(
            Key={
                'PK': item['PK'],
                'SK': item['SK']
            }
        )

deleteAllLocations()

geoddb = GeoDDB(table, pk_name='PK', precision=4, prefix='loc#')

name = 'Daydream Surfshop'
address = '1588 Monrovia Ave, Newport Beach, CA 92663'
lat, lon = 33.63195443030888, -117.93583128993387
full_geohash = encode(lat, lon, precision=9)

data = {
    'SK': f'coffee#{name.lower()}#{full_geohash}',
    'EntityType': 'Coffee Shop',
    'Name': name,
    'Metadata': {
        'address': address,
        'lat': Decimal(str(lat)),
        'lon': Decimal(str(lon)),
    }
}


rv = geoddb.put_item(lat, lon, data)

myLat, myLon = 33.6464627, -117.9323207
# myLat, myLon = 34.4177084, -118.5626209

results = geoddb.query(myLat, myLon, ddb_kwargs={
    'KeyConditionExpression': Key('SK').begins_with('coffee#day'),
})

print(results)
'''
