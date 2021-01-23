# EBS Snapshot remover 
# - Removes shared snapshots with other AWS accounts or AWS Marketplace
# - Set region and target AWS account ID
#

import boto3
from botocore.exceptions import ClientError

region = 'us-east-1'
ec2 = boto3.client('ec2', region_name=region)
accounts = boto3.client("sts").get_caller_identity()["Account"]
error = ""
SHARED_ACCOUNTS = [""] #add aws account id or aws-marketplace
marketplace_id = '679593333241' 

for i in ec2.describe_snapshots('ec2',region_name=region):
        permissions = ec2.describe_snapshot_attribute(Attribute='createVolumePermission',SnapshotId=i['SnapshotId'])
        if permissions['CreateVolumePermissions'] != []:
            try:
                    for UserId in permissions['CreateVolumePermissions']:
                        awsid =  UserId['UserId']
                        if awsid in SHARED_ACCOUNTS:
                             if awsid == 'aws-marketplace':
                                awsid = marketplace_id
                                remove = ec2.modify_snapshot_attribute(SnapshotId=['SnapshotId'],Attribute='createVolumePermission',OperationType='remove',UserIds=[awsid])
                                print("Removed " str(awsid) + " share from: " + permissions['SnapshotId'])
                            else:
                                remove = ec2.modify_snapshot_attribute(SnapshotId=['SnapshotId'],Attribute='createVolumePermission',OperationType='remove',UserIds=[awsid])
                                print("Removed " str(awsid) + " share from: " + permissions['SnapshotId'])
            except Exception as error:
                print("Error: %s" % error)
