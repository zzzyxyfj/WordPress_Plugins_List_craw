# WordPress_Plugins_List_craw

爬取wordpress的插件列表用于道德渗透测试中枚举wordpress插件

# WordPress 插件列表爬取工具

这是一个简单而高效的 Python 脚本，用于从 WordPress SVN 仓库 (`https://plugins.svn.wordpress.org/`) 爬取所有可用的插件目录名称，并将其保存到文本文件中。本工具旨在提供一个无需额外依赖、开箱即用的解决方案，方便开发者和用户快速获取 WordPress 插件列表。

## ✨ 特性

*   **零依赖**：仅使用 Python 标准库 (`urllib.request`, `re`, `argparse`, `sys`, `os`)，无需安装任何第三方库（如 `beautifulsoup4`）。下载后即可直接运行。
*   **全中文支持**：所有命令行帮助信息、进度提示和错误信息均为中文，方便中文用户使用。
*   **鲁棒的错误处理**：内置了网络连接错误、请求超时、HTTP 状态错误以及文件写入错误的捕获和处理机制，确保程序稳定运行。
*   **灵活的参数配置**：支持自定义目标 URL 和输出文件名。
*   **Windows 友好**：用法示例已针对 Windows 命令行环境进行优化。

## 🚀 如何使用

### 前提条件

确保您的系统已安装 Python 3.x 版本。

### 运行脚本

1.  将 `wp_plugin_crawler_final.py` 文件下载到您的本地计算机。

2.  打开命令行工具（在 Windows 上是 `CMD` 或 `PowerShell`）。

3.  导航到脚本所在的目录。

4.  运行以下命令：

    *   **查看帮助信息**：

        ```bash
        python wp_plugin_crawler_final.py -h
        ```

    *   **使用默认设置运行** (爬取 `https://plugins.svn.wordpress.org/` 并保存到 `plugins.txt`)：

        ```bash
        python wp_plugin_crawler_final.py
        ```

    *   **指定输出文件名**：

        ```bash
        python wp_plugin_crawler_final.py -o my_custom_plugins.txt
        ```

    *   **指定目标 URL** (例如，如果您想爬取其他 SVN 仓库)：

        ```bash
        python wp_plugin_crawler_final.py -u https://example.com/svn/plugins/ -o example_plugins.txt
        ```

### 注意事项

*   由于 WordPress 插件数量庞大（超过 11 万个），程序在下载和解析页面内容时可能需要几十秒到几分钟的时间，请耐心等待。
