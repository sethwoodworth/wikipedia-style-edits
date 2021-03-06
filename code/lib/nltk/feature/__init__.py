# Natural Language Toolkit: Feature Extraction
#
# Copyright (C) 2001 University of Pennsylvania
# Author: Edward Loper <edloper@gradient.cis.upenn.edu>
# URL: <http://lib.nltk.sf.net>
# For license information, see LICENSE.TXT
#
# $Id: __init__.py,v 1.12 2004/09/19 08:12:01 stevenbird Exp $

"""
Classes and interfaces for processing a token's X{features}, or
specific pieces of information about the token.  Features are
extracted from a token's properties by X{feature detectors}, and
stored in a feature dictionary, which maps feature names to feature
values.  A X{feature encoder} can then be used to translate the
feature dictionary into a homogenous reprsentation (such as a sparse
boolean list), suitable for use with other processing tasks.

@todo: Add interfaces & support for feature selection.

@group Feature Detection: FeatureDetectorI, AbstractFeatureDetector,
    *FeatureDetector
@group Feature Encoding: FeatureEncoderI, AbstractFeatureEncoder,
    *FeatureEncoder
"""

from lib.nltk import TaskI, PropertyIndirectionMixIn
from lib.nltk.token import *
from lib.nltk.util import *
from sets import *

######################################################################
## Feature Detection
######################################################################

class FeatureDetectorI(TaskI):
    """
    A processing class for finding the values of one or more features
    for a token.  These features are stored in the C{FEATURES}
    property, which contains a dictionary mapping from feature names
    to feature values.
    """
    def features(self):
        """
        @return: A list of the names of the features that can be
        generated by this feature detector.  This list contains all
        features that the detector might generate; but the detector
        may generate a subset of these features for a given token,
        depending on its value.
            
        @rtype: C{list} of C{string}
        """
        raise NotImplementedError
    
    def detect_features(self, token):
        """
        Find the values of this detector's features for C{token}, and
        add them to the token's C{FEATURES} dictionary.  If the
        C{FEATURES} dictionary does not exist, then it is created.
        Any values for this detector's features that are already
        present in the C{FEATURES} dictionary will be overwritten; but
        any other features will not be modified.
        
        @param token: The token whose features should be found.
        @type token: L{Token}
        @outprop: L{FEATURES}
        """
        raise NotImplementedError

    def get_features(self, token):
        """
        Find the values of this detector's features for C{token}, and
        return them as a dictionary from feature names to feature
        values.
        
        @param token: The token whose features should be found.
        @type token: L{Token}
        @rtype: C{dict} from C{string} to C{*}
        """
        raise NotImplementedError
        
class AbstractFeatureDetector(FeatureDetectorI, PropertyIndirectionMixIn):
    """
    An abstract base class for feature detectors.
    C{AbstractFeatureDetector} provides a default implementation for
    L{detect_features} (based on C{get_features}).
    """
    def __init__(self, **property_names):
        PropertyIndirectionMixIn.__init__(self, **property_names)
        
    def detect_features(self, token):
        FEATURES = self.property('FEATURES')

        # Initialize FEATURES to {}, if it doesn't exist.
        if not token.has(FEATURES):
            token[FEATURES] = {}

        # Update FEATURES with the token's features (as given by
        # get_features).
        features = self.get_features(token)
        token[FEATURES].update(features)

class MergedFeatureDetector(AbstractFeatureDetector):
    def __init__(self, *detectors, **property_names):
        AbstractFeatureDetector.__init__(self, **property_names)
        self._detectors = detectors

    def features(self):
        feature_names = Set()
        for detector in self._detectors:
            feature_names.update(detector.features())
        return list(feature_names)

    def get_features(self, token):
        features = {}
        for detector in self._detectors:
            features.update(detector.get_features(token))
        return features

