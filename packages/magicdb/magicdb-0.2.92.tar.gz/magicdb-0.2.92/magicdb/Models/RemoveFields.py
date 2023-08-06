class RemoveFields:
    fields_to_remove = set()

    def __init__(self, *args, **kwargs):
        self.remove_fields()
        super().__init__(*args, **kwargs)

    def remove_fields(self):
        if getattr(self, "__field_defaults__") and getattr(self, "__fields__"):
            for field in self.__field_defaults__["fields_to_remove"]:
                if field in self.__fields__:
                    del self.__fields__[field]
            del self.__fields__["fields_to_remove"]
