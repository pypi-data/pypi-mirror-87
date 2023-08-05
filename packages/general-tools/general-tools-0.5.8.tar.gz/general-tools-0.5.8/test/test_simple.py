import general_tools as gt
import os
import time


def test_object_id():
    print(gt.generate_object_id())


def test_log_info():
    import logging
    # gt.set_log_name("xxx")
    gt.log_init_config('core', 'console')
    # logging.root.setLevel(logging.WARNING)
    gt.set_log_process_name(True)
    gt.set_log_thread_name(True)
    gt.log_info('logxxxxx')
    logging.info("aaaa")


def test_log_error():
    gt.log_init_config('core', '../logs', monit_queue='rabbit_monit')
    gt.log_error('error xxx')


def test_log_fatal():
    gt.log_init_config('core', '/tmp', monit_queue='rabbit_monit')
    gt.log_fatal('error xxx')


def test_log_task():
    gt.log_init_config('core', '/tmp/', 'rabbit_monit')
    gt.log_task_schedule("stock_tag_222", 60 * 10, "stock", "17-18")


def test_log_notice():
    gt.log_init_config('core', '/tmp/', 'rabbit_monit')
    gt.log_notice("中文测试")


def test_log_error_monit():
    gt.log_init_config('core', '../logs', 'rabbit1')
    gt.log_error('error xxx')


def test_log_exception():
    gt.log_init_config('core', '../logs')
    try:
        print(5 / 0)
    except Exception as ex:
        gt.log_exception(ex)


def test_config():
    print(gt.config('db_stock', 'dbms'))
    print(gt.config('database'))
    print(gt.config('log_level'))


def consume_message(msg):
    print(msg)
    print('deal one')
    # gt.log_info('consumer ' + str(os.getpid()) + ' msg=' + msg)
    # time.sleep(2)


def test_rabbit_produce():
    gt.log_init_config('core', '/tmp/')
    producer = gt.RabbitProducer()
    for i in range(1, 10):
        producer.send('test1', 'helloo=%d' % i)


def test_kafka_consumer():
    gt.log_init_config('core', '/tmp/logs')
    consumer = gt.RabbitConsumer(topic='test3',
                                 config_info={'user': 'admin', 'password': 'sense_mq@2018', 'host': '52.82.30.135',
                                              'port': 5672})
    consumer.execute(consume_message)


def handle_process_work(job):
    gt.log_info("job={0}".format(job))
    time.sleep(0.1)


@gt.catch_raise_exception
def raise_exception():
    return 1 / 0


def test_raise_exception():
    gt.log_init_config('core', '/tmp')
    raise_exception()


@gt.try_catch_exception
def try_catch_exception():
    return 1 / 0


def test_catch_exception():
    gt.log_init_config('core', '/tmp')
    try_catch_exception()


def test_multi_process():
    gt.log_init_config('core', '/tmp')
    gt.set_log_process_name(True)
    jobs = list()
    for i in range(100):
        jobs.append(i)
        gt.execute_multi_core("dumb", handle_process_work, jobs, 4, True)


def test_mq():
    factory = gt.RabbitmqFactory('rabbit_monit')
    print(factory.list_queues())


def function_cal(body):
    import json
    msg = json.loads(body)
    print(msg['msg_header']['msg_idx'])
    time.sleep(1)


def test_rabbit_produce1():
    gt.log_init_config('core', '/tmp/')
    producer = gt.RabbitProducer()
    producer.send('test1', 'helloo=%d' % 1)
    # for i in range(1, 10):
    #     producer.send('test1', 'helloo=%d' % i)


def test_rabbit_consume():
    gt.log_init_config('core', '/tmp/')
    consumer = gt.RabbitConsumer('test1', 'rabbit')
    consumer.execute_safely(rabbit_consume, prefetch_count=1, no_ack=False)


def rabbit_consume(body):
    gt.log_info(str(body))
    time.sleep(100)


def function_test():
    gt.log_init_config('core', '/tmp/logs')
    consumer = gt.RabbitConsumer('cloud_data_pdf_test', 'rabbit_cloud')
    consumer.execute_safely(function_cal)


def test_thread_scale():
    factory = gt.ThreadAutoFactory(queue='cloud_data_pdf_test', label='rabbit_cloud', monitor=60)
    factory.execute(function_test)


def test_db():
    from general_tools import get_db_factory, DBACTION
    mysqlet = get_db_factory('mysql_stock')
    res = mysqlet.findKeySql(DBACTION.EXE_BY_SQL, sql='select * from sites')
    print(res)


def test_redis():
    from general_tools import get_redis_client
    config_map = {
        'host': '52.82.48.136',
        'port': '6389',
        'pass': 'sensedeal'
    }
    client = get_redis_client(0, 'reids', config_map)
    st = client.keys()
    print(st)


def test_encrypt():
    from general_tools import Encryption, log_info
    key = 'sdai0000'
    sk = Encryption.encrypt_key(key)
    print('\n')
    print('encrypt code: {}'.format(sk))
    log_info('sk: {}'.format(sk))
    code = Encryption.decrypt_key(sk)
    print(code)
    print(code == key)


def test_encrypt_dict():
    from general_tools import Encryption
    config_map = {'user': 'sdai', 'pass': 'sddddd222', 'host': '192.168.1.1', 'port': '32'}
    est = Encryption.encryt_dict(config_map)
    print(est)
    st = Encryption.decrypt_dict(est)
    print(st)
    est['port'] = 32
    print(est)
    print(Encryption.decrypt_dict(est))


def test_wechat():
    from general_tools import WechatFactory
    wechat = WechatFactory('wechat')
    wechat.send_message('111', [])


def test_email():
    from general_tools import EmailFactory
    email = EmailFactory('email')
    email.send_message('瞅你咋地', '你瞅啥')


def test_mq_fanout_produce():
    from general_tools import RabbitProducer
    import json
    produce = RabbitProducer('rabbit_88')
    for _k in range(1, 20):
        st = {'index': _k}
        produce.send_safely('alg_test_exc', json.dumps(st), exchange_type='fanout')
        print('send one {} sleep 10s'.format(_k))
        time.sleep(3)

def test_mq_fanout_consumer():
    import json
    from general_tools import RabbitConsumer
    def handler(body):
        print(body)
        st = json.loads(body)
        print(st)
    consumer = RabbitConsumer(topic='alg_dealed_result2', label='rabbit_88', heartbeat=300)
    consumer.execute_safely(handler, exchange='alg_test_exc')
