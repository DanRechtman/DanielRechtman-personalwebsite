from typing import List, Tuple, Type, TypeVar

class Helper:
    classmodel = TypeVar("classmodel")

    @staticmethod
    def get_or_none(classmodel:classmodel, **kwargs)->Tuple[classmodel,None]:
        try:
            return classmodel.objects.get(**kwargs)
        except classmodel.DoesNotExist:
            return None
