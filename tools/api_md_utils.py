#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import argparse
from typing import Dict, List, Any, Optional
from tools.http_utils import HttpUtils


class ApiMdUtils:
    """
    工具类，用于将API的JSON定义文件转换为Markdown格式的文档
    """

    def __init__(self, json_file_path: str, output_dir: Optional[str] = None):
        """
        初始化转换器
        
        Args:
            json_file_path: JSON文件路径
            output_dir: 输出目录路径，默认与JSON文件位于同一目录
        """
        self.json_file_path = json_file_path
        self.output_dir = output_dir or os.path.dirname(json_file_path)
        self.api_data = None

    @staticmethod
    def convert_data_to_markdown(api_data: Dict[str, Any]) -> str:
        """
        将API数据直接转换为Markdown格式
        
        Args:
            api_data: API数据字典
            
        Returns:
            str: 生成的Markdown内容
        """
        # 创建一个临时实例以复用逻辑
        utils = ApiMdUtils("dummy.json")
        utils.api_data = api_data
        
        # 由于这是静态方法，我们需要确保_processed_refs属性被正确初始化
        if not hasattr(utils, '_processed_refs'):
            utils._processed_refs = set()
            
        return utils.convert_to_markdown()

    def load_json(self) -> Dict[str, Any]:
        """
        从JSON文件加载API数据
        
        Returns:
            Dict[str, Any]: 加载的API数据
        """
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                self.api_data = json.load(file)
                return self.api_data
        except Exception as e:
            raise Exception(f"加载JSON文件失败: {str(e)}")
        
    def fetch_model_json(self, ref_name: str, api_group: str) -> List[Dict[str, Any]]:
        """
        从API定义中获取模型JSON
        
        Args:
            ref_name: 模型引用名称  
            api_group: API分组
        
        Returns:
            List[Dict[str, Any]]: 模型JSON数据
        """
        try:
            model_url = "https://open.yeepay.com/apis/docs/models/" + api_group + "/" + ref_name + ".json"
            model_content = HttpUtils.sync_download(model_url)
            if model_content and not model_content.startswith("错误:"):
                try:
                    modelJson = json.loads(model_content)
                    print(f"成功获取并解析模型: {ref_name}")    
                    return modelJson
                except json.JSONDecodeError as je:
                    print(f"模型JSON解析失败: {ref_name}, 错误: {str(je)}")
                    return []
            else:
                print(f"获取模型失败: {ref_name}, 响应: {model_content}")   
        except Exception as e:
            print(f"处理模型时发生异常: {ref_name}, 错误: {str(e)}")
            return []
    

    def convert_to_markdown(self) -> str:
        """
        将API数据转换为Markdown格式
        
        Returns:
            str: 生成的Markdown内容
        """
        if not self.api_data:
            self.load_json()

        content = []

        # 添加标题
        content.append(f"# {self.api_data.get('title', '未知API')}")
        content.append("")

        # 基本信息
        api_group = self.api_data.get('apiGroup', '')
        api_id = self.api_data.get('apiId', '')
        content.append("## 基本信息")
        content.append("")
        content.append(f"- **API ID**: {api_id}")
        content.append(f"- **API 分组**: {api_group}")
        content.append(f"- **请求路径**: `{self.api_data.get('path', '')}`")
        content.append(f"- **请求方法**: {self.api_data.get('method', '')}")
        content.append(f"- **类型**: {self.api_data.get('type', '')}")
        
        security_reqs = self.api_data.get('securityReqs', [])
        if security_reqs:
            content.append(f"- **安全需求**: {', '.join(security_reqs)}")
        
        content.append(f"- **描述**: {self.api_data.get('desc', '')}")
        content.append(f"- **最后更新时间**: {self.api_data.get('lastModifiedDate', '')}")
        content.append("")

        # 添加参数行的公共函数
        def add_param_row(param, indent_level=0, is_json_content_type=True, is_response=False):
            param_type = param.get('type', '')
            name = param.get('name', '')
            title = param.get('title', '')
            required = "是" if param.get('required', False) else "否"
            desc = param.get('description', '')
            desc = desc.replace('\n', '<br>')
            
            # 添加缩进前缀
            indent_prefix = '&nbsp;&nbsp;' * (indent_level - 1)
            if indent_level > 1:
                name = f"{indent_prefix}└─ {name}"
            # Always add the parameter to the table
            if indent_level > 0 or not is_json_content_type or param_type not in ['object', 'array']:
                if is_response:
                    content.append(f"| {name} | {title} | {param_type} | {desc} |")
                else:
                    content.append(f"| {name} | {title} | {param_type} | {required} | {desc} |")
            # 处理嵌套对象
            if param_type == 'object' and 'ref' in param:
                # 防止循环引用，记录已处理的引用
                processed_refs = getattr(self, '_processed_refs', set())
                ref_name = param.get('ref', '')
                
                # 检查是否已处理过该引用，避免循环引用导致无限递归
                if ref_name in processed_refs:
                    content.append(f"| {name}[循环引用] | 已在上方定义 | {param_type} | - | 循环引用到 {ref_name} |")
                    return
                
                # 添加到已处理引用集合
                if not hasattr(self, '_processed_refs'):
                    self._processed_refs = set()
                self._processed_refs.add(ref_name)
                
                api_group = self.api_data.get('apiGroup', '')
                modelJson = self.fetch_model_json(ref_name, api_group)
                
                # 处理子参数
                for child in modelJson:
                    add_param_row(child, indent_level + 1, is_json_content_type, is_response)
                
                # 处理完成后，从已处理集合中移除，允许在其他地方使用相同引用
                self._processed_refs.remove(ref_name)
            
            # 处理数组类型
            elif param_type == 'array' and 'ref' in param:
                api_group = self.api_data.get('apiGroup', '')
                modelJson = self.fetch_model_json(param.get('ref', ''), api_group)
                # 处理子参数
                for child in modelJson:
                    add_param_row(child, indent_level + 1, is_json_content_type, is_response)
            
            # 处理数组类型
            elif param_type == 'array' and 'ref' not in param:
                items = param.get('items', {})
                items_type = items.get('type', 'string')
                items_name = f"{name}[元素]"
                items_desc = items.get('description', '数组元素')
                
                # 添加数组元素行
                content.append(f"| {indent_prefix}&nbsp;&nbsp;└─ {items_name} | 数组元素 | {items_type} | - | {items_desc} |")

        # 请求参数
        req_params = self.api_data.get('reqParams', {})
        if req_params:
            content.append("## 请求参数")
            content.append("")
            
            for content_type, params in req_params.items():
                # 如果有多种content_type，只处理JSON类型的参数
                is_json_content_type = 'json' in content_type.lower()
                if len(req_params) > 1 and not is_json_content_type:
                    continue
                content.append(f"### {content_type}")
                content.append("")
                
                if params:
                    # 创建表头
                    content.append("| 参数名 | 参数说明 | 类型 | 是否必填 | 描述 |")
                    content.append("| ------ | ------ | ------ | ------ | ------ |")
                    
                    # 处理所有参数
                    for param in params:
                        add_param_row(param, is_json_content_type=is_json_content_type)
                
                content.append("")

            # 添加请求参数示例
            content.append("### 请求参数示例")
            content.append("")
            
            # 获取有example字段的参数进行示例展示
            for content_type, params in req_params.items():
                for param in params:
                    if 'example' in param and param.get('example') and not param.get('required', False):
                        name = param.get('name', '')
                        title = param.get('title', '')
                        example = param.get('example', '')
                        
                        # 尝试解析JSON示例
                        try:
                            # 如果是字符串形式的JSON，则格式化显示
                            if isinstance(example, str) and (example.startswith('{') or example.startswith('[')):
                                try:
                                    formatted_example = json.dumps(json.loads(example), indent=2, ensure_ascii=False)
                                except Exception as e:
                                    print(f"Error formatting JSON example for {name}: {e}")
                                    formatted_example = example
                                content.append(f"#### {name}（{title}）")
                                content.append("```json")
                                content.append(formatted_example)
                                content.append("```")
                            else:
                                content.append(f"#### {name}（{title}）")
                                content.append("```")
                                content.append(str(example))
                                content.append("```")
                        except:
                            # 如果解析失败，则直接显示原始内容
                            content.append(f"#### {name}（{title}）")
                            content.append("```")
                            content.append(str(example))
                            content.append("```")
                        
                        content.append("")

        # 响应参数
        resp_params = self.api_data.get('respParams', {})
        if resp_params:
            content.append("## 响应参数")
            content.append("")
            
            for content_type, params in resp_params.items():
                is_json_content_type = 'json' in content_type.lower()
                content.append(f"### {content_type}")
                content.append("")
                
                if params:
                    # 创建表头
                    content.append("| 参数名 | 参数说明 | 类型 | 描述 |")
                    content.append("| ------ | ------ | ------ | ------ |")
                    
                    # 处理所有参数
                    for param in params:
                        add_param_row(param, 0, is_json_content_type, is_response=True)
                
                content.append("")

            # 添加响应示例
            resp_examples = self.api_data.get('respExamples', {})
            if resp_examples:
                for content_type, example in resp_examples.items():
                    if example:
                        content.append("### 响应示例")
                        try:
                            # 尝试解析JSON示例
                            if isinstance(example, str) and (example.startswith('{') or example.startswith('[')):
                                try:
                                    formatted_example = json.dumps(json.loads(example), indent=2, ensure_ascii=False)
                                except Exception as e:
                                    print(f"Error formatting JSON example for {name}: {e}")
                                    formatted_example = example
                                content.append("```json")
                                content.append(formatted_example)
                                content.append("```")
                            else:
                                content.append("```")
                                content.append(str(example))
                                content.append("```")
                        except:
                            # 如果不是有效的JSON，直接输出
                            content.append("```")
                            content.append(str(example))
                            content.append("```")
                        
                        content.append("")
            else:
                # 如果没有响应示例，生成一个基于响应参数的示例
                content.append("### 响应示例")
                content.append("```json")
                example_response = {}
                content.append(json.dumps(example_response, indent=2, ensure_ascii=False))
                content.append("```")
                content.append("")

        # 示例代码
        sample_codes = self.api_data.get('sampleCodes', {})
        if sample_codes:
            content.append("## 示例代码")
            content.append("")
            if "JAVA" in sample_codes and "JAVA_COMMON" in sample_codes:
                sample_codes.pop("JAVA")
            
            if "PHP" in sample_codes:
                sample_codes.pop("PHP")
            
            for language, code in sample_codes.items():
                language_name = language.split('_')[0]
                if code:
                    content.append(f"### {language_name}")
                    content.append("```" + language_name.lower())
                    content.append(code)
                    content.append("```")
                    content.append("")
            
            # 如果有多种语言的示例代码，但前面只展示了Java
            if len(sample_codes) > 1:
                content.append("### 更多语言示例")
                content.append("")
                content.append("可查看原始API定义文档获取Python、PHP、C#、Go等其他语言的实现示例。 ")

        return "\n".join(content)

    def save_to_file(self, markdown_content: str) -> str:
        """
        将Markdown内容保存到文件
        
        Args:
            markdown_content: 要保存的Markdown内容
            
        Returns:
            str: 保存的文件路径
        """
        # 创建输出目录（如果不存在）
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 构建输出文件路径
        filename = os.path.basename(self.json_file_path)
        output_file_path = os.path.join(self.output_dir, filename.replace('.json', '.md'))
        
        # 写入文件
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
        
        return output_file_path

    def convert(self) -> str:
        """
        执行完整的转换过程
        
        Returns:
            str: 保存的文件路径
        """
        self.load_json()
        markdown_content = self.convert_to_markdown()
        return self.save_to_file(markdown_content)


def main():
    """
    命令行入口函数
    """
    parser = argparse.ArgumentParser(description='将API的JSON定义文件转换为Markdown格式')
    parser.add_argument('json_file', help='API的JSON定义文件路径')
    parser.add_argument('-o', '--output-dir', help='输出目录路径（默认与JSON文件位于同一目录）')
    
    args = parser.parse_args()
    
    try:
        converter = ApiMdUtils(args.json_file, args.output_dir)
        output_file = converter.convert()
        print(f"转换成功，Markdown文件保存在: {output_file}")
    except Exception as e:
        print(f"转换失败: {str(e)}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main()) 