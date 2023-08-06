from zope.deprecation import deprecated
from zope.interface import Interface


class IRefEGovService(Interface):
    """ Marker interface for RefEGovService """


class IEGovService(Interface):
    """ Marker interface for EGovService"""


# Old names for these interfaces - probably unused, but deprecated to make sure
IEgovLeistung = IEGovService
IRefEgovService = IRefEGovService

deprecated(
    ['IEgovLeistung'],
    'This marker interface has been deprecated in favour of IEGovService'
    ''
)
deprecated(
    ['IRefEgovService'],
    'This marker interface has been deprecated in favour of IRefEGovService'
)