class PropertyFeatureDetector(AbstractFeatureDetector):
    """
    A feature detector that copies one or more of a token's properties
    into the feature dictionary.
    """
    def __init__(self, *properties, **property_names):
        """
        Create a new feature detectors that copies the specified token
        properties into the feature dictionary.
        
        @type properties: C{tuple} of C{string}
        @param properties: The list of token properties that should
            be copied into a token's feature dictionary.  These
            are treated as generic property names; in particular, they
            will be mappied through the C{property_names} dictionary.
        """
        AbstractFeatureDetector.__init__(self, **property_names)
        self._properties = [self.property(p) for p in properties]
        
    def features(self):
        return self._properties
    
    def get_features(self, token):
        return dict([(p,token[p]) for p in self._properties])

######################################################################
## Feature Encoding
######################################################################

class FeatureEncoderI(TaskI):
    """
    A processing class for encoding a token's feature dictionary as a
    X{feature vector}, or a fixed-length ordered sequence over
    homogenous values.  

    @inprop: C{FEATURES}: The feature dictionary.
    @outprop: C{FEATURE_VECTOR}: The encoded feature vector.
    """
    def encode_features(self, token):
        """
        Encode the given token's feature dictionary as a feature
        vector, and write the encoded features to the
        C{FEATURE_VECTOR} property.
        
        @param token: The token whose features should be encoded.
        @type token: L{Token}
        """
        raise NotImplementedError

    def features(self):
        """
        @return: A list of the names of the features that this feature
        encoder knows how to encodes.
        @rtype: C{list} of C{string}
        """
        raise NotImplementedError

    def description(self, index):
        """
        @return: A description of the feature vector value whose index
        is C{index}.
        @rtype: C{string}
        """
        raise NotImplementedError
        
    def num_features(self):
        """
        @return: The length of the feature vector generated by
        this feature encoder.
        """
        raise NotImplementedError
        
# Merges encoders for individual features:
class MergedFeatureEncoder(FeatureEncoderI, PropertyIndirectionMixIn):
    """
    A feature encoder that merges the outputs from two or more basic
    encoders into a single vector.
    """
    def __init__(self, encoders, **property_names):
        """
        Create a new merged feature encoder.
        
        @param encoders: The basic feature encoders whose output
            should be combined to form this encoder's output.
        """
        PropertyIndirectionMixIn.__init__(self, **property_names)
        self._encoders = encoders

    def encode_features(self, token):
        FEATURES = self.property('FEATURES')
        FEATURE_VECTOR = self.property('FEATURE_VECTOR')
        token[FEATURE_VECTOR] = self.raw_encode_features(token[FEATURES])

    def raw_encode_features(self, features):
        encoded_fvlist = self._encoders[0].raw_encode_features(features)
        for encoder in self._encoders[1:]:
            encoded_fvlist += encoder.raw_encode_features(features)
        return encoded_fvlist

    def description(self, index):
        for encoder in self._encoders:
            if index < encoder.num_features():
                return encoder.description(index)
            else:
                index -= encoder.num_features()
        raise IndexError, 'Index out of bounds'

    def num_features(self):
        return sum([num_features(e) for e in self._encoders])

