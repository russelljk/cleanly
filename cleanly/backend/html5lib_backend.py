import html5lib
from html5lib import sanitizer, serializer, tokenizer, treebuilders, treewalkers

__all__ = ['cleanup_html', 'sanitize_html', 'make_sanitizer', 'sanitizer_manager', 'run_sanitizer']

def make_sanitizer(elements, attributes, css):
    class _Mixin(sanitizer.HTMLSanitizerMixin):
        acceptable_elements = elements
    
        acceptable_attributes = attributes
    
        allowed_elements = acceptable_elements
        allowed_attributes = acceptable_attributes
        allowed_css_properties = css
        allowed_css_keywords = ()
        allowed_svg_properties = ()
    
    class _Sanitizer(tokenizer.HTMLTokenizer, HTMLSanitizerMixin):
        def __init__(self, stream, encoding=None, parseMeta=True, useChardet=True,
                                 lowercaseElementName=True, lowercaseAttrName=True, parser=None):
            tokenizer.HTMLTokenizer.__init__(self, stream, encoding, parseMeta,
                                             useChardet, lowercaseElementName,
                                             lowercaseAttrName, parser)

        def __iter__(self):
            for token in tokenizer.HTMLTokenizer.__iter__(self):
                token = self.sanitize_token(token)
                if token:
                    yield token
    return _Sanitizer

HTMLSanitizer = make_sanitizer(
    elements = ( 'a', 'abbr', 'acronym', 'address', 'article', 'aside', 'b', 'bdi', 'bdo', 'big',
        'blockquote', 'br', 'caption', 'center', 'cite', 'code', 'col',
        'colgroup', 'data', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt', 'em', 'figcaption', 
        'figure', 'font', 'footer', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'heading', 'hr', 'i', 'img', 'ins', 'kbd',
        'li', 'mark', 'nav', 'ol', 'p', 'pre', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'section', 'small', 'span', 'strike',
        'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'time', 'tfoot', 'th', 'thead',
        'tr', 'u', 'ul', 'var', 'wbr'),
    
    attributes = ( 'abbr', 'align', 'alt', 'axis', 'border',
        'cellpadding', 'cellspacing', 'char', 'charoff', 'charset', 'cite',
        'cols', 'colspan', 'datetime', 'dir', 'frame', 'headers', 'height',
        'href', 'hreflang', 'hspace', 'lang', 'longdesc', 'name', 'nohref',
        'noshade', 'nowrap', 'rel', 'rev', 'rows', 'rowspan', 'rules', 'scope',
        'span', 'style', 'src', 'start', 'summary', 'title', 'type', 'valign', 'vspace',
        'width'),
    css = ('text-decoration', 'font-style', 'font-weight', 'text-justify', 
        'text-align', 'color'),    
)

HTMLRestrictedSanitizer = (
    elements = ('a', 'abbr', 'blockquote', 'br', 'code', 'em', 
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'figcaption', 
        'figure', 'img', 'li', 'ol', 'p', 'pre', 'span', 'strike',
        'strong', 'sub', 'sup', 'u', 'ul'),
    
    attributes = ('alt', 'cite', 'height',
        'href', 'span', 'style', 'src', 'title', 'width'),
    
    css = ( 'text-decoration' , 'font-style', 'font-weight', 'text-justify', 
        'text-align', 'color'),            
)

class SanitizerManager(object):
    def __init__(self):
        self.sanitizers = {}
    
    def register(self, name, val):
        self.sanitizers[name] = val
    
    def lookup(self, name):
        try:
            return self.sanitizers[name]
        except KeyError:
            # Look and see if the sanitizer is defined else where.
            from django.conf import settings
            cleanly_conf = getattr(settings, 'CLEANLY_CONF', None)
            
            # Just re-raise the KeyError if it's not found.
            if cleanly_conf is None:
                raise
            
            # Create the sanitizer and return it.
            conf = CLEANLY_CONF[name]
            sanitizer = make_sanitizer(**conf)
            self.register(name, sanitizer)
            return sanitizer

sanitizer_manager = SanitizerManager()
sanitizer_manager.register('Default', HTMLSanitizer)
sanitizer_manager.register('Restricted', HTMLRestrictedSanitizer)

def run_sanitizer(html, sanitizer):
    parser = html5lib.HTMLParser(tokenizer=sanitizer,
                            tree=treebuilders.getTreeBuilder("dom"))
    dom_tree = parser.parseFragment(html)
    walker = treewalkers.getTreeWalker("dom")
    stream = walker(dom_tree)
    s = serializer.HTMLSerializer(omit_optional_tags=False, quote_attr_values=True)
    result = s.serialize(stream)
    return u''.join(result)
    
def sanitize_html(html, restricted=False):    
    if restricted:
        the_sanitizer = HTMLRestrictedSanitizer
    else:
        the_sanitizer = HTMLSanitizer
    return run_sanitizer(html, the_sanitizer)

def cleanup_html(html):
    parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"))
    dom_tree = parser.parseFragment(html)
    walker = treewalkers.getTreeWalker("dom")
    stream = walker(dom_tree)
    s = serializer.htmlserializer.HTMLSerializer(omit_optional_tags=False, quote_attr_values=True)
    result = s.render(stream)
    return u''.join(result)