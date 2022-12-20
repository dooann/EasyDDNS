import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.request import CommonRequest
from modules.config import Config
from modules.domain import Domain

class Client:

    # Private variables for reuse.
    __client = None
    
    def __init__(self, config: Config) -> None:
        '''
            Initialize private variables
        '''
        self.__client = AcsClient(config.access_key, config.access_key_secret)

    def update_record(self, domain: Domain) -> None:
        '''
            Request for update DNS record.
        '''
        try:
            # Construct a request for update
            request = self.__create_request()
            request.set_action_name('UpdateDomainRecord')
            # if not hasattr(domain, 'record_id'):
            if domain.record_id is None:
                self.__query_record_id(domain)
            request.add_query_param('RecordId', domain.record_id)
            request.add_query_param('RR', domain.subdomain_name)
            request.add_query_param('Type', domain.type)
            request.add_query_param('Value', domain.ip)
            self.__client.do_action_with_exception(request)
        except (ServerException, ClientException) as e:
            error_code = e.get_error_code()
            if error_code == 'DomainRecordDuplicate':
                pass
            elif error_code == 'DomainRecordNotBelongToUser':
                self.add_record(domain)
                self.update_record(domain)
            else:
                domain.ip = None
                raise e
        finally:
            del request

    def add_record(self, domain: Domain) -> None:
        '''
            Request for add a DNS record.
        '''
        request = self.__create_request()
        request.set_action_name('AddDomainRecord')
        request.add_query_param('DomainName', domain.domain_name)
        request.add_query_param('RR', domain.subdomain_name)
        request.add_query_param('Type', domain.type)
        request.add_query_param('Value', domain.ip)
        self.__client.do_action_with_exception(request)
    
    def __create_request(self) -> CommonRequest:
        '''
            Return a request.
        '''
        request = CommonRequest()
        request.set_domain('alidns.aliyuncs.com')
        request.set_version('2015-01-09')
        return request

    def __query_record_id(self, domain: Domain) -> None:
        '''
            Request for query the record id for domain.
        '''
        try:
            request = self.__create_request()
            request.set_action_name('DescribeDomainRecords')
            request.add_query_param('DomainName', domain.domain_name)
            request.add_query_param('KeyWord', domain.subdomain_name)
            response = self.__client.do_action_with_exception(request)
            records = json.loads(response)['DomainRecords']['Record']
            for record in records:
                if record['RR'] == domain.subdomain_name \
                and record['DomainName'] == domain.domain_name:
                    domain.record_id = record['RecordId']
                    return
        finally:
            del request


