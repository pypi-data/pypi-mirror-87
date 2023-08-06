import warnings
from typing import List, Tuple
from urllib.parse import urldefrag

import rdflib
import pyshacl

from fairworkflows import namespaces
from fairworkflows.config import ROOT_DIR
from nanopub import Publication, NanopubClient


class RdfWrapper:
    def __init__(self, uri, ref_name='fairobject'):
        self._rdf = rdflib.Graph()
        self._uri = str(uri)
        self.self_ref = rdflib.term.BNode(ref_name)
        self._is_modified = False
        self._is_published = False
        self._bind_namespaces()

    def _bind_namespaces(self):
        """Bind namespaces used often in fair step and fair workflow.

        Unused namespaces will be removed upon serialization.
        """
        self.rdf.bind("npx", namespaces.NPX)
        self.rdf.bind("pplan", namespaces.PPLAN)
        self.rdf.bind("dul", namespaces.DUL)
        self.rdf.bind("bpmn", namespaces.BPMN)
        self.rdf.bind("pwo", namespaces.PWO)

    @property
    def rdf(self) -> rdflib.Graph:
        """Get the rdf graph."""
        return self._rdf

    @property
    def uri(self) -> str:
        """Get the URI for this RDF."""
        return self._uri

    @property
    def is_modified(self) -> bool:
        """Returns true if the RDF has been modified since initialisation"""
        return self._is_modified

    def add_triple(self, s, p, o):
        """ Add any general triple to the rdf i.e. that does not have the self_ref (step, or plan) as subject """
        self._rdf.add((s, p, o))

    def get_attribute(self, predicate, return_list=False):
        """Get attribute.

        Get attribute of this RDF.

        Returns:
            The object for which the predicate corresponds to predicate
            argument and subject corresponds to this concept. Return None
            if no attributes are found, or a list of attributes if multiple
            matching objects are found.
        """
        objects = list(self._rdf.objects(subject=self.self_ref,
                                         predicate=predicate))
        if return_list:
            return objects

        if len(objects) == 0:
            return None
        elif len(objects) == 1:
            return objects[0]
        else:
            return objects

    def set_attribute(self, predicate, value, overwrite=True):
        """Set attribute.

        Set attribute of this RDF. I.e. for the given `predicate` argument, set
        the object to the given `value` argument for the subject
        corresponding to this RDF. Optionally overwrite the attribute if it
        already exists (but throw a warning).
        """
        if overwrite and self.get_attribute(predicate) is not None:
            warnings.warn(f'A predicate {predicate} was already defined'
                          f'overwriting {predicate} for {self.self_ref}')
            self.remove_attribute(predicate)
        self._rdf.add((self.self_ref, predicate, value))
        self._is_modified = True

    def remove_attribute(self, predicate, object=None):
        """Remove attribute.

        If `object` arg is None: remove attribute of this RDF. I.e. remove all
        triples from the RDF for the given `predicate` argument that have the
        self-reference subject. Else remove only attributes with the object
        matching the `object` arg.
        """
        self._rdf.remove((self.self_ref, predicate, object))

    def shacl_validate(self, shaclfile=str(ROOT_DIR / 'shacl/plex-shapes.ttl')):
        sg = rdflib.Graph()
        sg.parse(shaclfile, format='ttl')
        r = pyshacl.validate(self._rdf, shacl_graph=sg, inference='rdfs', abort_on_error=False, meta_shacl=False, advanced=False, js=False, debug=False)
        conforms, results_graph, results_text = r

        assert conforms, results_text

    def anonymise_rdf(self):
        """
        Replace any subjects or objects referring directly to the rdf uri, with a blank node
        """
        replace_in_rdf(self._rdf, oldvalue=rdflib.URIRef(self.uri), newvalue=self.self_ref)

    @classmethod
    def from_rdf(cls, rdf: rdflib.Graph, uri: str, fetch_references: bool = False,
                 force: bool = False, remove_irrelevant_triples: bool = True):
        """Construct RdfWrapper object from rdf graph.

        Args:
            rdf: The RDF graph
            uri: Uri of the object
            fetch_references: Boolean toggling whether to fetch objects from nanopub that are
                referred by this object (e.g. FairSteps in a FairWorkflow)
            force: Toggle forcing creation of object even if url is not in any of the subjects of
                the passed RDF
            remove_irrelevant_triples: Toggle removing irrelevant triples from the wrapped rdf.
        """
        raise NotImplementedError()

    @staticmethod
    def _uri_is_subject_in_rdf(uri: str, rdf: rdflib.Graph, force: bool):
        """Check whether uri is a subject in the rdf.

        Args:
            rdf: The RDF graph
            uri: Uri of the object
            force: Toggle raising an error (force=False) or just a warning (force=True)
        """
        if rdflib.URIRef(uri) not in rdf.subjects():
            message = (f"Provided URI '{uri}' does not "
                       f"match any subject in provided rdf graph.")
            if force:
                warnings.warn(message, UserWarning)
            else:
                raise ValueError(message + " Use force=True to suppress this error")

    @classmethod
    def from_nanopub(cls, uri: str, use_test_server=False):
        """Construct RdfWrapper object from an existing nanopublication.

        Fetch the nanopublication corresponding to the specified URI. Pass its assertion
        graph to from_rdf to construct the object.

        Args:
            uri: The URI of a nanopublication (e.g.: http://purl.org/np/id) that npx:introduces
                the RDF object as a concept or the URI of a nanopublication fragment pointing to a
                concept (e.g.: http://purl.org/np/id#concept)
            use_test_server: Toggle using the test nanopub server.
        """
        # Work out the nanopub URI by defragging the step URI
        nanopub_uri, frag = urldefrag(uri)

        # Fetch the nanopub
        client = NanopubClient(use_test_server=use_test_server)
        nanopub = client.fetch(nanopub_uri)

        if len(frag) > 0:
            # If we found a fragment we can use the passed URI
            uri = uri
        elif nanopub.introduces_concept:
            # Otherwise we try to extract it from 'introduced concept'
            uri = str(nanopub.introduces_concept)
        else:
            raise ValueError('This nanopub does not introduce any concepts. Please provide URI to '
                             'the FAIR object itself (not just the nanopub).')
        self = cls.from_rdf(rdf=nanopub.assertion, uri=uri, fetch_references=True)
        # Record that this RDF originates from a published source
        self._is_published = True
        return self

    def _publish_as_nanopub(self, use_test_server=False, **kwargs):
        """
        Publishes this rdf as a nanopublication.

        Args:
            use_test_server (bool): Toggle using the test nanopub server.
            kwargs: Keyword arguments to be passed to [nanopub.Publication.from_assertion](
                https://nanopub.readthedocs.io/en/latest/reference/publication.html#
                nanopub.publication.Publication.from_assertion).
                This allows for more control over the nanopublication RDF.

        Returns:
            a dictionary with publication info, including 'nanopub_uri', and 'concept_uri'
        """

        # If this RDF has been modified from something that was previously published,
        # include the original URI in the derived_from PROV (if applicable)
        derived_from = None
        if self._is_published:
            if self.is_modified:
                derived_from = self._uri
            else:
                warnings.warn(f'Cannot publish() this Fair object. This rdf is already published (at {self._uri}) and has not been modified locally.')
                return {'nanopub_uri': None, 'concept_uri': None}

        for invalid_kwarg in ['introduces_concept', 'assertion_rdf']:
            if invalid_kwarg in kwargs:
                raise ValueError(f'{invalid_kwarg} is automatically filled by fairworkflows '
                                 f'library, you cannot set it.')

        if 'derived_from' in kwargs:
            derived_from = self._merge_derived_from(user_derived_from=kwargs['derived_from'],
                                                    our_derived_from=derived_from)
            del kwargs['derived_from']  # We do not want to pass derived_from multiple times.

        # Publish the rdf of this step as a nanopublication
        nanopub = Publication.from_assertion(assertion_rdf=self.rdf,
                                             introduces_concept=self.self_ref,
                                             derived_from=derived_from,
                                             **kwargs)
        client = NanopubClient(use_test_server=use_test_server)
        publication_info = client.publish(nanopub)

        # Set the new, published, URI, which should be whatever the (published) URI of the concept that was introduced is.
        # Note that this is NOT the nanopub's URI, since the nanopub is not the step/workflow. The rdf object describing the step/workflow
        # is contained in the assertion graph of the nanopub, and has its own URI.
        self._uri = publication_info['concept_uri']

        self._is_published = True
        self._is_modified = False

        return publication_info

    @staticmethod
    def _merge_derived_from(user_derived_from, our_derived_from):
        """
        Merge user-provided `derived_from` with `derived_from` that is based on self.uri .

        Returns:
             A list of derived_from URIRefs.
        """
        if our_derived_from is None:
            return user_derived_from
        if not isinstance(user_derived_from, list):
            user_derived_from = [user_derived_from]
        return user_derived_from + [our_derived_from]


def replace_in_rdf(rdf: rdflib.Graph, oldvalue, newvalue):
    """
    Replace subjects or objects of oldvalue with newvalue
    """
    for s, p, o in rdf:
        if s == oldvalue:
            rdf.remove((s, p, o))
            rdf.add((newvalue, p, o))
        elif o == oldvalue:
            rdf.remove((s, p, o))
            rdf.add((s, p, newvalue))
