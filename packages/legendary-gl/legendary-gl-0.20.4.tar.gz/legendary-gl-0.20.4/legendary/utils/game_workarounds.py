# coding: utf-8

# games where the download order optimizations are enabled by default
_optimize_default = {
    'wombat', 'snapdragon'
}


def is_opt_enabled(app_name):
    return app_name.lower() in _optimize_default


_cyberpunk_sdl = {
    'de': {'tags': ['voice_de_de'], 'name': 'Deutsch'},
    'es': {'tags': ['voice_es_es'], 'name': 'español (España)'},
    'fr': {'tags': ['voice_fr_fr'], 'name': 'français'},
    'it': {'tags': ['voice_it_it'], 'name': 'italiano'},
    'ja': {'tags': ['voice_ja_jp'], 'name': '日本語'},
    'ko': {'tags': ['voice_ko_kr'], 'name': '한국어'},
    'pl': {'tags': ['voice_pl_pl'], 'name': 'polski'},
    'pt': {'tags': ['voice_pt_br'], 'name': 'português brasileiro'},
    'ru': {'tags': ['voice_ru_ru'], 'name': 'русский'},
    'zh': {'tags': ['voice_zh_cn'], 'name': '中文（中国）'}
}


def cyber_prompt_2077():
    print('You are about to install Cyberpunk 2077, this game supports selective downloads for langauge packs.')
    print('The following language packs are available:')
    for tag, info in _cyberpunk_sdl.items():
        print(' *', tag, '-', info['name'])

    print('Please enter a comma-separated list of language packs to install (leave blank for english only)')
    choices = input('Additional languages [e.g. de,fr]: ')
    if not choices:
        return ['']

    tags = ['']
    for c in choices.split(','):
        c = c.strip()
        if c in _cyberpunk_sdl:
            tags.extend(_cyberpunk_sdl[c]['tags'])
        else:
            print('Invalid tag:', c)

    return tags
