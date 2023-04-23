class BaseResponse:
    def __init__(self, success=True, error=None):
        self.success = success
        self.error = error

    def to_dict(self):
        return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'isBase64Encoded': False,
        'body': self.__dict__
    }
