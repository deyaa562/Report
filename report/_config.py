import argparse
from . import _internal

def config():
    parser = argparse.ArgumentParser(description='Pytest Report Portal Wrapper')
    parser.add_argument('--host', '-H', default='localhost', help='host:ip or domain name (Example: localhost:8080)')
    parser.add_argument('--launch-name', '-l', default='new launch' ,help='New launch name ( default is "new launch" )')
    parser.add_argument('--bearer-uuid', '-u', required=True, help='Auth bearer UUID')
    parser.add_argument('--project-name', '-p', required=True, help='Report Portal project name')
    args = parser.parse_args()
    print(args.bearer_uuid)
    _internal.Data.endpoint = args.host
    _internal.Data.launch_name = args.launch_name 
    _internal.Data.uuid = args.bearer_uuid
    _internal.Data.project = args.project_name
    _internal.Data.update_url()
    _internal.Launch.update_headers()

    
if __name__ == '__main__':
    data = config()
    _internal.Launch.start_launch()
    
