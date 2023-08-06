import concurrent.futures
import re
import time
import logging

logger = logging.getLogger(__name__)

class XNSRecord:

    def __init__(self, CLOUDXNS, domain_id):
        self.xns = CLOUDXNS
        self.domain_id = domain_id
        self._data = self._get_domain_host_list()
        self.data = []
        self.result = []

    def _get_domain_host_list(self):
        return self.xns.domain_host_list(self.domain_id)['hosts']

    def _get_record_list(self, host_id):

        status = False
        for i in range(1, 6):
            record = self.xns.domain_host_record_list(self.domain_id, host_id=host_id)
            if record.get('data'):
                status = True
                break
            else:
                time.sleep(1)
                logger.warning(f'CLOUDXNS 請求錯誤 重試第{i}次 Domainid: {self.domain_id} host_id: {host_id}')

        if not status:
            raise Exception(f'CLOUDXNS 多次請求錯誤 Domainid: {self.domain_id} host_id: {host_id}')

        data = record['data']
        # print('get_record_list', record)
        return data[0] if isinstance(data, list) else data

    def filter_host(self, name):
        data = [i for i in self._data if re.match(f'{name}', i['host'])]
        self.data = self.data + data
        return data

    def filter_site(self, name):
        data = [i for i in self._data if re.match(f'.*{name}[^\d].*', i['host'])]
        self.data = self.data + data
        return data

    def get_record_list(self):

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self._get_record_list, d['id']) for d in self.data]
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    # print(result)
                    self.result.append(result)
                except Exception as exc:
                    print('generated an exception: %s' % (exc))


class FilterRecord:

    def __init__(self, CLOUDXNS):
        self.xns = CLOUDXNS

    def filter_site_xns(self, domain_id_list, namelist):
        result = []

        for domain_id in domain_id_list:
            xns = XNSRecord(CLOUDXNS=self.xns,domain_id=domain_id)
            for name in namelist:
                xns.filter_site(name=name)
            xns.get_record_list()
            result = result + xns.result

        return result

    def filter_name_xns(self, domain_id_list, namelist):
        result = []

        for domain_id in domain_id_list:
            xns = XNSRecord(CLOUDXNS=self.xns, domain_id=domain_id)
            for name in namelist:
                xns.filter_host(name=name)
            xns.get_record_list()
            result = result + xns.result

        return result



