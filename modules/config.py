import json
from modules.domain import *

class Config:

    access_key = None
    access_key_secret = None
    domains = []
    period = None                       # Execute update task per `period` seconds 

    def __init__(self, path: str) -> None:
        with open(path, 'r') as file:
            config = json.load(file)
            self.access_key = config['access_key']
            self.access_key_secret = config['access_key_secret']
            self.period = config['period'] if config.get('period') else None

            for domain_dict in config['domains']:
                domain = Domain(
                    domain_dict['domain_name']
                )
                if 'subdomain_name' in domain_dict:
                    domain.subdomain_name = domain_dict['subdomain_name']
                if 'type' in domain_dict:
                    domain.type = domain_dict['type']
                if 'ip' in domain_dict:
                    domain.ip = domain_dict['ip']
                if 'query_url' in domain_dict:
                    domain.query_url = domain_dict['query_url']
                self.domains.append(domain)
        
    def dump(self, path):
        with open(path, 'w') as file:
            json.dump(self, file, cls=ConfigEncoder, indent=4)
            

class ConfigEncoder(json.JSONEncoder):
    def default(self, obj: Config) -> dict:
        if isinstance(obj, Config):
            config = {
                'access_key': obj.access_key,
                'access_key_secret': obj.access_key_secret,
                'domains': []
            }
            if obj.period is not None:
                config['period'] = obj.period

            if len(obj.domains)>0:
                encoder = DomainEncoder()
                for domain in obj.domains:
                    config['domains'].append(encoder.default(domain))
            return config
        # Let the base class default method raise the TypeError
        return super().default(obj)