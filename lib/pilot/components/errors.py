
class ComponentManagerImportError(ImportError):
    pass


class ComponentManagerReservedError(ComponentManagerImportError):
    pass


class ComponentManagerNotAComponentError(ComponentManagerImportError):
    pass


class ComponentManagerSetError(AttributeError):
    pass
