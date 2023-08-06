"""
    sphinxnotes.peopledomain
    ~~~~~~~~~~~~~~~~~~~~~~~~

    The domain for describing people.

    :copyright: Copyright 2020 Shengyu Zhang
    :license: BSD, see LICENSE for details.
"""

from typing import Any, Dict, Iterator, Tuple
from typing import cast

from docutils.nodes import Element, Text, reference
from docutils.parsers.rst import directives

from sphinx.addnodes import pending_xref, desc_signature, desc_name
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType
from sphinx.environment import BuildEnvironment
from sphinx.locale import _, __
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinx.util.nodes import make_refnode
try:
    from sphinx.util.nodes import make_id
except Exception:
    from docutils.nodes import make_id


logger = logging.getLogger(__name__)

class FriendDirective(ObjectDescription):
    """
    Directive implementation for descripting a friend.
    """

    required_arguments = 1
    option_spec = {
        'homepage': directives.uri,
        'blog': directives.uri,
    }
    has_content = True

    def add_target_and_index(self, name: str, sig: str, signode: desc_signature) -> None:
        node_id = make_id(self.env, self.state.document, self.objtype, name)
        signode['ids'].append(node_id)

        self.state.document.note_explicit_target(signode)

        domain = cast(PeopleDomain, self.env.get_domain('ppl'))
        domain.note_object(self.objtype, name, node_id, location=signode)

    def handle_signature(self, sig: str, signode: desc_signature) -> str:
        # Generate node for people name
        signode += desc_name(text=sig)

        # Separator of name and external link
        signode += Text(' ')

        # Generate external link to people's homepage
        if self.options.get('homepage'):
            homepage = self.options.get('homepage')
            signode += reference(text=homepage, refuri=homepage)

        return sig


class PeopleRole(XRefRole):
    """
    Role implementation for refering to a people.
    """

    def process_link(self, env: BuildEnvironment, refnode: Element,
                     has_explicit_title: bool, title: str, target: str) -> Tuple[str, str]:
        return '@' + title, target

class PeopleDomain(Domain):
    """People domain."""
    name = 'ppl'
    label = 'People'

    object_types = {
        'friend': ObjType(_('friend'), 'friend'),
    }
    directives = {
        'friend': FriendDirective,
    }
    roles = {
        'friend': PeopleRole(),
    }
    initial_data = {
        'objects': {},  # fullname -> docname, objtype
    }

    @property
    def objects(self) -> Dict[Tuple[str, str], Tuple[str, str]]:
        return self.data.setdefault('objects', {})  # (objtype, fullname) -> (docname, node_id)

    def note_object(self, objtype: str, name: str, node_id: str, location: Any = None) -> None:
        if (objtype, name) in self.objects:
            docname, node_id = self.objects[objtype, name]
            logger.warning(__('duplicate description of %s %s, other instance in %s') %
                           (objtype, name, docname), location=location)

        self.objects[objtype, name] = (self.env.docname, node_id)

    def clear_doc(self, docname: str) -> None:
        for (typ, name), (doc, node_id) in list(self.objects.items()):
            if doc == docname:
                del self.objects[typ, name]

    def resolve_xref(self, env: BuildEnvironment, fromdocname: str, builder: Builder,
                     typ: str, target: str, node: pending_xref, contnode: Element
                     ) -> Element:
        objtypes = self.objtypes_for_role(typ)
        for objtype in objtypes:
            todocname, node_id = self.objects.get((objtype, target), (None, None))
            if todocname:
                return make_refnode(builder, fromdocname, todocname, node_id,
                                    contnode, target + ' ' + objtype)
        return None

    def get_objects(self) -> Iterator[Tuple[str, str, str, str, str, int]]:
        for (typ, name), (docname, node_id) in self.data['objects'].items():
            yield name, name, typ, docname, node_id, 1


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_domain(PeopleDomain)

    return {
        'version': 'builtin',
        'env_version': 2,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
