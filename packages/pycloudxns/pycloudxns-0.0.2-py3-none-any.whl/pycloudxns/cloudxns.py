from .request import HTTP
import logging
import json

logger = logging.getLogger(__name__)


class CLOUDXNS:

    def __init__(self,API_KEY, SECRET_KEY):
        self.http = HTTP(API_KEY, SECRET_KEY)

    def getDomainList(self):
        """
        功能 域名列表
        HTTP 请求方式 GET
        URL https://www.cloudxns.net/api2/domain
        :return: Dict
        """

        return self.http.get('domain')

    def domain_host_list(self, domain_id, offset=0, row_num=2000, hostname=None):
        """
        功能 主机记录
        HTTP 请求方式 GET
        URL https://www.cloudxns.net/api2/host/:domain_id?offset=:offset&row_num=:row_num
            请求参数：
                参数名称 类型 必填 描述
                domain_id Integer 是 域名ID
                offset Integer  否 记录开始的偏移,第一条记录为 0,依次类推
                row_num Integer 否 要获取的记录的数量,比如获取 30 条,则为 30,最大可取 2000条
        :return: String
        """

        if row_num > 2000:
            row_num = 2000

        params = {'offset': offset, 'row_num': row_num}

        if hostname:
            params.update({'host_name': hostname})

        return self.http.get(f'host/{domain_id}', params=params)

    def domain_host_record_list(self,domain_id, host_id=None, offset=0, row_num=1, host_name=None):
        """
        功能 获取解析记录列表
        HTTP 请求方式 GET
        URL https://www.cloudxns.net/api2/record/:domain_id?host_id=0&offset=:offset&row_num=:row_num
        URL 参数说明
            domain_id:域名 id
            host_id:主机记录 id(传 0 查全部)
            offset:记录开始的偏移，第一条记录为 0，依次类推,默认取 0
            row_num:要获取的记录的数量， 比如获取 30 条， 则为 30,最大可取 2000
            条,默认取 30 条.
        :return:
            code int 请求状态，详见附件 code 对照表
            message String 操作信息，提示操作成功或错误信息
            total int 总记录条数
            offset int 记录开始的偏移
            row_num int 要获取的记录的数量
            data array 记录列表
                record_id: 解析记录 id
                host_id:主机记录 id
                host：主机记录名
                line_id：线路 ID
                line_zh：中文名称
                line_en：英文名称
                mx：优先级
                Value：记录值
                Type：记录类型
                Status：记录状态(ok 已生效 userstop 暂停)
                create_time：创建时间
                update_time：更新时间
        """

        if row_num > 2000:
            row_num = 2000

        params = {'domain_id': domain_id, 'offset': offset, 'row_num': row_num}

        if host_name:
            # params = {'domain_id': domain_id, 'host_id': host_id,'offset':offset,'row_num':row_num}
            params.update({'host_name': host_name})

        else:
            # params = {'domain_id': domain_id, 'host_name': host_name, 'offset': offset, 'row_num': row_num}
            params.update({'host_id': host_id})

        return self.http.get(f'record/{domain_id}', params=params)



    def domain_host_record_update(self,record_id,domain_id, host, value):
        """
        功能 更新解析记录
        HTTP 请求方式 GET
        URL https://www.cloudxns.net/api2/record/:id
            请求参数：
                参数名称 类型 必填 描述
                record_id Integer 解析记录id
                domain_id Integer 域名id
                host_name String 主机记录名称 如 www, 默认@
                value String 记录值, 如IP:8.8.8.8,CNAME:cname.cloudxns.net., MX: mail.cloudxns.net.
                record_type String 记录类型,通过 API 获得记录类型,大写英文,比如:A
                mx Integer 优先级,范围 1-100。当记录类型是 MX/AX/CNAMEX 时有效并且必选
                ttl Integer TTL,范围 60-3600,不同等级域名最小值不同
                line_id Integer 线路 id,(通过 API 获得记录线路 id)
                spare_data String 备IP
            :return: String
        """
        # _data = json.dumps({'domain_id': domain_id, 'host': host, 'value': value}).encode('UTF-8', 'ignore')
        return self.http.put(f'record/{record_id}', data=json.dumps({'domain_id': domain_id, 'host': host, 'value': value}))