class AbstractFeatureEncoder(FeatureEncoderI, PropertyIndirectionMixIn):
    """
    An abstract base class for feature encoders that encode a single
    feature, where each feature value index corresponds to a single
    feature value or subvalue.

    C{AbstractFeatureEncoder} provides default implementations for
    L{description}, L{num_features}, and L{encode_features} (based on
    C{raw_encode_features}).  It also provides three instance
    variables for subclasses: L{_feature_name}, L{_index_to_val}, and
    L{_val_to_index}.  Subclasses must implement
    L{raw_encode_features}.

    @ivar _feature_name: The name of the feature that is encoded by
        this feature encoder.
    @ivar _index_to_val: A list mapping indices in the feature vector
        to corresponding values.
    @ivar _index_to_val: A list mapping values to indices in the 
        feature vector.
    """
    def __init__(self, feature_name, values, **property_names):
        """
        Create a new feature encoder that encodes the feature with the
        given name.

        @type feature_name: C{string}
        @param feature_name: The name of the feature to encode.
        @type values: C{list}
        @param values: A list of the feature values of subvalues that
            the feature is known to take.  A feature vector index
            will also be created for unseen values.
        """
        PropertyIndirectionMixIn.__init__(self, **property_names)
        self._feature_name = feature_name
        
        # Initialize the mappings between basic values and feature
        # vector indices.  Reserve index 0 for unseen feature values.
        self._index_to_val = ['<unknown>']+list(values)
        self._val_to_index = dict([(v,i+1) for (i,v) in enumerate(values)])

    def description(self, index):
        if index == 0:
            return '%s=<unknown>' % self._feature_name
        else:
            return '%s=%r' % (self._feature_name, self._index_to_val[index])

    def num_features(self):
        return len(self._index_to_val)

    def encode_features(self, token):
        FEATURES = self.property('FEATURES')
        FEATURE_VECTOR = self.property('FEATURE_VECTOR')
        token[FEATURE_VECTOR] = self.raw_encode_features(token[FEATURES])

    def __repr__(self):
        return '<%s for %s>' % (self.__class__.__name__, self._feature_name)

class BasicValuedFeatureEncoder(AbstractFeatureEncoder):
    """
    A feature encoder for simple-valued features, that encodes the
    feature as a boolean L{SparseList}.  Each index in this list
    corresponds to a single feature value, and is true iff the feature
    has that value.  An extra index position is also reserved for
    unseen values, and is true iff the feature has a value that does
    not correspond to any other index.
    """
    def raw_encode_features(self, features):
        # If the feature isn't defined, return an empty feature vector.
        if self._feature_name not in features:
            return SparseList({}, self.num_features(), 0)

        # Find the index corresponding to the feature value.
        feature_value = features[self._feature_name]
        index = self._val_to_index.get(feature_value, 0) # 0 = unseen
        return SparseList({index:True}, self.num_features(), False)
    
class SetValuedFeatureEncoder(AbstractFeatureEncoder):
    """
    A feature encoder for collection-valued features, that encodes the
    feature as a boolean L{SparseList}.  Each index in this list
    corresponds to a single simple value, and is true iff the feature
    contains that value.  An extra index position is also reserved for
    unseen values, and is true iff the feature contains a value that
    does not correspond to any other index.
    """
    def raw_encode_features(self, features):
        # If the feature isn't defined, return an empty feature vector.
        if self._feature_name not in features:
            return SparseList({}, self.num_features(), 0)
        
        # For each value in the set, set the corresponding vector value
        # to True.
        assigns = {}
        for basic_value in features[self._feature_name]:
            index = self._val_to_index.get(basic_value, 0) # 0 = unseen
            assigns[index] = True
        return SparseList(assigns, self.num_features(), False)

class BagValuedFeatureEncoder(AbstractFeatureEncoder):
    """
    A feature encoder for collection-valued features, that encodes the
    feature as an integer L{SparseList}.  Each index in this list
    corresponds to a single simple value, and its value is equal to
    the number of times the feature contains that value.  An extra
    index position is also reserved for unseen values, and is equal to
    the number of times that the feature contains values that do not
    correspond to any other index.
    """
    def raw_encode_features(self, features):
        # If the feature isn't defined, return an empty feature vector.
        if self._feature_name not in features:
            return SparseList({}, self.num_features(), 0)
        
        # For each value in the set, increment the corresponding vector.
        assigns = {}
        for basic_value in features[self._feature_name]:
            index = self._val_to_index.get(basic_value, 0) # 0 = unseen
            assigns[index] = assigns.get(index,0) + 1
        return SparseList(assigns, self.num_features(), 0)

