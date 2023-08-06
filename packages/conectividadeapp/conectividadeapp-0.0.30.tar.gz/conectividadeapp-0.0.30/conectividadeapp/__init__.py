from extras.plugins import PluginConfig


class ConectividadeAppConfig(PluginConfig):
    name = 'conectividadeapp'
    verbose_name = 'conectividade'
    description = 'An plugin'
    version = '0.0.30'
    author = 'Johnny; Avando; Eduardo; Rary'
    author_email = 'johnnyyuri56@gmail.com'
    required_settings = []
    default_settings = {
        'loud': False
    }

    # Base URL path. If not set, the plugin name will be used.
    base_url = 'conectividadeapp'
    # Caching config
    caching_config = {}


config = ConectividadeAppConfig
