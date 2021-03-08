import re
from typing import Pattern

def regex_link() -> Pattern:
    regex = re.compile(
        r'((?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+))', re.IGNORECASE)
    return regex

def regex_link_only() -> Pattern:
    regex = re.compile(
        r'^' +
        regex_link().pattern +
        r'$',
        re.IGNORECASE
        )
    return regex


def regex_id() -> Pattern:
    regex = re.compile(
        r'((?!SC|NF|IRD|OMA|BCN|SHPC|RCM|WM)(?:(?:[A-Z0-9@#]+))|' # ID widthout quotes and spaces
        r'(?!SC|NF|IRD|OMA|BCN|SHPC|RCM|WM)(?:\"(?:[ A-Z0-9@#]+)\"))', # ID width quotes and spaces
        re.IGNORECASE
    )
    return regex

def regex_id_only() -> Pattern:
    regex = re.compile(
        r'^' +
        regex_id().pattern +
        r'$',
        re.IGNORECASE
        )
    return regex


def regex_shorthand() -> Pattern:
    regex = re.compile(
        r'((?:(?:(?:\d+)[ \t]*(?:SC|NF|IRD|OMA|BCN|SHPC|RCM|WM)[ \t]*)+)|' # amount name order
        r'(?:(?:(?:SC|NF|IRD|OMA|BCN|SHPC|RCM|WM)[ \t]*(?:\d+)[ \t]*)+))', # name amount order
        re.IGNORECASE
    )
    return regex

def regex_extract_shorthand() -> Pattern:
    regex = re.compile(
        r'(?:(\d+)[ \t]*(SC|NF|IRD|OMA|BCN|SHPC|RCM|WM)[ \t]*)', # amount name order
        re.IGNORECASE
    )
    return regex

def regex_extract_shorthand_reverse() -> Pattern:
    regex = re.compile(
        r'(?:(SC|NF|IRD|OMA|BCN|SHPC|RCM|WM)[ \t]*(\d+)[ \t]*)', # name amount order
        re.IGNORECASE
    )
    return regex

def regex_shorthand_only() -> Pattern:
    regex = re.compile(
        r'^' +
        regex_shorthand().pattern +
        r'$',
        re.IGNORECASE
        )
    return regex


def regex_p4types() -> Pattern:
    regex = re.compile(
        r'((?:(?:SC|NF|IRD|OMA|BCN|SHPC|RCM|WM)\s*){1,8})',
        re.IGNORECASE
    )
    return regex

def regex_extract_p4types() -> Pattern:
    regex = re.compile(
        r'(?:(SC|NF|IRD|OMA|BCN|SHPC|RCM|WM)\s*)',
        re.IGNORECASE
    )
    return regex

def regex_p4types_only() -> Pattern:
    regex = re.compile(
        r'^' +
        regex_p4types().pattern +
        r'$',
        re.IGNORECASE
        )
    return regex

def regex_id_and_link() -> Pattern:
    regex = re.compile(
        r'^' +
        regex_id().pattern +
        r' ' +
        regex_link().pattern +
        r'$',
        re.IGNORECASE
    )
    return regex

def regex_id_and_shorthand() -> Pattern:
    regex = re.compile(
        r'^' +
        regex_id().pattern +
        r' ' +
        regex_shorthand().pattern +
        r'$',
        re.IGNORECASE
    )
    return regex

def regex_id_and_p4type() -> Pattern:
    regex = re.compile(
        r'^' +
        regex_id().pattern +
        r' ' +
        regex_p4types().pattern +
        r'$',
        re.IGNORECASE
    )
    return regex