def _get_val_type(val):
    if isinstance(val, (str, int)):
        return 'basic'
    else:
        # It's a container; make sure it only contains basic values.
        for subval in val:
            if _get_val_type(subval) != 'basic':
                raise ValueError
        # Check what type of container it is.
        if isinstance(val, tuple):
            return 'basic'
        elif isinstance(val, BaseSet):
            return 'set'
        elif isinstance(val, (list, SparseList)):
            return 'bag'
        else:
            raise ValueError
        
def learn_encoder(tokens, unseen_cutoff=0, **property_names):
    """
    A helper function that automatically creates a feature detector
    from a list of example tokens.

    list -> BagValued
    set -> SetValued
    basic -> BasicValued
    
    """
    FEATURES = property_names.get('FEATURES', 'FEATURES')

    # Count the number of times each feature value occurs for
    # each feature name.
    fval_counts = {} # fname -> fval -> count
    fval_types = {} # fname -> ('basic' or 'set' or 'bag')
    for token in tokens:
        for (fname, fval) in token[FEATURES].items():
            # Check the feature's value type.  
            try: fval_type = _get_val_type(fval)
            except ValueError:
                raise ValueError('Unsupported value type for '+fname)
            if (fval_types.setdefault(fname, fval_type) != fval_type):
                raise ValueError('Inconsistant value types for '+fname)

            # Update the counts of the basic values
            counts = fval_counts.setdefault(fname, {})
            if fval_type == 'basic':
                counts[fval] = counts.get(fval,0) + 1
            else:
                for subval in fval:
                    counts[subval] = counts.get(subval,0) + 1

    # Create an encoder for each feature name.
    encoders = []
    for (fname, counts) in fval_counts.items():
        # Extract the list of values whose counts are high enough.
        fvals = [fval for (fval, count) in counts.items()
                 if count > unseen_cutoff]
        # If no values are left, then ignore this feature.
        if not fvals: continue
        # Create the feature encoder
        if fval_types[fname] == 'basic':
            enc = BasicValuedFeatureEncoder(fname, fvals)
        elif fval_types[fname] == 'set':
            enc = SetValuedFeatureEncoder(fname, fvals)
        elif fval_types[fname] == 'bag':
            enc = BagValuedFeatureEncoder(fname, fvals)
        else:
            assert False, 'Bad feature value type'
        encoders.append(enc)
    # [XX] property name indirection??
    return MergedFeatureEncoder(encoders, **property_names)

######################################################################
## Demo
######################################################################

def demo():
    import lib.nltk.corpus

    # Load the training data, and split it into test & train.
    text = lib.nltk.corpus.brown.read('cr01', add_contexts=True)
    toks = text['WORDS']
    split = len(toks) * 3/4
    train, test = toks[:split], toks[split:]

    # Create the feature detector.
    from lib.nltk.feature.word import BagOfContextWordsFeatureDetector
    detector = MergedFeatureDetector(
        PropertyFeatureDetector('TEXT'),
        PropertyFeatureDetector('TAG'),
        BagOfContextWordsFeatureDetector(window=2))

    # Run feature detection on the training data.
    for tok in train:
        detector.detect_features(tok)

    # Build a feature encoder, based on the training data.
    encoder = learn_encoder(train, unseen_cutoff=0)

    # Run the feature encoder on the test data.
    for tok in test[:10]:
        print 'Input token:   ', tok.exclude('CONTEXT')
        detector.detect_features(tok)
        items = tok['FEATURES'].items()
        print ('Feature dict: {' + 
               (',\n'+16*' ').join(['%r: %r' % i for i in items]) +
               ' }')
        encoder.encode_features(tok)
        print 'Feature vector:',
        assignments = tok['FEATURE_VECTOR'].assignments()
        assignments.sort()
        print ', '.join(['v[%d]=%d' % (index, val)
                         for index, val in assignments])
        print

if __name__ == '__main__': demo()
