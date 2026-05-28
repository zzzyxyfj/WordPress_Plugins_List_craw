#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import urllib.error
import re
import argparse
import sys
import os

def get_plugin_list(url):
    """
    爬取 WordPress SVN 插件列表
    """
    try:
        # 设置请求头，模拟浏览器访问
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"正在连接到: {url} ...")
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as response:
            # 检查 HTTP 状态码
            if response.getcode() != 200:
                raise urllib.error.HTTPError(url, response.getcode(), f"HTTP 错误: {response.getcode()}", headers, None)
            
            print("正在下载并解析页面内容 (由于插件数量庞大，可能需要几十秒)...")
            # 网页非常大（约 3MB+），一次性读取
            html_content = response.read().decode('utf-8')
        
        plugins = []
        
        # 匹配 <a href="plugin-name/">plugin-name/</a> 这种最常见的格式
        # 提取 <a> 标签的文本内容，并去除末尾的斜杠
        matches = re.findall(r'<a[^>]*>(.*?)/</a>', html_content)
        for match in matches:
            # 排除掉 ".." (返回上级目录) 和其他非插件目录的链接
            if match and match != '..' and not match.startswith('.'):
                plugins.append(match.rstrip('/'))

        # 最终去重并排序
        unique_plugins = sorted(list(set(plugins)))
        print(f"解析完成，共找到 {len(unique_plugins)} 个插件。")
        return unique_plugins

    except urllib.error.URLError as e:
        if isinstance(e.reason, ConnectionRefusedError):
            print("错误: 无法连接到服务器。请检查您的网络连接或 URL 是否正确。")
        elif isinstance(e.reason, TimeoutError):
            print("错误: 请求超时。服务器响应过慢，请稍后重试。")
        else:
            print(f"错误: URL 错误 - {e.reason}")
        sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"错误: HTTP 请求失败 (状态码: {e.code})。详细信息: {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"发生未知错误: {e}")
        sys.exit(1)

def save_to_file(plugins, filename):
    """
    将插件列表保存到 txt 文件
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for plugin in plugins:
                f.write(f"{plugin}\n")
        print(f"成功保存 {len(plugins)} 个插件到文件: {filename}")
    except IOError as e:
        print(f"错误: 写入文件时发生 I/O 错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 无法保存文件: {e}")
        sys.exit(1)

def main():
    # 创建参数解析器，并设置自定义的帮助信息
    parser = argparse.ArgumentParser(
        description="WordPress 插件列表爬取工具 - 用于从 SVN 仓库获取插件目录名",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False, # 禁用默认帮助以自定义
        epilog="""
用法示例 (在 Windows 命令提示符或 PowerShell 中):
  python wp_plugin_crawler_final.py                       # 使用默认设置爬取并保存为 plugins.txt
  python wp_plugin_crawler_final.py -o my_plugins.txt     # 指定输出文件名
  python wp_plugin_crawler_final.py -u https://example.com # 指定爬取的 URL

注意: 本程序无需安装任何第三方库，下载后即可直接运行。
        """
    )

    group = parser.add_argument_group("可选参数")
    group.add_argument("-h", "--help", action="help", help="显示此帮助信息并退出")
    group.add_argument(
        "-u", "--url", 
        default="https://plugins.svn.wordpress.org/", 
        help="目标 WordPress SVN 地址 (默认为: https://plugins.svn.wordpress.org/)"
    )
    group.add_argument(
        "-o", "--output", 
        default="plugins.txt", 
        help="保存的 txt 文件名称 (默认为: plugins.txt)"
    )

    # 如果没有参数或者请求帮助
    if len(sys.argv) == 1:
        # 默认执行，不打印帮助
        pass

    args = parser.parse_args()

    # 执行爬取
    plugins = get_plugin_list(args.url)
    
    if plugins:
        save_to_file(plugins, args.output)
    else:
        print("警告: 未找到任何插件。请检查目标页面结构是否发生变化。")

if __name__ == "__main__":
    main()
