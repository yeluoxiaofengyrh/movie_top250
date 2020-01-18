from utils import log, get_text
from request_and_response import get


def get_movie_info(body):
    body_line = body.split('\n')
    it = iter(body_line)
    lists = []
    count = 1
    name, grade, review_num, quote = '', '', '', ''
    while True:
        try:
            line = next(it)
            if 'class="title"' in line:
                name = get_text(line)
                next(it)
                count += 1
            elif 'class="rating_num"' in line:
                grade = get_text(line)
                next(it)
                line = next(it)
                review_num = get_text(line)
                count += 2
            elif 'class="inq"' in line:
                quote = get_text(line)
                count += 1
        except StopIteration:
            # 遇到StopIteration就退出循环
            break
        if count % 5 == 0:
            item = [name, grade, review_num, quote]
            count = 1
            lists.append(item)
    return lists


def main():
    url = 'http://movie.douban.com/top250'
    for i in range(10):
        index = i*25
        query = {
            'start': index
        }
        status_code, headers, body = get(url, **query)
        # log('main', status_code)
        # log('main headers ({})'.format(headers))
        # log('main body', body)
        lists = get_movie_info(body)
        for each in lists:
            log(each)


if __name__ == '__main__':
    main()
