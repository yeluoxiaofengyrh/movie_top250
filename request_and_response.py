import socket
import ssl
from parsed_url import parsed_url


# 根据协议返回一个 socket 实例
def socket_by_protocol(protocol):
    if protocol == 'https':
        s = ssl.wrap_socket(socket.socket())
    else:
        s = socket.socket()
    return s


# 参数是一个 socket 实例, 返回这个 socket 读取的所有数据
def response_by_socket(s):
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        response += r
    return response


# 把 response 解析出 状态码_int headers_dict body_str 返回
def parsed_response(r):
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = int(h[0].split()[1])

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v
    return status_code, headers, body


def path_with_query(path, **query):
    if not query:
        return path
    query = dict([(x, str(y)) for x, y in query.items()])
    querykeys = list(query.keys())
    route = path + '?' + querykeys[0] + '=' + query[querykeys[0]]
    for key in querykeys[1:]:
        route += '&' + key + '=' + query[key]
    return route


# 把向服务器发送 HTTP 请求并且获得数据这个过程封装成函数
def get(url, **query):
    protocol, host, port, path = parsed_url(url)
    path = path_with_query(path, **query)
    s = socket_by_protocol(protocol)
    s.connect((host, port))

    encoding = 'utf-8'
    request = 'GET {} HTTP/1.1\r\nhost:{}\r\nConnection: close\r\n\r\n'.format(path, host)
    s.send(request.encode(encoding))

    response = response_by_socket(s)
    r = response.decode(encoding)

    status_code, headers, body = parsed_response(r)

    if status_code in [301, 302]:
        url = headers['Location']
        return get(url)

    return status_code, headers, body
