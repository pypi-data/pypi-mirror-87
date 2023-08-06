class SavviHubError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def inheritors(klass):
    subclasses = []
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.append(child)
                work.append(child)
    return subclasses


class SavviHubInternalError(SavviHubError):
    error_code = 'InternalServerError'


class SavviHubNotADirectoryError(SavviHubError):
    error_code = 'NotADirectory'


def parse_error_code(resp):
    code = resp.json().get('code')
    message = resp.json().get('message')
    fields = resp.json().get('fields')

    for klass in inheritors(SavviHubError):
        if klass.error_code == code:
            return klass(message, fields)

    return SavviHubInternalError(resp.text)
