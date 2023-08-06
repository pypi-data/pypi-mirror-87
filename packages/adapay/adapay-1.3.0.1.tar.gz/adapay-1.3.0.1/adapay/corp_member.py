import os

from adapay.request_tools import request_post, request_get, corp_member_create, corp_member_query


class CorpMember(object):

    @classmethod
    def create(cls, **kwargs):
        """
        创建企业用户
        """
        file_path = kwargs.get('attach_file')
        files = {'attach_file': (os.path.basename(file_path), open(file_path, 'rb'), 'application/octet-stream')}
        kwargs.pop('attach_file')
        return request_post(corp_member_create, kwargs, files)

    @classmethod
    def query(cls, **kwargs):
        """
        查询企业用户
        """
        url = corp_member_query.format(member_id=kwargs.get('member_id'))
        return request_get(url, kwargs)


if __name__ == '__main__':
    import time
    import adapay
    import logging
    from adapay_core.param_handler import read_file

    # app_id = 'app_f8b14a77-dc24-433b-864f-98a62209d6c4'
    app_id = 'app_7d87c043-aae3-4357-9b2c-269349a980d6'
    adapay.base_url = 'https://api-test.adapay.tech'
    adapay.config_path = os.getcwd()
    adapay.init_config('yfy_test_config', True)
    adapay.init_log(True, logging.INFO)
    adapay.public_key = read_file(adapay.config_path + '\\test_public_key.pem')


    def create_corp_member():
        # 创建企业用户
        order_no = str(int(time.time()))
        corp_member = adapay.CorpMember.create(app_id=app_id,
                                               order_no=order_no,
                                               member_id='hf_test_member_id3',
                                               name='测试企业1',
                                               prov_code='0031',
                                               area_code='3100',
                                               social_credit_code='social_credit_code',
                                               social_credit_code_expires='20200101',
                                               legal_person='frname',
                                               legal_cert_id='1234567890',
                                               legal_mp='13333333333',
                                               address='企业地址测试',
                                               attach_file=adapay.config_path + '\\request_tools.py',
                                               bank_acct_type='1')

        print('create corp_member resp:\n' + str(corp_member))


    def query_corp_member():
        # 查询企业用户
        corp_member = adapay.CorpMember.query(app_id='app_7d87c043-aae3-4357-9b2c-269349a980d6',
                                              member_id='corp_1243432427')

        print('query corp_member resp:\n' + str(corp_member))


    create_corp_member()
    query_corp_member()
