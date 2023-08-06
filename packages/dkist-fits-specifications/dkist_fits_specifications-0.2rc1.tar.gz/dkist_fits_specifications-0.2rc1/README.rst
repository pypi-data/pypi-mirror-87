Machine readable FITS specifications for DKIST data.
----------------------------------------------------

This repository contains machine readable versions of DKIST specifications for
FITS files. Specifically corresponding to specs 122 (level 0) and 214 (level 1)
data.

Usage
-----


This repository contains machine readable versions of DKIST specifications 122 (level 0 FITS files) and 214 (level 1 FITS files).
There are two submodules `spec122` and `spec214`, they respectively provide a `load_spec122()` and a `load_spec214()` function which returns the "simple" schema for both specifications.
The `spec214` module also provides a `load_full_spec214()` function which provides extra metadata on the schema designed for generation of the 214 documentation.


License
-------

This project is Copyright (c) AURA/NSO and licensed under
the terms of the BSD 3-Clause license. This package is based upon
the `Openastronomy packaging guide <https://github.com/OpenAstronomy/packaging-guide>`_
which is licensed under the BSD 3-clause licence. See the licenses folder for
more information.


Contributing
------------

We love contributions! dkist-fits-specifications is open source,
built on open source, and we'd love to have you hang out in our community.

**Imposter syndrome disclaimer**: We want your help. No, really.

There may be a little voice inside your head that is telling you that you're not
ready to be an open source contributor; that your skills aren't nearly good
enough to contribute. What could you possibly offer a project like this one?

We assure you - the little voice in your head is wrong. If you can write code at
all, you can contribute code to open source. Contributing to open source
projects is a fantastic way to advance one's coding skills. Writing perfect code
isn't the measure of a good developer (that would disqualify all of us!); it's
trying to create something, making mistakes, and learning from those
mistakes. That's how we all improve, and we are happy to help others learn.

Being an open source contributor doesn't just mean writing code, either. You can
help out by writing documentation, tests, or even giving feedback about the
project (and yes - that includes giving feedback about the contribution
process). Some of these contributions may be the most valuable to the project as
a whole, because you're coming to the project with fresh eyes, so you can see
the errors and assumptions that seasoned contributors have glossed over.

Note: This disclaimer was originally written by
`Adrienne Lowe <https://github.com/adriennefriend>`_ for a
`PyCon talk <https://www.youtube.com/watch?v=6Uj746j9Heo>`_, and was adapted by
dkist-fits-specifications based on its use in the README file for the
`MetPy project <https://github.com/Unidata/MetPy>`_.
# Specification for DKIST FITS Files
