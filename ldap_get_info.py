from ldap3 import Server, Connection, ALL
import argparse
import json
import os


def get_args():
    parser = argparse.ArgumentParser(description='Get users info from LDAP server.')
    parser.add_argument('--host', help='IP or Host name', type=str, required=True)
    parser.add_argument('--port', help='Port number', type=str, required=True)
    parser.add_argument('--user', help='User DN', type=str, required=True)
    parser.add_argument('--pass', help='Password', type=str, required=True)
    parser.add_argument('--base', help='LDAP base ex. dc=example,dc=com"', type=str, required=True)
    args = vars(parser.parse_args())
    return args


def write_connection_info(conn):
    file_path = 'results/connection_info.txt'
    with open(file_path, 'w') as f:
        print(conn, file=f)
    print(f'>>> write connection info to "{file_path}"')


def write_bind_result(result, bind_success):
    file_path = 'results/bind_result.json'
    with open(file_path, 'w') as f:
        json.dump(result, f, indent=2)
    if bind_success:
        print(f'>>> bind success, write bind result to "{file_path}"')
    else:
        print(f'>>> bind failed, write bind result to "{file_path}"')


def write_server_info(server: Server, conn):
    file_path = 'results/server_info.json'
    server.info.to_file(file_path)
    print(f'>>> write server info to "{file_path}"')

    file_path = 'results/server_schema.json'
    server.schema.to_file(file_path)
    print(f'>>> write server schema to "{file_path}"')


def write_users_info(conn):
    file_path = 'results/users_info.txt'
    with open(file_path, 'w') as f:
        print(f'\n=== users, found {len(conn.entries)} ===', file=f)
        for entry in conn.entries:
            print(entry, file=f)
    print(f'>>> write users info to "{file_path}"')


def create_output_dir():
    dir_path = './results'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    

def main():
    create_output_dir()
    
    args = get_args()

    LDAP_HOST = args['host']
    LDAP_PORT = int(args['port'])
    LDAP_USER = args['user']
    LDAP_PASSWORD = args['pass']
    
    SEARCH_BASE = args['base']
    SEARCH_FILTER = '(|(objectclass=person)(objectcategory=user))'
    # SEARCH_FILTER = '(objectclass=person)'
    SEARCH_ATTRIBUTES = '*'
    SEARCH_SIZE_LIMIT = 100

    server = Server(LDAP_HOST, LDAP_PORT, get_info=ALL)

    conn = Connection(
        server, 
        LDAP_USER, 
        LDAP_PASSWORD, 
        auto_bind=False,
        raise_exceptions=False,
    )
    conn.open()
    print(f'>>> connect success')
    write_connection_info(conn)

    bind_success = conn.bind()
    write_bind_result(conn.result, bind_success)
    if not bind_success:
        return

    write_server_info(server, conn)

    conn.search(
        SEARCH_BASE, 
        SEARCH_FILTER, 
        attributes=SEARCH_ATTRIBUTES, 
        size_limit=SEARCH_SIZE_LIMIT,
    )
    print(f'>>> search success found {len(conn.entries)}')
    write_users_info(conn)

    conn.unbind()


if __name__ == '__main__':
    main()