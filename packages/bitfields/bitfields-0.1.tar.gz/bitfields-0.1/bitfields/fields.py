"""
BitField objects
"""

from bitfields import PaddedBits
import inspect


# noinspection PyInitNewSignature
class BitFieldMeta(type):
    __fields__ = {}
    __funcs__ = []
    __bit_length__ = 0

    def __init__(cls, name, bases, attrs):
        super(BitFieldMeta, cls).__init__(name, bases, attrs)

        bit_pos = 0

        IGNORED = ("from_bits", "from_bytes")

        for key, val in list(cls.__dict__.items()):
            private = False

            # ignore builtin attributes
            if key.startswith("__") or key in IGNORED or not isinstance(val, int):
                private = True

            # retain custom functions or properties
            if inspect.isfunction(val) or inspect.ismethod(val) or inspect.isdatadescriptor(val):
                if key[0] == "_":
                    private = True
                else:
                    cls.__funcs__.append((key, val))

            if private:
                continue

            cls.__fields__[key] = (bit_pos, val)
            cls.__bit_length__ += val
            bit_pos += val


class BitField(object, metaclass=BitFieldMeta):
    """
    Skeleton class for custom bit flags. When called, a :class:`flags._LoadedBitField` is actually returned, as this
    class is only used to define bit flags.

    :param \\*\\*kwargs: Fields to populate the bit field with. Each field MUST be specified.

    :returns: :class:`flags._LoadedBitField`
    """

    __fields__ = {}
    __funcs__ = []
    __bit_length__ = 0

    def __new__(cls, **kwargs):
        for key in kwargs:
            if key not in cls.__fields__:
                raise KeyError("{!r} isn't a field for {!r}".format(key, cls.__name__))

        for key in cls.__fields__:
            if key not in kwargs:
                raise KeyError("Missing field {!r}".format(key))

        return _LoadedBitField(cls.__name__, cls.__fields__, cls.__bit_length__, funcs=cls.__funcs__,
                               attrs_given=kwargs)

    @classmethod
    def from_bits(cls, bits):
        """
        Populates a bit field from bits.

        :param bits: Bits to populate with. May be :class:`Bits`, :class:`PaddedBits`, or ``int``
        :returns: :class:`flags._LoadedBitField`
        """

        if not isinstance(bits, PaddedBits):
            bits = PaddedBits(int(bits), cls.__bit_length__)

        fields_given = {}

        for field, props in cls.__fields__.items():
            fields_given[field] = int(bits[props[0]: props[0] + props[1]])

        return _LoadedBitField(cls.__name__, cls.__fields__, cls.__bit_length__, funcs=cls.__funcs__,
                               attrs_given=fields_given)

    @classmethod
    def from_bytes(cls, b, byteorder="big"):
        """
        Populates a bit field from bytes object.

        :param bytes b: Bytes to populate with
        :param str byteorder: (Optional) Byte order. Must equal "big" or "little". Defaults to "big"

        :returns: :class:`flags._LoadedBitField`
        """

        bits = PaddedBits.from_bytes(b, byteorder=byteorder)

        return cls.from_bits(bits)

    @classmethod
    def from_stream(cls, stream, byteorder="big"):
        """
        Populates a bit field from a readable stream. ``stream.read(bit_length)`` will be called.

        :param stream: Readable stream, e.g., file object
        :param str byteorder: (Optional) Byte order. Must equal "big" or "little". Defaults to "little"

        :returns: :class:`flags._LoadedBitField`
        """

        byte_length = (cls.__bit_length__ + 7) // 8

        b = stream.read(byte_length)

        # allow normal streams
        if not isinstance(b, bytes):
            b = bytes(b, "utf-8")

        return cls.from_bytes(b, byteorder=byteorder)


class _LoadedBitField(object):
    """
    Populated bit field. Can be read or written to like a dictionary.
    """

    def __init__(self, name, fields, bit_length, funcs=None, attrs_given=None):
        self._bits = PaddedBits(0, bit_length)
        self._name = name
        self._fields = fields
        self._bit_length = bit_length

        self._attrs = {}
        for field in self._fields:
            value = attrs_given.get(field, 0)

            if value is True:
                value = 1
            if value is False:
                value = 0

            self._attrs[field] = value

        if funcs:
            for k, v in funcs:
                setattr(self, k, v)

                # ensure that data descriptors get called
                setattr(self.__class__, k, v)

        self._remake_bits()

    def __repr__(self):
        values = ["{}={}".format(key, self._attrs[key]) for key in self._fields]

        return self._name + "(" + ", ".join(values) + ")"

    def __bytes__(self):
        return bytes(self.bits)

    def __getitem__(self, item):
        if item not in self._fields:
            raise KeyError("{!r} isn't a field for {!r}".format(item, self._name))

        return self._attrs[item]

    def __setitem__(self, item, value):
        if item not in self._fields:
            raise KeyError("{!r} isn't a field for {!r}".format(item, self._name))

        field_bit_length = self._fields[item][1]
        if value.bit_length() > field_bit_length:
            raise ValueError("{!r} doesn't fit in {} bits".format(value, field_bit_length))

        self._attrs[item] = value

        self._remake_bits()

    def __int__(self):
        return int(self.bits)

    def update(self, **kwargs):
        """
        Updates bit fields with new values.

        :param \\*\\*kwargs: Values to update with.
        """
        for k, v in kwargs.items():
            self[k] = v

    def _remake_bits(self):
        for field, properties in self._fields.items():
            self._bits[properties[0]: properties[0] + properties[1]] = self._attrs[field]

    def bit_length(self):
        """
        Returns added bit length of the bit field.

        :returns: int
        """

        return self._bit_length

    @property
    def bits(self):
        return self._bits
