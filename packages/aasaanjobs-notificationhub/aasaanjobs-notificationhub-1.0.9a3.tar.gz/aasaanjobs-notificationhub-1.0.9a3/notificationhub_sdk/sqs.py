import importlib
import os
from configparser import (ConfigParser, NoOptionError, NoSectionError,
                          ParsingError)
from os import path

import boto3
from notificationhub_sdk.base import ImproperlyConfigured
from notificationhub_sdk.common import MessageType


class SQSProducer:
    """
    Used for pushing the messages to SQS
    """
    setting_keys = (
        ('region', 'NOTIFICATION_HUB_SQS_REGION'),
        ('queue_name', 'NOTIFICATION_HUB_SQS_QUEUE_NAME'),  # transactional queue name
        ('marketing_queue_name', 'NOTIFICATION_HUB_MARKETING_SQS_QUEUE_NAME'),
        ('otp_queue_name', 'NOTIFICATION_HUB_OTP_SQS_QUEUE_NAME'),
        ('eks_role_arn', 'EKS_ROLE_ARN'),
        ('local_dev_env', 'NOTIFICATION_HUB_LOCAL_ENV'),
    )

    def __init__(self, **kwargs):
        # Retrieve Settings
        self.region = self._get_setting(*self.setting_keys[0], True, **kwargs)
        self.queue_name = self._get_setting(*self.setting_keys[1], False, **kwargs)
        self.marketing_queue_name = self._get_setting(*self.setting_keys[2], False, **kwargs)
        self.otp_queue_name = self._get_setting(*self.setting_keys[3], False, **kwargs)
        self.eks_role_arn = self._get_setting(*self.setting_keys[4], False, **kwargs)
        self.local_dev_env = self._get_setting(*self.setting_keys[5], False, **kwargs)

        # check whether at least one queue is set or not
        if (self.queue_name is None or self.queue_name == "") and \
            (self.marketing_queue_name is None or self.marketing_queue_name == "") and \
                (self.otp_queue_name is None or self.otp_queue_name == ""):
            raise ImproperlyConfigured('At least one queue should be set.')

        self._session = None
        self._queue = None

        self.init_sqs_session()

    def _get_setting(self, kw_name, env_name, is_mandatory = False, **kwargs):
        if kwargs.get(kw_name):
            return kwargs[kw_name]
        value = self.__get_from_django_settings(env_name)
        # If not found in Django settings, retrieve from environment variables
        if not value:
            value = os.getenv(env_name)
        # Throw error if still failed to retrieve the setting
        # skip NOTIFICATION_HUB_LOCAL_ENV as this is only for local
        if is_mandatory and not value:
            raise ImproperlyConfigured('Missing required settings `{}`'.format(env_name))
        return value

    @staticmethod
    def __get_from_django_settings(name):
        """
        If the Django project is initiated, then retrieves the settings
        from Django settings
        :param name: Setting Name
        :return: Setting Value
        """
        try:
            module = importlib.import_module('django.conf')
            settings = getattr(module, 'settings')
            return getattr(settings, name, None)
        except ImportError:
            return None

    def init_sqs_session(self):
        """
        Initiates SQS session
        """
        # local env
        if self.local_dev_env:
            access_key_id, secret_access_key = self.get_aws_profile_credentials_from_local()
            client_kwargs = {
                'service_name': "sqs",
                'aws_access_key_id': access_key_id,
                'aws_secret_access_key': secret_access_key,
                'region_name': self.region
            }
            self._session = boto3.resource(**client_kwargs)
        # production and staging env
        else:
            client_kwargs = {
                'service_name': "sqs",
                'region_name': self.region
            }
            self._session = boto3.resource(**client_kwargs)
            # check whether the given information has the account number or not
            aws_client = boto3.client('sts') # .get_caller_identity().get('Account')
            if aws_client == None or aws_client == "":
                raise ImproperlyConfigured('Issue while connecting to SQS region `{}`'.format(self.region))
            
            # for EKS, we need to get the access key and secret key from the token
            if self.eks_role_ar and self.eks_role_arn != "":
                try:
                    token_path = "/var/run/secrets/eks.amazonaws.com/serviceaccount/token"
                    if not path.exists(token_path):
                        raise ImproperlyConfigured('Token not present in pod. Check token at `{}`'.format(token_path))
                    with open(token_path, 'r') as file:
                        access_details = file.read()
                    response = aws_client.assume_role_with_web_identity(
                        RoleArn=self.eks_role_arn,
                        RoleSessionName='string',
                        WebIdentityToken=access_details,
                    )
                    if not response:
                        raise ImproperlyConfigured('Issue with token in pod. Check token at `{0}` with {1} '.format(token_path, self.eks_role_arn))
                except ImportError:
                    raise ImproperlyConfigured('Token not present in pod. Check token at `{0}` with {1} '.format(token_path, self.eks_role_arn))     
        
        if self._session:
            self._queue = self._session.get_queue_by_name(QueueName=self.queue_name)
        else:
            raise ImproperlyConfigured('Issue while connecting to SQS region `{}`'.format(self.region))

    @staticmethod
    def get_aws_profile_credentials_from_local() -> tuple:
        '''
        get_aws_profile_credentials reads the profile_name from the arguments
        You can pass if you want to read any specific profile from the file.
        It return AWS access key and secret keys.
        '''
        config = ConfigParser()
        filename = '.aws/credentials'
        config.read([path.join(path.expanduser("~"),filename)])
        try:
            aws_access_key_id = config.get('default', 'aws_access_key_id')
            aws_secret_access_key = config.get('default', 'aws_secret_access_key')
        except:
            raise ImproperlyConfigured('Unable to find default configuration from AWS credentials in local env')
            
        return (aws_access_key_id, aws_secret_access_key)

    def send_message(self, message_body: str, message_type: MessageType) -> str:
        """
        Sends a message to Amazon SQS
        :param message_body: The message to be pushed to queue
        :param message_type: The type of message to be processed. This is used to identify the queue
        :returns The MessageId returned by AWS
        :raises ConnectionError if failure in sending occurs
        """
        queue_name = self.queue_name
        if message_type == MessageType.MARKETING:
            queue_name = self.marketing_queue_name
        elif message_type == MessageType.TRANSACTIONAL:
            queue_name = self.queue_name
        elif message_type == MessageType.OTP:
            queue_name = self.otp_queue_name

        self._queue = self._session.get_queue_by_name(QueueName=queue_name)
        res = self._queue.send_message(QueueUrl=self._queue.url, MessageBody=str(message_body))
        status_code = res.get('ResponseMetadata').get('HTTPStatusCode')
        if status_code / 100 != 2:
            raise ConnectionError('Failed to send message to Hub Queue')
        return res['MessageId']
