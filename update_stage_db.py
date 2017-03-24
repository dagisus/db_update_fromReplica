import boto3
import time


client = boto3.client('rds')

db_instance = 
db_source_instance = 
db_instance_class = 
db_availability_zone = 


def create_readreplica():
    response = client.create_db_instance_read_replica(
        DBInstanceIdentifier=db_instance,
        SourceDBInstanceIdentifier=db_source_instance,
        DBInstanceClass=db_instance_class,
        AvailabilityZone=db_availability_zone,
        Port=5432,
        AutoMinorVersionUpgrade=True,
        PubliclyAccessible=False
    )
    return response


def promote_instance():
    response = client.promote_read_replica(
        DBInstanceIdentifier=db_instance,
        BackupRetentionPeriod=7
    )
    return response


def verify_instance_status():
    try:
        db_instance_dict = client.describe_db_instances(DBInstanceIdentifier=db_instance)
        db_instance_status = db_instance_dict['DBInstances'][0]['DBInstanceStatus']
    except:
        db_instance_status = 'deleted'
    return db_instance_status


def delete_instance():
    try:
        response = client.delete_db_instance(
            DBInstanceIdentifier=db_instance,
            SkipFinalSnapshot=True
        )
    except:
        response = 'fail, no database'
    return response


def update_db():
    delete_instance()
    time.sleep(1)
    while True:
        response = verify_instance_status()
        print 'status = {0}'.format(response)
        if response != 'deleting' or response == 'fail, no database':
            break
        time.sleep(60)
    create_readreplica()
    while True:
        response = verify_instance_status()
        print 'status = {0}'.format(response)
        if response == 'available':
            print 'status = {0}'.format(response)
            break
        time.sleep(60)
    promote_instance()
    while True:
        response = verify_instance_status()
        print 'status = {0}'.format(response)
        if response == 'available':
            print 'status = {0}'.format(response)
            break
        time.sleep(60)

update_db()
