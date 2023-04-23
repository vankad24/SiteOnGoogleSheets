class BaseResponse:
    def __init__(self, success=True, error=None):
        self.body = {"success": success,
                     "error":None if error is None else error.to_dict()}

    def to_dict(self):
        return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'isBase64Encoded': False,
        'body': self.body
    }
