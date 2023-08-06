# -*- coding: utf-8 -*-
from plone import api
from zope.component import queryUtility
from zope.i18n.interfaces import ITranslationDomain


def _(msgid, context, domain="collective.pivot", mapping=None):
    translation_domain = queryUtility(ITranslationDomain, domain)
    return translation_domain.translate(msgid, context=context.REQUEST, mapping=mapping)


def add_category(context, family_id, title):
    """Add a category in the configuration folder"""
    pivot_category = api.content.create(
        container=context, type="pivot_category", family=family_id, title=title
    )
    return pivot_category
