class Parser:
    """
    To handle text formatting and converting problems.

    #######################
    ### CAMEL and SNAKE ###
    #######################
    >>> Parser.camel2snake('MyModelName', delimiter=0)
    Traceback (most recent call last):
        ...
    TypeError: Invalid type, text and delimiter must be str.

    >>> Parser.snake2camel(None, delimiter='_')
    Traceback (most recent call last):
        ...
    TypeError: Invalid type, text and delimiter must be str.
    """
    @staticmethod
    def snake2camel(text, delimiter='_'):
        """
        :param text: snake string
        :type text: str
        :param delimiter: specify unusual split symbol
        :type delimiter: str
        :return: formatted as camel
        >>> Parser.snake2camel('my_model_name')
        'MyModelName'
        >>> Parser.snake2camel('maybe0like0this', delimiter='0')
        'MaybeLikeThis'
        >>> Parser.snake2camel('orlikethis')
        'Orlikethis'
        """
        if not (isinstance(text, str) and isinstance(delimiter, str)):
            raise TypeError('Invalid type, text and delimiter must be str.')
        if delimiter not in text:
            return text.title()
        return ''.join(_.title() for _ in text.split(delimiter))

    @staticmethod
    def camel2snake(text, delimiter='_'):
        """
        :param text: camel string
        :type text: str
        :param delimiter: specify unusual split symbol
        :type delimiter: str
        :return: formatted as snake
        >>> Parser.camel2snake('MyModelName')
        'my_model_name'
        >>> Parser.camel2snake('HowAboutThis', delimiter='-')
        'how-about-this'
        """
        if not (isinstance(text, str) and isinstance(delimiter, str)):
            raise TypeError('Invalid type, text and delimiter must be str.')
        if text.islower():
            return text
        result = ''.join(f'{delimiter}{_.lower()}' if _.isupper() else _ for _ in text)
        return result.lstrip(delimiter)

