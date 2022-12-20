import json
import urllib.request as request

class Domain:

    domain_name = None
    subdomain_name = None
    type = None
    ip = None
    query_url = None
    record_id = None

    def __init__(
        self, 
        domain_name: str,
        subdomain_name: str=None,
        type: str='AAAA',
        ip: str=None,
        query_url: str=None
    ):
        '''
           Construct a Domain instance. 
        '''
        type = type.upper()
        if type not in ('AAAA', 'A'):
            raise AttributeError('Invalid value for type: ', type)
        self.type = type
        self.domain_name = domain_name
        self.subdomain_name = subdomain_name if subdomain_name else '@'
        self.ip = ip
        self.query_url = query_url
    
    def update(self):
        api_url = None
        if self.query_url:
            api_url = self.query_url
        else:
            if self.type == 'AAAA':
                api_url = 'https://api6.ipify.org/'
            elif self.type == 'A':
                api_url = 'https://api4.ipify.org/'
        response = request.urlopen(api_url)
        current_ip = response.read().decode('utf-8')
        if current_ip:
            self.ip = current_ip
            return True
        else:
            raise 

class DomainEncoder(json.JSONEncoder):
    def default(self, obj: Domain) -> dict:
        if isinstance(obj, Domain):
            domain = {
                'domain_name': obj.domain_name,
                'subdomain_name': obj.subdomain_name,
                'type': obj.type
            }
            if hasattr(obj, 'ip') and obj.ip:
                domain['ip'] = obj.ip
            if hasattr(obj, 'ip') and obj.query_url:
                domain['query_url'] = obj.query_url
            return domain
        # Let the base class default method raise the TypeError
        return super().default(obj)