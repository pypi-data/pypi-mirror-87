# synth-tree

An efficient additive synthesis library. Simple, clean, and very
typechecker-friendly; it might not be ideal for production, but
the code within might be interesting to the prying eye!

Internally, it uses a binary tree representation to quickly cull
away contiguous regions of zero parameters (that is, silent
sine waves, in practice equivalent to no-op).

It comes with a class to read a PCM stream, as a read-only
io.RawIOBase subclass. It also allows exporting to .WAV,
and both serializing and deserializing TreeSynths with all
parameters into a future-proof (version checking enabled)
binary format. Talk about standing the test of time!

## How to use

After you install it (using pip or setup.py), you can simply use
the TreeSynth class, use a index syntax (like a list) to set
values, including ranges thereof using slice syntax, and then
you use call syntax (like a function) to obtain values.

```py
>>> import synthtree
>>> synth = synthtree.SynthTree()
>>> synth.values[90] = 0.5  # this is where the binary tree is constructed!
>>> synth(20)
-0.1950903220149695
```

Note that if you set one single value, the result will be one single sine wave.
Which is kind of boring. But that's because you only set **one** value!

Think of each index into the synthesizer as its own sine wave oscillator, and
the corresponding value as the amplitude. Negative values simply invert the
phase! The more values you set, the more interesting the wave. Hooray!

But let's suppose you got the most awesome wave ever imaginable. There's only
one issue... you can't *really* hear it now, can you? Well, you can! Simply export
it to WAV:

```
>>> my_cool_synth.export_wav('my_cool_wave.wav')
```

The default samplerate is 44.1 kHz (44100 Hertz), and by default the volume is halved
to protect your ears from potential fun arising from setting ridiculous values and
parameters. You can use the `amplitude` keyword argument to change that, **but use it
at your own discretion!**

What? You want to save the parameters you set so you can reuse them later? Simple!
You don't need to lug it around like a disgusting sack of pickles.
([Pun intended.](https://docs.python.org/3.8/library/pickle.html))
Simply use `SynthTree.dump()` to get your data in a sexy binary serialization format!
Hayo!

```
>>> data = my_cooler_synth.dump() 
```

Once you have your serialized data, you can write it to a file. Then, the next morning,
you wake up, feel the Need for Synth rushing in your veins again, and load it back into
a SynthTree!...actually, a tuple, containing your loaded SynthTree and any surplus data.
The latter is for convenience purposes for in case you're loading SynthTrees directly from
a byte stream or a larger file (which you probably shouldn't), but if you used `dump`
then it should be empty, so you may safely discard that, e.g. using the syntax demonstrated in the
second REPL statement of the example below. *Note the comma!*

```
>>> synthtree.SynthTree.load(data)
(<synthtree.synth.SynthTree object at 0x7ff99fca5df0>, b'')
>>> my_cooler_synth_again, _ = synthtree.SynthTree.load(data) # Again, note the comma! See? *Now* you saw it, silly!
>>> my_cooler_synth_again
<synthtree.synth.SynthTree object at 0x7ff99fcb46a0>
```

You can also use `synthtree.PCMStream` to get a raw PCM stream as a read-only file-like
object, and use it for whatever. Cool!

```
>>> stream = synthtree.PCMStream(my_super_cool_synth)
>>> pcm = stream.read(8192)
>>> # Step 3: ???
>>> # Step 4: Profit!
```
