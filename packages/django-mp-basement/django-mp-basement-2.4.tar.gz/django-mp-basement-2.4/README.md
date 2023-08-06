Install with pip:

```
pip install django-mp-basement
```

Settings:
```
from basement.settings import BasementSettings


BASE_DIR = dirname(dirname(abspath(__file__)))
 
 
class BaseSettings(BasementSettings):
 
    BASE_DIR = BASE_DIR
    DB_NAME = 'example'
    DOMAIN = 'example.com'
    SECRET_KEY = 'some_secret_key'
```

Local settings:
```
from basement.settings import LocalSettingsMixin
from core.common_settings import CommonSettings
 
 
class Settings(LocalSettingsMixin, CommonSettings):
    pass

```

Production settings:
```
from basement.settings import ProductionSettingsMixin
from core.common_settings import CommonSettings
 
 
class Settings(ProductionSettingsMixin, CommonSettings):
    pass
```
