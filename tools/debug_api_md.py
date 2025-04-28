import sys
sys.path.append('./')
from tools.api_md_utils import ApiMdUtils

test_data = {
    'title': 'Test API', 
    'apiGroup': 'test', 
    'apiId': 'test123', 
    'path': '/api/test', 
    'method': 'POST', 
    'type': 'JSON', 
    'desc': 'Test description', 
    'lastModifiedDate': '2023-01-01', 
    'securityReqs': ['OAuth2'], 
    'reqParams': {
        'application/json': [
            {
                'name': 'id', 
                'title': 'ID', 
                'type': 'string', 
                'required': True, 
                'description': 'Unique identifier'
            }
        ]
    }, 
    'respParams': {}
}

def debug_convert_to_markdown():
    # Create a test instance
    utils = ApiMdUtils('dummy.json')
    utils.api_data = test_data
    
    # Debug the convert_to_markdown logic
    content = []
    content.append(f"# {utils.api_data.get('title', '未知API')}")
    content.append("")
    
    req_params = utils.api_data.get('reqParams', {})
    for content_type, params in req_params.items():
        is_json_content_type = 'json' in content_type.lower()
        print(f'Content-Type: {content_type}, is_json_content_type: {is_json_content_type}')
        
        content.append(f"### {content_type}")
        content.append("")
        
        content.append('| 参数名 | 参数说明 | 类型 | 是否必填 | 描述 |')
        content.append('| ------ | ------ | ------ | ------ | ------ |')
        
        # Test parameters
        for param in params:
            print(f'Param: {param}')
            indent_level = 0
            name = param.get('name', '')
            title = param.get('title', '')
            param_type = param.get('type', '')
            required = '是' if param.get('required', False) else '否'
            desc = param.get('description', '')
            
            print(f'indent_level: {indent_level}, is_json_content_type: {is_json_content_type}')
            print(f'Condition result: {indent_level > 0 or not is_json_content_type}')
            
            # Modified logic without the problematic condition
            content.append(f'| {name} | {title} | {param_type} | {required} | {desc} |')
    
    print("\nGenerated Markdown:")
    print('\n'.join(content))
    
    # Test the static method
    print("\nStatic method test:")
    md = ApiMdUtils.convert_data_to_markdown(test_data)
    print(md.split('### application/json')[1].split('###')[0])

# Run the debug function
debug_convert_to_markdown() 