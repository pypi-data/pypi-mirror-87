import boto3
from basacommons.SingletonMeta import SingletonMeta

class AlertManager(metaclass = SingletonMeta):

    def __init__(self, config):
        self.environment = config.get('global','environment')
        self.source = config.get('alert','source')
        self.recipients = config.get('alert','recipients').split(',')

    def sendAlert(self, text):
        self.sendSESEmail(self.source, self.recipients, f'[{self.environment}] Alert', text)

    def sendSESEmail(self, from_address, to_addresses, subject, body):
        client = boto3.client('ses')
        client.send_email( Destination={
                'ToAddresses': to_addresses,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': body,
                    }
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source=from_address
        )

    
    