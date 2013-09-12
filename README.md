#Cleanly

A HTML cleanup/sanitizer based on Google's html5lib for use in Django.

##License

Cleanly is released under the zlib license and can be used for personal, commercial and educational purposes. See the `LICENSE` file in the root directory.

##Requirements

* **html5lib** - [https://github.com/html5lib/html5lib-python]()
* **Django** - [https://www.djangoproject.com/]()

##Quick Start

###Installation

Install directly from **GitHub**:

    $ git clone git://github.com/russelljk/cleanly.git
    $ cd cleanly
    $ python setup.py install

Install Cleanly to your Django project by adding it to your `INSTALLED_APPS`.

    INSTALLED_APPS = (
        ...
        'cleanly',
    )

###Usage    

**Cleanup Only**, use for trusted sources only (ie yourself).

This will cleanup open tags, unquoted attributes. See the html5lib documentation for more details.

    {% load 'cleanly' %}

    {{page.html|cleanup_html}}

**Sanitize**, use for semi-trusted sources. 

For instance an author that writes articles for your blog/website. The most dangerous tags are stripped, along side non-body tags like `html`, `head`, `link`, `style`.

    {% load 'cleanly' %}

    {{page.html|sanitize_html}}
    
**Restricted**, use for untrusted sources. 

For example comments on a blog, forum or other public website. Be careful and test for unexpected input before going live. You want to review the tags that are stripped by Cleanly beforehand and make sure it meets your needs.

Note that even if you are using **Markdown** or another HTML generator/markup language, you should still sanitize the results before displaying them.

    {% load 'cleanly' %}

    {{page.html|restricted_html}}

###Customization

You have the ability to create customizable sanitizers.

**For example:**

In your settings.py file:
    
    CLEANILY_CONF = {
        'MySanitizer': {
            'elements': ('a', 'p', 'ul', 'li',),
            'attributes': ('style', 'title', 'name', 'id', 'class')
            'css': ('text-align', 'color'),
        },
        'MyCleaner': ...
    }

`CLEANILY_CONF` Should be a dictionary of sanitizer definitions. Each definition should be a dictionary containing tuple of the `elements`, `attributes` and `css` values allowed when cleaning html.

Any value not listed will be removed when cleaned.

To use it in your template simple do the following:

    {% load 'cleanly' %}
    
    {{page.html|clean_with:'MySanitizer'}}

###TODO 

####More Backends

Add backends for other html/xml parsers. Backends must use a whitelist vs blacklist to filter html. They must support HTML5 as well.
