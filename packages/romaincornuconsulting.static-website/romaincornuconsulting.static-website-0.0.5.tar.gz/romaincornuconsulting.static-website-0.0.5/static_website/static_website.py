from aws_cdk.core import Construct, CfnOutput


class StaticWebsite(Construct):

    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        CfnOutput(self, "Output", value='output')
        CfnOutput(
            self,
            'BucketName',
            value='bucketname123',
            export_name='BucketName'
        )