from modules.domain import *
from modules.config import *
from modules.aliyun import *
import time

def update_domains(client: Client, config: Config):
    count = 0
    for domain in config.domains:
        domain.update()
        client.update_record(domain)
        count += 1
        print('update', domain.subdomain_name + '.' + domain.domain_name, 'record success')
    print(count, 'domain record(s) updated. ')
    config.dump('config.json')

def main():
    config = Config('config.json')

    client = Client(config)
    if config.period is not None:
        while True:
            try:
                update_domains(client, config)
            except Exception as e:
                # Do not raise exceptions because this program needs to keep running.
                print(e)
            finally:
                print('Waiting for the next performance...\n')
                time.sleep(config.period)
    else:
        update_domains(client, config)

if __name__ == "__main__":
    main()