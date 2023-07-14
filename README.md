# <center>Learning Large Model</center>

## 环境

* `multi_key_chat_open_ai.py` 为了避免 open_ai 的 limit 限制而做了轮训 api_key。


* 使用代理

    使用 `langchain` 时很方便，参考 `multi_key_chat_open_ai.py`
    
    使用 `openai` 包有以下两种方法

    1. 启动 jupyter notebook 设置代理：
        ```bash
        jupyter notebook --generate-config
        ```
        生成配置文件 `~/.jupyter/jupyter_notebook_config.py`，在文件中添加如下配置：
        ```python
        import os
        os.environ['HTTP_PROXY'] = 'http://127.0.0.1:1080'
        os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:1080'
        ```

    2. 或直接设置代理
        ```python
        openai.proxy = os.environ['OPENAI_LOCAL_PROXY']
        ```

    3. 使用代理服务器：
        ```python
        api_base='https://api.openai-proxy.com/v1'
        openai.ChatCompletion.create(
            api_base=api_base,
        )
        ```