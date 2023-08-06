class Response(object):
    obj: object = None

    def __init__(self, obj):
        self.obj = obj

    def __iter__(self):
        """ Return the data object as iterator """
        if hasattr(self.obj, 'data'):
            return iter(self.obj.data)
        else:
            raise TypeError

    def __getattr__(self, item):
        """ Transpose the get attribute to the data object, except for the
        pagination property. """
        if item == 'pagination':
            if hasattr(self.obj, 'pagination'):
                return getattr(self.obj, item)
            else:
                raise AttributeError
        else:
            if hasattr(self.obj, 'data'):
                return getattr(self.obj.data, item)
            else:
                raise AttributeError

    def __repr__(self):
        """ Return the data object representation """
        if hasattr(self.obj, 'data'):
            return repr(self.obj.data)
        else:
            return repr(Response)

    def __getitem__(self, item):
        """ If the response data is subscriptable, return the requested
        item """
        if hasattr(self.obj, 'data'):
            if hasattr(self.obj.data, '__getitem__'):
                return self.obj.data[item]
            else:
                if item == 0:
                    return self.obj.data
                else:
                    raise IndexError
        else:
            raise IndexError

    def __len__(self):
        """ Get the length of the data object if iterable """
        if hasattr(self.obj, 'data'):
            if hasattr(self.obj.data, '__getitem__'):
                return len(self.obj.data)
            else:
                return 0
        else:
            return 0
