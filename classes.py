class Response():
    '''
    HTML response container.

    Attributes:
    - headers (str): HTML headers response.
    - html (str): HTML code response.
    '''

    def __init__(self, headers: str, html: str) -> None:
        '''
        Response initializer.

        Args:
        - headers (str): HTML headers response.
        - html (str): HTML code response.
        '''
        self.__headers = headers
        self.__html = html

    def get_headers(self):
        '''
        Gets headers attribute.
        '''
        return self.__headers

    def get_html(self):
        '''
        Gets html attribute.
        '''
        return self.__html
