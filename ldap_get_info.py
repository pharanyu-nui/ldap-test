from ldap3 import Server, Connection, ALL
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='Get users info from LDAP server.')
    parser.add_argument('--host', help='IP or Host name', type=str, required=True)
    parser.add_argument('--port', help='Port number', type=str, required=True)
    parser.add_argument('--user', help='Username', type=str, required=True)
    parser.add_argument('--pass', help='Password', type=str, required=True)
    parser.add_argument('--base', help='LDAP base ex. dc=example,dc=com"', type=str, required=True)
    args = vars(parser.parse_args())
    return args


def write_result(server, conn):
    with open('result.txt', 'w') as f:
        print('=== conn ===', file=f)
        print(conn, file=f)

        print('\n=== server info ===', file=f)
        print(server.info, file=f)

        print(f'\n=== people, found {len(conn.entries)} ===', file=f)
        for entry in conn.entries:
            print(entry, file=f)
    print('write data to "result.txt"')


def main():
    args = get_args()

    LDAP_HOST = args['host']
    LDAP_PORT = int(args['port'])
    LDAP_USER = args['user']
    LDAP_PASSWORD = args['pass']
    LDAP_SEARCH_BASE = args['base']
    SEARCH_SIZE_LIMIT = 100

    server = Server(LDAP_HOST, LDAP_PORT, get_info=ALL)

    conn = Connection(
        server, 
        f'cn={LDAP_USER},{LDAP_SEARCH_BASE}', 
        LDAP_PASSWORD, 
        auto_bind=False,
        raise_exceptions=True,
    )
    print(f'connect success')

    conn.bind()
    print(f'bind success')

    conn.search(
        LDAP_SEARCH_BASE, 
        '(objectclass=person)', 
        attributes='*', 
        size_limit=SEARCH_SIZE_LIMIT
    )
    print(f'search success found {len(conn.entries)}')

    write_result(server, conn)


if __name__ == '__main__':
    main()