import pprint

import attr

_pprinter = pprint.PrettyPrinter()


@attr.s
class TdxModel(object):
    # Used to warn users that this object may only have partial data
    # and performing a save() call could result in data loss.
    _partial = attr.ib(default=True, repr=False, eq=False)
    __tdx_type__ = None

    @classmethod
    def from_data(cls, data, partial=True):
        """Create an instance of object from TDX json decoded data."""
        # 404 errors will return no data
        if data is None:
            return None

        def model_from_dict(class_, dictionary):
            kwargs = {}

            for field in [f for f in attr.fields(class_) if f.repr]:
                tdx_name = field.metadata["tdx_name"]

                try:
                    val = dictionary[tdx_name]

                    if isinstance(val, str) and val.strip() == "":
                        val = None

                    kwargs[field.name] = val
                except KeyError:
                    pass

            return class_(partial=partial, **kwargs)

        if isinstance(data, dict):
            return model_from_dict(cls, data)

        elif isinstance(data, list):
            return [model_from_dict(cls, d) for d in data]

        else:
            raise ValueError(f"Failed to create {cls.__name__} from {type(data)}")

    def __str__(self):
        return _pprinter.pformat(attr.asdict(self, filter=lambda a, v: a.repr is True))
