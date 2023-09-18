import boto3


def get_replicas_endpoints(primary_db_identifier):
    client = boto3.client("rds")
    response = client.describe_db_instances(
        DBInstanceIdentifier=primary_db_identifier,
        Filters=[
            {
                'Name': 'db-instance-id',
                'Values': [
                    primary_db_identifier
                ]
            },
        ]
    )
    replicas = response['DBInstances'][0]['ReadReplicaDBInstanceIdentifiers']
    endpoint_list = map(get_database_endpoint_details, replicas)
    return endpoint_list


def get_database_endpoint_details(db_identifier):
    client = boto3.client("rds")
    response = client.describe_db_instances(
        DBInstanceIdentifier=db_identifier,
        Filters=[
            {
                'Name': 'db-instance-id',
                'Values': [
                    db_identifier
                ]
            },
        ]
    )
    endpoint = response['DBInstances'][0]['Endpoint']
    return endpoint


if __name__ == '__main__':
    endpoints = get_replicas_endpoints("v757970-test")
    for endpoint in endpoints:
        print(f"Endpoint url {endpoint['Address']} and port {endpoint['Port']}")
