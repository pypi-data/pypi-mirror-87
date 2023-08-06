# MP-exchange

Django exchange app.

### Installation

Install with pip:

```
$ pip install django-mp-exchange
```

Product manager (extending):
```
    from exchange.managers import MultiCurrencyManager
    
    class ProductManager(MultiCurrencyManager):
        ...
```

Product queryset (extending):
```
from exchange.querysets import MultiCurrencyQuerySet
 
class ProductQuerySet(MultiCurrencyQuerySet):
    ...
```

Product model:
```
from exchange.models import MultiCurrencyPrice
 
class Product(MultiCurrencyPrice):
    ...
    
```
