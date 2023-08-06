import django
import sre_parse
from sre_constants import LITERAL, AT, AT_END

_NEWEST_DJANGO = float(django.get_version()) >= float(2.0)

try:
    # Python 3
    from urllib.parse import quote, unquote
    unichr = chr
except ImportError:
    # Python 2
    from urllib import quote, unquote

try:
    from django.core.urlresolvers import get_urlconf, get_resolver, RegexURLResolver
    from django.conf.urls import url
except ImportError:
    from django.urls import get_urlconf, get_resolver, URLResolver
    from django.urls import path, re_path


def robots_decorator(url_function):
    """
    Decorator for django.conf.urls.url
    """
    def url_extended(regex, view, kwargs=None, name=None, robots_allow=None):
        resolver_or_pattern = url_function(regex, view, kwargs=kwargs, name=name)

        resolver_or_pattern.robots_allow = robots_allow
        return resolver_or_pattern

    return url_extended


if _NEWEST_DJANGO is True:
    path = robots_decorator(path)
    re_path = robots_decorator(re_path)
else:
    url = robots_decorator(url)


def create_rules(urlconf=None):
    """
    Creates rules from conf
    """
    if urlconf is None:
        urlconf = get_urlconf()

    root_resolver = get_resolver(urlconf)
    rule_list = create_rule_list(root_resolver, '')

    return u'\n'.join(rule_list)


def create_rule_list(parent_resolver, abs_pattern):
    """
    Creates usable rule list
    """
    rule_list = []

    for resolver in parent_resolver.url_patterns:
        try:
            pattern = join_patterns(abs_pattern, resolver.regex.pattern)
        except AttributeError:
            pattern = join_patterns(abs_pattern, resolver.pattern)
        rule = ''
        robots_allow = getattr(resolver, 'robots_allow', None)

        if robots_allow is None:
            pass
        elif robots_allow:
            rule = 'Allow: '
        else:
            rule = 'Disallow: '

        if rule:
            path = clean_pattern(pattern)
            rule += path
            rule_list.append(rule)

        try:
            if isinstance(resolver, RegexURLResolver):
                rule_list += create_rule_list(resolver, pattern)
        except:
            if isinstance(resolver, URLResolver):
                rule_list += create_rule_list(resolver, pattern)

    return rule_list


def join_patterns(pattern1, pattern2):
    """
    Joins URL patterns
    """
    if pattern1.endswith('$'):
        return pattern1
    try:
        if pattern2.startswith('^'):
            return pattern1 + pattern2[1:]
        if pattern2:
            return pattern1 + '.' + pattern2
    except AttributeError:
        if str(pattern2).startswith('^'):
            return pattern1 + str(pattern2)[1:]
        if pattern2:
            return pattern1 + '.' + str(pattern2)

    return pattern1


def clean_pattern(pattern):
    """
    Cleans URL patterns
     * pattern => token
     * '2'     => ('literal', 50)
     * '2|3'   => ('in', [('literal', 50), ('literal', 51)])
    """
    star = '*'
    parsed = sre_parse.parse(pattern)
    literals = []

    for token in parsed:
        if token[0] == LITERAL:
            character = quote(unichr(token[1]).encode('utf8'))
            literals.append(character)
        elif token[0] == AT:
            pass

        elif literals[-1:] != [star]:
            literals.append(star)

    rule = '/' + ''.join(literals)

    if parsed and not rule.endswith(star):
        if parsed[-1] == (AT, AT_END):
            rule += '$'
        else:
            rule += star

    return rule
