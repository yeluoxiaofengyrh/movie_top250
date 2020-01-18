#from parsed_url import parsed_url
from request_and_response import get, parsed_response
from utils import log

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
    return int(u)


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


def test_parsed_url():
    """
    parsed_url 函数很容易出错, 所以我们写测试函数来运行看检测是否正确运行
    """
    http = 'http'
    https = 'https'
    host = 'g.cn'
    path = '/'
    test_items = [
        ('http://g.cn', (http, host, 80, path)),
        ('http://g.cn:90', (http, host, 90, path)),
        ('https://g.cn', (https, host, 443, path)),
        ('https://g.cn:233/', (https, host, 233, path)),
    ]
    for t in test_items:
        url, expected = t
        u = parsed_url(url)
        # assert 是一个语句, 名字叫 断言
        # 如果断言成功, 条件成立, 则通过测试
        # 否则为测试失败, 中断程序报错
        e = "parsed_url ERROR, ({}) ({}) ({})".format(url, u, expected)
        assert u == expected, e


def test_parsed_response():
    response = 'HTTP/1.1 301 Moved Permanently\r\n' \
               'Content-Type: text/html\r\n' \
               'Location: https://movie.douban.com/top250\r\n' \
               'Content-Length: 178\r\n\r\n' \
               'test body'
    status_code, header, body = parsed_response(response)
    assert status_code == 301
    assert len(list(header.keys())) == 3
    assert body == 'test body'


def test_get():
    urls = [
        'http://movie.douban.com/top250',
        'https://movie.douban.com/top250',
    ]
    for u in urls:
        get(u)


def test():
    test_parsed_url()
    test_get()
    test_parsed_response()


if __name__ == '__main__':
    test()
