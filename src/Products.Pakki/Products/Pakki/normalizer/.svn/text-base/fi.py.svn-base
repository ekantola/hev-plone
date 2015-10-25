from plone.i18n.normalizer.interfaces import INormalizer
from zope.interface import implements
from plone.i18n.normalizer.base import mapUnicode

# Finnish character mapping
mapping = {
    196 : 'A', 197 : 'A', 214 : 'O', 220 : 'U',
    228 : 'a', 229 : 'a', 246 : 'o', 252 : 'u'
}

class Normalizer(object):
    """
    This normalizer can normalize any unicode string and returns a version
    that only contains of ASCII characters.

    Let's make sure that this implementation actually fulfills the API.

      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(INormalizer, Normalizer)
      True

      >>> norm = Normalizer()
      >>> norm.normalize(u'\xe4')
      'a'
    """
    implements(INormalizer)

    def normalize(self, text, locale=None, max_length=None):
        """
        Returns a normalized text. text has to be a unicode string.
        """
        return mapUnicode(text, mapping=mapping)

normalizer = Normalizer()
