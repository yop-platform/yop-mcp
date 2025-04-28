import sys
sys.path.append('./')
from tools.api_md_utils import ApiMdUtils
import json

# Test with a more complex API definition
test_data = {
    'title': 'Complex API',
    'apiGroup': 'test',
    'apiId': 'complex123',
    'path': '/api/complex',
    'method': 'POST',
    'type': 'JSON',
    'desc': 'Complex API description',
    'lastModifiedDate': '2023-01-01',
    'securityReqs': ['OAuth2'],
    'reqParams': {
        'application/json': [
            {
                'name': 'request',
                'title': 'Request',
                'type': 'object',
                'required': True,
                'description': 'Request object'
            }
        ]
    },
    'respParams': {
        'application/json': [
            {
                'name': 'code',
                'title': 'Code',
                'type': 'string',
                'description': 'Response code'
            },
            {
                'name': 'message',
                'title': 'Message',
                'type': 'string',
                'description': 'Response message'
            },
            {
                'name': 'data',
                'title': 'Data',
                'type': 'object',
                'description': 'Response data'
            }
        ]
    },
    'respExamples': {
        'application/json': json.dumps({
            'code': '0',
            'message': 'Success',
            'data': {
                'id': '123456',
                'status': 'active'
            }
        })
    }
}

# Test the static method
md = ApiMdUtils.convert_data_to_markdown(test_data)
print('Static Method Output:')
print(md) 