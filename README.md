# M3D-Fio-Perf: Performance experiments for `M3D-Fio`

This is meant to be cloned next to your `M3D-Fio` repo, so that 

`python m3dfio.py t1.gcode`

knows where to find `M3D-Fio`. 

## m3dfio.py and octoprint

`m3dfio.py` takes a path to a GCode input file on the command line, and uses the dummy `octoprint` module to run the `M3D-Fio` module code against it.  Obviously it doesn't print anything. :)  It does, however, make it a lot easier to see and profile what's happening.

The `octoprint` dummy module has effectively no functionality.  It's just stubs to allow the `M3D-Fio` plugin to run.

Presumably it'd work for other plugins too.  Maybe.  If you're lucky.

## 1-regex.py and friends

These run _without_ using any plugin madness, as a way to isolate the effect of different algorithms.  I've been playing with these on two platforms: my MacBook Air is a mid-2012 with a 2GHz Core 17, and my Raspberry Pi is a Model B that says (c)2011.12 on it -- not sure what version that is.

- On the Air, I ran these as `time python _whatever.py_ t1.gcode > out_num_.txt`.
- On the RPi, I ran these as `time ~/oprint/bin/python _whatever.py_ t1.gcode > out_num_.txt`.

In theory, it should be possible to compare the output from a given experiment to another other. In practice, I only bothered trying `2-initialM3DFio.py` and `4-splitWhitespace.py`, since they're the only ones where I've made correctness a priority.

#### 1-justScan.py

`1-justScan.py` scans the GCode file and uses a regex to split each line into elements.  *DOES NOT WORK* in that it doesn't parse `M28` and friends correctly; it's here as a performance baseline, since all the work should be happening in C.

- Air: 1.73s
- RPi: 41.9s

(The Air has a 2GHz CPU and an SSD.  I'm a little concerned that it's only 20x as fast as the Pi...)

#### 2-initialM3DFio.py

`2-initialM3DFio.py` runs pretty much the same parsing code as M3D-Fio from my fork.

- Air: 9.7s
- RPi: 228s

Holding at around 20x.  Good, I guess.

#### 3-recursiveDescent.py

`3-recursiveDescent.py` is an experiment with a recursive-descent parser. Easy to try but too slow and thankfully (since GCode dictates the whitespace between elements from what I see), unnecessary.

- Air: 10.7s
- RPi: 345s

Note that we've gone to a 30x difference here.

#### 4-splitWhitespace.py

`4-splitWhitespace.py` splits each line into whitespace and processes from there. It parses `M28` and friends and might even get binary correct, though I haven't tested that yet, and uses a dict to track parameters.

- Air: 4.74s
- RPi: 115s

Still 30x, but dramatically better than 2 or 3, and similar to the Air's 3x slowdown between 1 and 4.




