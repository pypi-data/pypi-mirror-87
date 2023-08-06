from .request import HTTP
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class DNSXONE:

    def __init__(self,API_KEY, UID):
        self.http = HTTP(API_KEY, UID)

    def getDomainList(self) -> List:

        return self.http.post(
            params={'c': 'domain', 'a': 'getList'},
            data={
                'format': 'json',
                # "keyword": "",
                # "offset": "0",
                "length": "1000",
                # "group_id": "null"
            }
        )['domains']


    def createDomain(self,domain) -> Dict:
        """
        新增域名
        'https://console.dnsxone.com/api/?c=domain&a=domainAdd'
        :return: {'status': {'code': 1, 'created_at': '2020-11-05 10:47:28', 'message': '操作成功'}, 'domain': {'id': 'foo3.com', 'punycode': 'foo3.com', 'domain': 'foo3.com', 'flags': None, 'pid': '1', 'pname': '企業版', 'pid_expire_time': None}, 'ret': 'foo3.com'}
        """
        return self.http.post(
            params={'c': 'domain', 'a': 'domainAdd'},
            data={
                'format': 'json',
                'domain': domain
            }
        )

    def getDomainRecordList(self,domain) -> List:
        """
        獲取域名紀錄列表
        :param domain:
        :return: {'status': {'code': 1, 'message': 'successflu', 'created_at': '2020-11-05 10:37:14'}, 'domain': {'id': 'foo2.com', 'name': 'foo2.com', 'punycode': 'foo2.com', 'pid': '1', 'pname': '企業版', 'pid_expire_time': '', 'record_ns_protection': ''}, 'info': {'sub_domains': '4', 'record_total': '4'}, 'records': [{'monitor_flag': '0', 'id': '1', 'name': '@', 'line': '默认', 'type': 'NS', 'value': 'ns1.dnsx365.com.', 'ttl': '3600', 'enabled': 1, 'status': 'enable', 'backup': 0, 'visible': 1, 'cdn': 0, 'hold': 'hold', 'cdnSiteStatus': False, 'cb_domain_id': None, 'cdn_pid': None, 'monitor_status': '', 'remark': '', 'updated_on': '2020-11-05 10:37:14', 'monitor': None, 'monitor_enable': '', 'monitor_switch': None, 'monitor_error': None, 'ns_protection': None, 'height_cf': None, 'height_ho': None, 'height_cb': None, 'height_th': None, 'height_sh': None, 'height_tc': None, 'height_ce': None, 'orig_t': None, 'orig_value': None}, {'monitor_flag': '0', 'id': '2', 'name': '@', 'line': '默认', 'type': 'NS', 'value': 'ns2.dnsx365.com.', 'ttl': '3600', 'enabled': 1, 'status': 'enable', 'backup': 0, 'visible': 1, 'cdn': 0, 'hold': 'hold', 'cdnSiteStatus': False, 'cb_domain_id': None, 'cdn_pid': None, 'monitor_status': '', 'remark': '', 'updated_on': '2020-11-05 10:37:14', 'monitor': None, 'monitor_enable': '', 'monitor_switch': None, 'monitor_error': None, 'ns_protection': None, 'height_cf': None, 'height_ho': None, 'height_cb': None, 'height_th': None, 'height_sh': None, 'height_tc': None, 'height_ce': None, 'orig_t': None, 'orig_value': None}, {'monitor_flag': '0', 'id': '10001', 'name': 'test', 'line': '默认', 'type': 'A', 'value': '1.1.1.1', 'ttl': '60', 'enabled': 1, 'status': 'enable', 'backup': 0, 'visible': 1, 'cdn': 0, 'hold': '', 'cdnSiteStatus': False, 'cb_domain_id': None, 'cdn_pid': None, 'monitor_status': '', 'remark': '', 'updated_on': '2020-11-05 10:37:14', 'monitor': None, 'monitor_enable': 'yes', 'monitor_switch': None, 'monitor_error': None, 'ns_protection': None, 'height_cf': None, 'height_ho': None, 'height_cb': None, 'height_th': None, 'height_sh': None, 'height_tc': None, 'height_ce': None, 'orig_t': None, 'orig_value': None}, {'monitor_flag': '0', 'id': '10002', 'name': 'test', 'line': '默认', 'type': 'A', 'value': '1.1.1.1', 'ttl': '60', 'enabled': 1, 'status': 'enable', 'backup': 0, 'visible': 1, 'cdn': 0, 'hold': '', 'cdnSiteStatus': False, 'cb_domain_id': None, 'cdn_pid': None, 'monitor_status': '', 'remark': '', 'updated_on': '2020-11-05 10:37:14', 'monitor': None, 'monitor_enable': 'yes', 'monitor_switch': None, 'monitor_error': None, 'ns_protection': None, 'height_cf': None, 'height_ho': None, 'height_cb': None, 'height_th': None, 'height_sh': None, 'height_tc': None, 'height_ce': None, 'orig_t': None, 'orig_value': None}], 'siteStatus': None}
        """
        return self.http.post(
            params={'c': 'record', 'a': 'list'},
            data={
                'format': 'json',
                'domain': domain,
                # "offset": "0",
                "length": "2000",
                # "keyword": "",
                # "line": "",
                # "t": "",
                # "flags": "0",
                # "monitor_flag": "0"
            }
        )['records']

    def createDomainRecord(self,domain, name, record_type, record_line, value, **kwargs):
        """
        新增指定域名紀錄
        curl -X POST 'https://console.dnsxone.com/api/?c=record&a=add' -d 'api_key=id&uid=1&format=json&domain=aaa.com&sub_domain=yydud&record_type='A'&value=1.1.1.1'
        :param domain:
        :param sub_domain:
        :param record_type: A
        :param record_line: "海外" or "默认" or "中国大陆"
        :return: {'status': {'code': 1, 'created_at': '2020-11-05 10:50:04', 'message': '操作成功'}, 'record': {'id': '10001', 'name': 'test', 'status': 'enable', 'monitor_enable': 'yes'}}
        """
        return self.http.post(
            params={'c': 'record', 'a': 'add'},
            data={
                'format': 'json',
                'domain': domain,
                "sub_domain": name,
                "record_type": record_type,
                "record_line": record_line,
                "value": value
            }
        )

    def updateDomainRecord(self,domain, record_id, name, record_type, record_line, value, **kwargs):
        """
        新增指定域名紀錄
        curl -X POST 'https://console.dnsxone.com/api/?c=record&a=modify' -d 'api_key=id&uid=1&format=json&domain=aaa.com&sub_domain=yydud&record_type='A'&value=1.1.1.1'
        :param record_id:
        :param domain:
        :param sub_domain:
        :param record_type: A
        :param record_line: "海外" or "默认" or "中国大陆"
        :return: {'status': {'code': 1, 'created_at': '2020-11-05 10:50:04', 'message': '操作成功'}, 'record': {'id': '10001', 'name': 'test', 'status': 'enable', 'monitor_enable': 'yes'}}
        """
        return self.http.post(
            params={'c': 'record', 'a': 'modify'},
            data={
                'format': 'json',
                "record_id": record_id,
                'domain': domain,
                "sub_domain": name,
                "record_type": record_type,
                "record_line": record_line,
                "value": value,
            }
        )

    def deleteDomainRecord(self,domain, record_id, **kwargs):
        """
        新增指定域名紀錄
        curl -X POST 'https://console.dnsxone.com/api/?c=record&a=del'
        :param domain:
        :param record_id:
        :return: {
                    "status": {
                        "code": 1,
                        "created_at": "2020-11-12 16:48:21",
                        "message": "操作成功"
                    }
                }
        """
        return self.http.post(
            params={'c': 'record', 'a': 'del'},
            data={
                'format': 'json',
                "domain": domain,
                "record_id": record_id

            }
        )

    def updateDomainRecordStatus(self,record_id, domain, status, **kwargs):
        """

        :param record_id: "10006"
        :param domain:  "androidfrom.com"
        :param status: "enable" or "disable"
        :return:
        """
        return self.http.post(
            params={'c': 'record', 'a': 'status'},
            data={
                'format': 'json',
                "record_id": record_id,
                "domain": domain,
                "status": status
            }
        )
