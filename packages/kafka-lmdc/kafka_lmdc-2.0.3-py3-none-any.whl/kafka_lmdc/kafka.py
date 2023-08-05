import os
import sys

from confluent_kafka import Producer, Consumer

# Biblioteca para Python & Kafka
# Read: https://docs.confluent.io/current/installation/configuration/consumer-configs.html

class KafkaAPI():

    @staticmethod
    def createConsumerWithKerberos(kafka_ip: str,
                                   group_id: str,
                                   kerberosKeyTabPath: str,
                                   kerberosUsername: str,
                                   autoOffsetReset: str = 'earliest',
                                   securityProtocol: str = 'SASL_PLAINTEXT',
                                   kafka_debug: bool = False) -> Consumer:
        conf = {
            'bootstrap.servers': kafka_ip,
            'group.id': group_id,
            'auto.offset.reset': autoOffsetReset,
            'security.protocol': securityProtocol,
            'sasl.mechanism': 'GSSAPI',
            'sasl.kerberos.service.name': 'kafka',
            'sasl.kerberos.keytab': kerberosKeyTabPath,
            'sasl.kerberos.principal': kerberosUsername
        }
        if kafka_debug:
            conf['debug'] = 'security,broker'

        c = Consumer(conf)
        return c

    @staticmethod
    def createConsumerWithLoginAndPass(kafka_ip: str,
                                       group_id: str,
                                       kafkaUserName: str,
                                       kafkaPassword: str,
                                       autoOffsetReset: str = 'earliest',
                                       securityProtocol: str = 'SASL_PLAINTEXT',
                                       kafka_debug: bool = False) -> Consumer:

        conf = {'bootstrap.servers': kafka_ip,
                'group.id': group_id,
                'auto.offset.reset': autoOffsetReset,
                'security.protocol': securityProtocol,
                'sasl.mechanism': 'PLAIN',
                'sasl.username': kafkaUserName,
                'sasl.password': kafkaPassword
                }
        if kafka_debug:
            conf['debug'] = 'security,broker'
        c = Consumer(conf)
        return c

    @staticmethod
    def createConsumerWithoutLogin(kafka_ip: str,
                                   group_id: str,
                                   autoOffsetReset: str = 'earliest',
                                   kafka_debug: bool = False) -> Consumer:
        conf = {
            'bootstrap.servers': kafka_ip,
            'group.id': group_id,
            'auto.offset.reset': autoOffsetReset
        }
        if kafka_debug:
            conf['debug'] = 'security,broker'
        c = Consumer(conf)
        return c

    @staticmethod
    def createProducerWithKerberos(kafka_ip: str,
                                   kafka_krb5_user_keytab_path: str,
                                   kafka_krb5_username: str,
                                   securityProtocol: str = 'SASL_PLAINTEXT',
                                   kafka_debug: bool = False) -> Producer:
        producer_conf = {'bootstrap.servers': kafka_ip,
                         'security.protocol': securityProtocol,
                         'sasl.mechanism': 'GSSAPI',
                         'sasl.kerberos.service.name': 'kafka',
                         'sasl.kerberos.keytab': kafka_krb5_user_keytab_path,
                         'sasl.kerberos.principal': kafka_krb5_username}

        try:
            if kafka_debug:
                producer_conf['debug'] = 'security,broker'
            producer = Producer(**producer_conf)
            return producer
        except BufferError:
            sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' % len(producer))
            return None

    @staticmethod
    def createProducerWithLoginAndPass(kafka_ip: str,
                                       kafkaUserName: str,
                                       kafkaPassword: str,
                                       securityProtocol: str = 'SASL_PLAINTEXT',
                                       kafka_debug: bool = False) -> Producer:
        # check this function
        try:
            producer_conf = {'bootstrap.servers': kafka_ip,
                             'security.protocol': securityProtocol,
                             'sasl.mechanism': 'PLAIN',
                             'sasl.username': kafkaUserName,
                             'sasl.password': kafkaPassword}
            if kafka_debug:
                producer_conf['debug'] = 'security,broker'

            producer = Producer(**producer_conf)
            return producer

        except BufferError:
            sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' % len(producer))
            return None

    @staticmethod
    def createProducerWithoutLogin(kafka_ip: str, kafka_debug: bool = False) -> Producer:
        try:
            producer_conf = {'bootstrap.servers': kafka_ip}
            if kafka_debug:
                producer_conf['debug'] = 'security,broker'

            producer = Producer(**producer_conf)
            return producer

        except BufferError:
            sys.stderr.write(
                '%% Local producer queue is full (%d messages awaiting delivery): try again\n' % len(producer))
            return None

    @staticmethod
    def createProducerFromEnvs() -> Producer:
        authType = os.environ['KAFKA_SASL_MECHANISM']  # GSSAPI(Kerberos) | NOSASL(Normal) | PLAIN(Password)
        severs = os.environ['KAFKA_HOST_URL']
        debug = os.environ['KAFKA_DEBUG'].lower() == 'true'
        if authType == "GSSAPI":
            return KafkaAPI.createProducerWithKerberos(
                severs,
                os.environ['KAFKA_KRB5_USER_KEYTAB_PATH'],
                os.environ['KAFKA_KRB5_USERNAME'],
                'SASL_PLAINTEXT',
                debug
            )
        elif authType == "PLAIN":
            return KafkaAPI.createProducerWithLoginAndPass(
                severs,
                os.environ['KAFKA_PLAIN_USERNAME'],
                os.environ['KAFKA_PLAIN_PASSWORD'],
                'SASL_PLAINTEXT',
                debug
            )
        elif authType == "NOSASL":
            return KafkaAPI.createProducerWithoutLogin(severs, debug)
        else:
            return None

    @staticmethod
    def createConsumerFromEnvs(groupId=None, autoOffsetReset: str = 'earliest') -> Consumer:
        if groupId is None:
            groupId = os.environ['KAFKA_GROUP_ID']
        authType = os.environ['KAFKA_SASL_MECHANISM']  # GSSAPI(Kerberos) | NOSASL(Normal) | PLAIN(Password)
        severs = os.environ['KAFKA_HOST_URL']
        debug = os.environ['KAFKA_DEBUG'].lower() == 'true'
        if authType == "GSSAPI":
            return KafkaAPI.createConsumerWithKerberos(
                severs, groupId,
                os.environ['KAFKA_KRB5_USER_KEYTAB_PATH'],
                os.environ['KAFKA_KRB5_USERNAME'],
                autoOffsetReset,
                'SASL_PLAINTEXT',
                debug
            )
        elif authType == "PLAIN":
            return KafkaAPI.createConsumerWithLoginAndPass(
                severs,
                groupId,
                os.environ['KAFKA_PLAIN_USERNAME'],
                os.environ['KAFKA_PLAIN_PASSWORD'],
                autoOffsetReset,
                'SASL_PLAINTEXT',
                debug
            )
        elif authType == "NOSASL":
            return KafkaAPI.createConsumerWithoutLogin(severs, groupId, autoOffsetReset, debug)
        else:
            return None
