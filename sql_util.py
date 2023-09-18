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
    return map(get_database_endpoint_details, replicas)


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
    return response['DBInstances'][0]['Endpoint']


def main():
    primary_db_identifier = "test"
    endpoints = get_replicas_endpoints(primary_db_identifier)
    for endpoint in endpoints:
        print(f"Endpoint url {endpoint['Address']} and port {endpoint['Port']}")


if __name__ == '__main__':
    main()
