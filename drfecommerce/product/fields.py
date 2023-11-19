from typing import Any
from django.core import checks
from django.db import models
from django.db.models import Model
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    description="unique order field for field lines"
    def __init__(self, unique_for_field=None,*args, **kwargs):
        self.unique_for_field=unique_for_field
        super().__init__(*args, **kwargs)

    def check(self,**kwqrgs):
        return  [
            *super().check(**kwqrgs),
            *self._check_for_field_attribute(**kwqrgs)
        ]
    def _check_for_field_attribute(self,**kwargs):
        if self.unique_for_field is None:
            return [
                checks.Error("order field must define a 'unique for field' attribute ")
            ]
        elif self.unique_for_field not in [ f.name for f in self.model._meta.get_fields()]:
            return [
                checks.Error("orderfield does not match any existing model fields")
            ]
        return []
    
    def pre_save(self, model_instance, add):
        if getattr(model_instance,self.attname) is None:
            qs=self.model.objects.all()
            try:
                query={self.unique_for_field:getattr(model_instance,self.unique_for_field)}
                print(query)
                qs=qs.filter(**query)
                print(qs)
                last_item=qs.latest(self.attname)
                print(last_item)
                value=last_item.order+1
            except ObjectDoesNotExist:
                value=1
            return value
        return super().pre_save(model_instance, add)
