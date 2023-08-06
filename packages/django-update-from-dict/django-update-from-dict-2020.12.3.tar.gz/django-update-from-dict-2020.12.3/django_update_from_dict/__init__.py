__all__ = ['update_from_dict', 'UpdateFromDictMixin']


def update_from_dict(instance, attrs, commit):
    """Update Django model from dictionary"""

    field_names = list(map(lambda f: f.name, instance._meta.get_fields()))
    for attr, val in attrs.items():
        if attr in field_names:
            setattr(instance, attr, val)

    if commit:
        instance.save()


class UpdateFromDictMixin:
    """Update Django model from dictionary"""

    def update_from_dict(self, attrs, commit):
        return update_from_dict(self, attrs, commit)
