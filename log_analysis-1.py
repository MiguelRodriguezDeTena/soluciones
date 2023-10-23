import re

from datetime import datetime
from collections import defaultdict



'''
Comentario del profesor,
Esto es una constante. El convenio de Python es que vaya todo el nombre
en mayúsculas
REGEX = .....
'''
regex = re.compile(r"""(?P<ip>\d+\.\d+\.\d+\.\d+)         #IP address
                       \s\-\s\-                           #separator
                       \s\[(?P<timestamp>.*)\]            #timestamp
                       \s\".*\"                           #request method, resource and HTTP
                       \s\d{1,3}\s\d{1,3}                 #status code
                       \s\".*\"                           #referer
                       \s(?P<user_agent>\".*\")           #user agent
                       """,re.VERBOSE)

def ipaddreses(filename: str) -> set[str]:
    '''
    Returns the IPs of the accesses that are not bots
    '''
    my_set = set()

    def is_bot(useragent: str) -> bool:
        '''
        Check of the access in the line correspons to a bot

        Examples
        --------
        >>> is_bot('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
        False

        >>> is_bot('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
        True

        >>> is_bot('213.180.203.109 - - [15/Sep/2023:00:12:18 +0200] "GET /robots.txt HTTP/1.1" 302 567 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"')
        True
        '''
        '''
        Comenario del profesor
        esta expresión regular no hace falta es una simple secuencia de letras, es más eficiente usar
        bot in useragent

        '''
        botregex = re.compile(r"(bot)")
        botsearcher = botregex.search(useragent)
        '''
        Comentario del profesor.
        Este if es un tanto redundante. Es más conciso poner
        return bool(botsearcher)
        '''
        if botsearcher:
            return True
        else:
            return False

    def get_user_agent(log: str) -> str:
        """
        Get the user agent of the line.

        Examples
        ---------
        >>> get_user_agent('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

        >>> get_user_agent('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0'
        """
        user_search = regex.search(log)
        return user_search.group("user_agent")

    with open(filename, "r") as ffile:
        file = ffile.readlines()
    for line in file:
        user = get_user_agent(line)
        if not is_bot(user):
            ip_search = regex.search(line)
            my_set.add(ip_search.group("ip"))

    return my_set

def histbyhour(filename: str) -> dict[int, int]:
    '''
    Computes the histogram of access by hour
    '''
    dict = defaultdict(int)

    def get_hour(ip: str) -> int:
        """
        Get the user agent of the line.

        Examples
        ---------
        >>> get_hour('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
        0

        >>> get_hour('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antacres.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
        12
        """
        search = regex.search(ip)
        dtobj = datetime.strptime(search.group("timestamp"),'%d/%b/%Y:%H:%M:%S %z')
        return dtobj.hour

    with open(filename, "r") as ffile:
        file = ffile.readlines()
    for line in file:
        hour = get_hour(line)
        dict[hour] += 1

    return dict


import doctest

"""
Comentario del profesor,
Anque lo de arriba está perfectamente estructurado, el problema
es que este test no lo pasa por el ámbito de las funciones.
"""
def test_doc():
    doctest.run_docstring_examples(get_user_agent, globals(), verbose=True)
    doctest.run_docstring_examples(is_bot, globals(), verbose=True)
    doctest.run_docstring_examples(get_hour, globals(), verbose=True)


def test_ipaddresses():
    assert ipaddreses('access_short.log') == {'34.105.93.183', '39.103.168.88'}

def test_hist():
    hist = histbyhour('access_short.log')
    assert hist == {5: 3, 7: 2, 23: 1}

if __name__ == '__main__':
    test_doc()
    test_ipaddresses()
    test_hist()
