import re


def get_fs(src: str, context: dict, spl: str="$") -> str:
    """
    解析自定义 f 字符串格式：
    - $name 替换为字典中的值
    - $$ 转义为单个 $
    - 未识别的占位符保留原样

    :param src: 包含占位符的原始字符串
    :param context: 包含占位符键值对的字典
    :param spl:

    :return: 解析后的字符串
    """
    # 正则匹配：$$ 或 $ + 合法标识符 (字母/下划线开头)
    pattern = fr'(\{spl}\{spl})|(\$[a-zA-Z_][a-zA-Z0-9_]*)'

    def replace(match):
        # 处理 $$ 转义情况
        if match.group(1):
            return spl

        # 提取占位符名称 (去掉开头的$)
        placeholder = match.group(2)[1:]

        # 替换已知占位符，未知保留原样
        return str(context.get(placeholder, match.group(2)))

    return re.sub(pattern, replace, src)