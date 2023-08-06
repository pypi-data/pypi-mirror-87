"""
Simple proof-of-concept for additive synthesis of a
digital signal including culling of contiguous silent regions
('zero regions') via a binary tree structure.
"""

import io
import typing
import abc
import math
import wave
import struct
import array


try:
    import numpy as np
    
    HAS_NUMPY = True

except ImportError:
    HAS_NUMPY = False



class SynthNodeType(typing.Protocol):
    def update(self):
        """
        Updates this node.
        """
        pass
    
    def deinit(self):
        """
        Deinitializes this node.
        """
        pass

    def __call__(self, pos: float) -> float:
        """
        Produces a sample for a given position.
        """
        pass


class SynthTree:
    """
    SynthTree is the overall tree of sine wave oscillators.
    Additive synthesis is the synthesis and formation of
    a sound wave by adding many different frequencies of
    sine waves together. The amplitude of each wave is
    the paramemter that is used by an additive synthesizer,
    and the result is the addition of all these waves together;
    hence additive synthesis.

    This implementation uses a binary tree divide-and-conquer
    strategy for performance. It assumes that most parameters
    won't actually be set, and will remain at the default of
    zero. If that is not true, it is instead suggested to use a
    vectorizable, iterative rather than recursive, method --
    preferably in a performant language like C, even if it means
    needing a little glue code to integrate it with your existing
    application, although portable solutions do exist, such as
    embedding Lua directly.

    Use an index syntax (like a list's) to set/get parameters, and
    call syntax (like a function's) to get the result for a given
    position in time t.
    """

    SERIALIZATION_VERSION: int = 1
    SERIALIZATION_TAG: str = 'SYNTH TREE'

    def __init__(self, min_freq: float = 2.0, max_freq: float = 22050.0, resolution: int = 4096):
        """
        Initializes a synth tree. This will also by default initialize all parameters
        to zero; if you try to get (or listen to) a wave from a newly initialized
        SynthTree, you'll get a flat line of silence.
        """
    
        self.min_freq   = min_freq 
        self.max_freq   = max_freq
        self.resolution = resolution

        self.freq_step = (max_freq - min_freq) / resolution

        self.all_nodes: typing.Set[SynthNodeType] = set()
        self.values    = [0.0 for _ in range(resolution)] 

        self._setup_nodes()

    def dump(self) -> bytes:
        """
        Serializes this SynthTree object into a binary format.
        """
    
        res = bytearray(len(self.SERIALIZATION_TAG.encode('utf-8')).to_bytes(2, 'little', signed=False) + self.SERIALIZATION_TAG.encode('utf-8') + struct.pack('HddL', self.SERIALIZATION_VERSION, self.min_freq, self.max_freq, self.resolution))

        a = array.array('d', self.values[: self.resolution]).tobytes()
        res += a

        return res

    @classmethod
    def load(cls: typing.Type['SynthTree'], data: bytes) -> typing.Tuple['SynthTree', bytes]:
        """
        Deserializes the binary representation produced by dump() back
        into a SynthTree. Returns a size 2 tuple containing the resulting
        loaded SynthTree alongside all remaining data.
        """

        tagsize_l = 2
        tag_l, = struct.unpack('H', data[: tagsize_l])

        head_l = 2 + tag_l + struct.calcsize('HddL')
        value_l = struct.calcsize('d')

        ser_tag = data[tagsize_l : tagsize_l + tag_l].decode('utf-8')

        ser_version, min_freq, max_freq, resolution = struct.unpack('HddL', data[tag_l + tagsize_l : head_l])

        if ser_tag != cls.SERIALIZATION_TAG:
            raise ValueError("{} SynthTree serialization tag mismatched -- expected {}, got {}".format(cls.__name__, repr(cls.SERIALIZATION_TAG), repr(ser_tag)))

        if ser_version != cls.SERIALIZATION_VERSION:
            raise ValueError("{} SynthTree serialization version mismatched -- expected {}, got {}".format(cls.__name__, cls.SERIALIZATION_VERSION, ser_version))

        # only check for sufficient data now, as insufficient data errors
        # may mask future version checks (should future versions request
        # more data than previous serialization versions would predict)
        if len(data) < head_l + value_l * resolution:
            raise ValueError('Insufficient data pased to deserialize a {} SynthTree deserializer, tag {} version {} -- expected at least {}, got {}'.format(cls.__name__, cls.SERIALIZATION_VERSION, ser_version, head_l + value_l * resolution, len(data)))
    
        loaded = cls(min_freq, max_freq, resolution)
        
        loaded.values = list(array.array('d', data[head_l : head_l + value_l * resolution]))
        loaded.refresh()

        return loaded, data[head_l + value_l * resolution :]

    def export_wav(self, target: typing.Union[str, typing.BinaryIO], length: float = 5.0, sample_rate: int = None, sample_type: str = 'H', amplitude: float = 0.5):
        """
        Exports the signal synthesized by this SynthTree into
        a wave audio file. str can be either a filename or
        a file object supported by wave.open.
        """
    
        sample_rate = sample_rate or int(self.max_freq * 2)

        sample_width = struct.calcsize(sample_type)
        limit = 2. ** (8 * sample_width) - 1.

        num_frames = int(sample_rate * length)

        with wave.open(target, 'wb') as fp:
            fp.setnchannels(1)
            fp.setsampwidth(sample_width)
            fp.setframerate(sample_rate)
            fp.setnframes(num_frames)

            if HAS_NUMPY:
                wsamples = np.linspace(0., length, num_frames)

                # transform wsamples by calling self
                wsamples = np.vectorize(self)(wsamples)

                # alias to integer bounds
                wsamples -= min(wsamples)
                wsamples /= max(wsamples)
                wsamples -= 0.5
                wsamples *= limit * amplitude

                # convert to array of integers
                encoded = array.array(sample_type.upper(), wsamples.astype(sample_type.upper()))

                # write!
                fp.writeframes(encoded.tobytes())

            else:
                # more iterative, but also slower
                wsamples = []

                # find samples, without normalization
                for pos in range(0, num_frames + 1):
                    secs = pos / sample_rate
                    wsamples.append(self(secs))

                # normalize
                mi, ma = min(wsamples), max(wsamples)
                span = ma - mi

                # pack 
                encoded = array.array(sample_type.upper(), (int(((sample - mi) / span - 0.5) * limit * amplitude) for sample in wsamples))

                # write!
                fp.writeframes(encoded.tobytes())

    def duplicate(self: 'SynthTree') -> 'SynthTree':
        """
        Returns a duplicate version of this SynthTree.

        Subclass instances will duplicate to their own subclass,
        rather than to SynthTree.
        """

        duplicate: 'SynthTree' = type(self)(self.min_freq, self.max_freq, self.resolution)

        duplicate.values = list(self.values)
        duplicate.refresh()

        return duplicate

    def __setitem__(self, index: int, value: float):
        self.values[index] = value

        # Update node structure.
        self.refresh()

    def __getitem__(self, index: int) -> float:
        return self.values[index]

    def __call__(self, pos: float) -> float:
        if not self.root:
            return 0.0
    
        return self.root(pos)

    def print_tree(self):
        """
        Prints a pretty tree to the terminal because why not.
        Ooo, pretty.
        """

        print(' * root')

        stack = [(self.root, 0, 0, self.resolution)]

        while stack:
            curr, level, imin, imax = stack.pop()
            header = '    ' * level

            if isinstance(curr, SynthNodeSplit):
                print(header + " *---+ split - range {} to {}, middle at {}".format(curr.range[0], curr.range[1], curr.split_index))

                stack.append((curr.left,  level + 1, curr.range[0], curr.split_index))
                stack.append((curr.right, level + 1, curr.split_index, curr.range[1]))

            elif isinstance(curr, SynthNodeLeaf):
                print(header + " % leaf - index {}, freq {:.2f}Hz".format(imin, curr.frequency))

            elif isinstance(curr, SynthNodeDiscard):
                print(header + " o discard - range {} to {}".format(imin, imax))

    def find_node_for(self, index: int) -> 'SynthNode':
        """
        Find the node responsible for the generation of this
        frequency index. May return a SynthNodeLeaf or a
        SynthNodeDiscard.
        """

        curr = self.root

        while True:
            if isinstance(curr, SynthNodeSplit):
                curr = curr.left if index < curr.split_index else curr.right

            else:
                return curr

    def split_for(self, start: int, end: int) -> 'SynthNode':
        """
        Creates a node (or subtree thereof, in the case
        of a SynthNodeSplit) that properly encompasses
        this section of the parameters in a lossless
        manner, and returns it.

        Do not worry about this function if you're not
        working on this library yourself.
        """

        res: SynthNode
    
        sliced = self.values[start : end]
    
        if all(x == 0.0 for x in sliced):
            # all zeros - dismissable silence
            res = SynthNodeDiscard(self)

        elif len(sliced) == 1:
            # single value - single leaf
            res = SynthNodeLeaf(self, start)

        else:
            # multiple uneven values - split
            middle = int((start + end) // 2)
        
            res = SynthNodeSplit(self, middle, (start, end))

        # Add this node to the all_nodes list.
        self.all_nodes.add(res)
        
        return res

    def refresh(self):
        """
        Destroys all nodes if they have been
        setup previously, then (re-)creates the
        binary tree structure. Also recalculates
        some other internal values.
        """

        # cap values to ensure no excess (that would be bad!)
        self.values = self.values[:self.resolution]

        if hasattr(self, 'root') and self.root:
            self.root = None
        
            for node in self.all_nodes:
                node.deinit()

            self.all_nodes = set()

        self._setup_nodes()

    def _setup_nodes(self):
        """
        Creates the binary tree structure from scratch.
        Warning: does not check for existing trees,
        just use refresh() instead!
        """
    
        self.root = self.split_for(0, self.resolution)

    def frequency(self, index: int) -> float:
        """
        Determines the frequency at a given index of the values,
        such that the first oscillator will have min_freq, and
        the last oscillator will have max_freq.

        This is called when the nodes are initialized. If you're
        not a developer messing with this code -- and why would you,
        it's a weird proof-of-concept of sorts, probably convoluted
        too --, you need not concern about this function.
        """
    
        return self.min_freq + index * self.freq_step

class PCMStream(io.RawIOBase):
    """
    This class is responsible for obtaining raw PCM data from a
    SynthTree in a consistent manner, that can later be streamed
    using a io.RawIOBase-compatible interface.
    """

    def __init__(self, synth: SynthTree, sample_rate: int = 44100, initial_pos: float = 0.0, sample_type: str = 'H', amplification: float = 0.5, signed: bool = False):
        """
        Note: To use with the 'wave' standard library module (to save WAV
        files), pass signed=True. wave only uspports writing signed samples
        for some reason.
        """
    
        self.synth          = synth

        self.pos            = initial_pos
        self.pos_bytes      = 0
        
        self.sample_rate    = sample_rate
        self.sample_type    = sample_type
        self.sample_width   = struct.calcsize(self.sample_type)
        self.sample_step    = 1.0 / self.sample_rate
        self.amplification  = min(amplification, 1.0)
        self.limit          = 2. ** (8 * self.sample_width) - 1.
        self._limiter_span  = 1.0

        self.signed         = signed

    def _sample_here(self):
        samp = self.synth(self.pos) * self.amplification

        if abs(samp) > self._limiter_span:
            self._limiter_span = abs(samp)

        samp = (samp / self._limiter_span + 1.0) * self.limit / 2.0
        samp = int(max(0, min(self.limit, samp)))

        if self.signed:
            samp -= math.ceil((self.limit + 1) / 2)

        return samp

    def read(self, size):
        if size == -1:
            raise ValueError("Blocking read would block forever! Please specify a size. -1 is for reading entire files, but THE SYNTH is forever, silly! :P")
        
        res = array.array(self.sample_type.lower() if self.signed else self.sample_type.upper())

        for i in range(size):
            res.append(self._sample_here())
            self.pos += self.sample_step
            self.pos_bytes += 1

        return res.tobytes()

    def close(self):
        pass

    def fileno(self):
        raise OSError("PCMStream does not use file descriptors.")

    def flush(self):
        pass

    def isatty(self):
        return False

    def readable(self):
        return True

    def writable(self):
        return False

    def seekable(self):
        return True

    def tell(self):
        return self.pos_bytes

    def seek(self, offset, whence):
        if whence == 0: # seek_set
            diff = offset - self.pos_bytes

            self.pos_bytes = offset
            self.pos += diff * self.sample_rate

        elif whence == 1: # seek_cur
            self.pos_bytes += offset
            self.pos += offset * self.sample_rate

        elif whence == 2: # seek_end
            raise ValueError("Cannot seek to the end of an infinite stream!")

class SynthNode:
    """
    Abstract class, defined for the sake of common behaviour
    and organisation. Inheriting this class is not necessary
    to make a class be usable as a SynthTree node, but you'll
    have to reimplement common functionality.
    """

    def update(self):
        """
        Updates this node, for whatever reason. No-op, by default.
        """
        pass
    
    def deinit(self):
        """
        Deinitializes this node. 'Nuff said.
        """
        self.tree = None

    def __call__(self, pos: float) -> float:
        """
        Included here for consistency with actual concrete
        implementations of SynthTree nodes.
        """
        raise NotImplementedError

class SynthNodeSplit(SynthNode):
    """
    A special kind of SynthTree node, that is a (usually uniform)
    split of a region of the values in two. The left and right
    areas are computed individually and then added -- because additive
    synthesis --. Those in turn can be either Discard, Leaf, or more Split
    nodes.
    """

    def __init__(self, tree: SynthTree, split_index: int, index_range: typing.Tuple[int, int]):
        self.tree = tree
        self.split_index = split_index
        self.range = index_range

        self.update()

    def update(self):
        """
        Creates (or recreates) the left and right children nodes of this
        Split node.
        """
    
        self.left  = self.tree.split_for(self.range[0], self.split_index)
        self.right = self.tree.split_for(self.split_index, self.range[1])

    def __call__(self, pos: float) -> float:
        """
        Computes the sample for the left and right children nodes, and
        adds them together.
        """
    
        return self.left(pos) + self.right(pos)

class SynthNodeDiscard(SynthNode):
    """
    A synth node that returns zero.
    This is useful, because it allows
    abstracting away the computations of
    not just single zero values, but also
    entire regions of zero values at once,
    with a single 'return zero'. It even
    skips the need for the sine function!
    """

    def __init__(self, tree: SynthTree):
        self.tree = tree

    def __call__(self, pos: float = None) -> float:
        """
        Computes the sample for a contiguous region
        of parameter zero sine-wave oscillators...
        hold on, that's just zero! :o
        """
    
        return 0.0

class SynthNodeLeaf(SynthNode):
    """
    A leaf node, that represents one single sine-wave
    oscillator.
    """

    def __init__(self, tree: SynthTree, frequency_index: int):
        self.tree = tree
        self.frequency_index = frequency_index

        self.update()

    def update(self):
        """
        Updates the frequency and frequency_rads parameters of this
        SynthNode. Those are determined automatically by the index
        this leaf occurs in. It's determined here. It also fetches
        the value from the corresponding index of the SynthTree's
        values list. Whew.

        This skips having to perform those redundant calculations
        again and again for every sample.
        """
    
        self.frequency = self.tree.frequency(self.frequency_index)
        self.frequency_rads = self.frequency * math.tau
        self.value = self.tree.values[self.frequency_index]

    def __call__(self, pos: float) -> float:
        """
        Computes the sine wave function at the given position
        and amplitude value for this oscillator and at its
        corresponding frequency, and returns the final result.
        """
    
        return math.sin(pos * self.frequency_rads * self.value)
