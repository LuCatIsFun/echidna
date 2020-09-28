"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/8/3 6:08 下午
"""

from pymdownx import emoji
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from markdown.extensions.fenced_code import FencedBlockPreprocessor

FencedBlockPreprocessor.CODE_WRAP = '<pre class="line-numbers"><code%s>%s</code></pre>'
FencedBlockPreprocessor.LANG_TAG = ' class="language-%s"'

MARKDOWN_EXTENSION = [
    # 官方拓展 https://python-markdown.github.io/extensions/
    TocExtension(slugify=slugify),  # 文章目录
    'nl2br',
    'tables',
    'abbr',
    'admonition',
    'footnotes',
    'attr_list',
    'footnotes',
    'md_in_html',

    # 第三方拓展 https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex/
    'pymdownx.betterem',  # 粗体
    'pymdownx.details',  # 详情
    'pymdownx.emoji',  # emoji
    'pymdownx.caret',
    'pymdownx.critic',
    'pymdownx.escapeall',
    'pymdownx.keys',  # 键盘按键
    'pymdownx.magiclink',  # 短链接
    'pymdownx.smartsymbols',
    'pymdownx.tasklist',  # 列表
    'pymdownx.tabbed',
    'pymdownx.progressbar',  # 进度条
    'pymdownx.mark',
    'pymdownx.tilde',
    'pymdownx.highlight',
    'pymdownx.superfences',
    'pymdownx.inlinehilite'

]

MARKDOWN_EXTENSION_CONFIG = {
    "pymdownx.magiclink": {
        "repo_url_shortener": True,
        "repo_url_shorthand": True,
        "provider": "github",
        "user": "facelessuser",
        "repo": "pymdown-extensions"
    },
    "pymdownx.tilde": {
        "subscript": False
    },
    "pymdownx.highlight": {
        "guess_lang": True,
        "use_pygments": False
        # "linenums": True
    },
    'pymdownx.inlinehilite': {
        "css_class": 'inlinehilite',
    },
    "pymdownx.tasklist": {
        "custom_checkbox": True
    },
    "pymdownx.emoji": {
        "emoji_index": emoji.emojione,
        "emoji_generator": emoji.to_svg,
        "alt": "short",
        "options": {
            "attributes": {
                "align": "absmiddle",
                "height": "20px",
                "width": "20px"
            },
        }
    }
}

# 判断目录为空时的字符串
MARKDOWN_NONE_TOC = """<div class="toc"><ul></ul></div>"""
