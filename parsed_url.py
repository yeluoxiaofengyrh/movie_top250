"""
url 是字符串, 可能的值如下
'g.cn'
'g.cn/'
'g.cn:3000'
'g.cn:3000/search'
'http://g.cn'
'https://g.cn'
'http://g.cn/'
"""

# 1 返回代表协议的字符串, 'http' 或者 'https'
def protocol_of_url(url):
    protocol = 'http'
    try:
        protocol, other = url.split('://')
    except ValueError:
        pass
    return protocol


# 2 返回代表主机的字符串, 比如 'g.cn'
def host_of_url(url):
    u = url
    try:
        protocol, u = u.split('://')
    except ValueError:
        pass
    try:
        u, path = u.split('/', 1)
    except ValueError:
        pass
    try:
        u, port = u.split(':', 1)
    except ValueError:
        pass
    return u


# 3 返回代表端口的字符串, 比如 '80'
def port_of_url(url):
    u = url
    try:
        protocol, u = u.split('://')
    except ValueError:
        pass
    try:
        u, path = u.split('/', 1)
    except ValueError:
        pass
    try:
        host, u = u.split(':', 1)
    except ValueError:
        protocol = protocol_of_url(url)
        if protocol == 'https':
            u = 443
        else:
            u = 80
    return u


# 4 返回代表路径的字符串, 比如 '/' 或者 '/search'
def path_of_url(url):
    u = url
    try:
        protocol, u = u.split('://')
    except ValueError:
        pass
    try:
        u, path = u.split('/', 1)
    except ValueError:
        path = ''
    return '/' + path


# 5 返回一个 tuple, 内容如下 (protocol, host, port, path)
def parsed_url(url):
    protocol = protocol_of_url(url)
    host = host_of_url(url)
    port = port_of_url(url)
    path = path_of_url(url)
    return protocol, host, port, path
