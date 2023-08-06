

.. image:: https://raw.githubusercontent.com/life4/deal/master/logo.png
   :target: https://raw.githubusercontent.com/life4/deal/master/logo.png
   :alt: Deal

================================================================================================================================================================


.. image:: https://travis-ci.org/life4/deal.svg?branch=master
   :target: https://travis-ci.org/life4/deal
   :alt: Build Status


.. image:: https://coveralls.io/repos/github/life4/deal/badge.svg
   :target: https://coveralls.io/github/life4/deal
   :alt: Coverage Status


.. image:: https://img.shields.io/pypi/v/deal.svg
   :target: https://pypi.python.org/pypi/deal
   :alt: PyPI version


.. image:: https://img.shields.io/pypi/status/deal.svg
   :target: https://pypi.python.org/pypi/deal
   :alt: Development Status


**Deal** -- python library for `design by contract <https://en.wikipedia.org/wiki/Design_by_contract>`_ (DbC) and checking values, exceptions, and side-effects. Read `intro <https://deal.readthedocs.io/basic/intro.html>`_ to get started.

Features
--------


* `Classic DbC: precondition, postcondition, invariant. <https://deal.readthedocs.io/basic/values.html>`_
* `Tracking exceptions and side-effects. <https://deal.readthedocs.io/basic/exceptions.html>`_
* `Property-based testing. <https://deal.readthedocs.io/basic/tests.html>`_
* `Static checker. <https://deal.readthedocs.io/basic/linter.html>`_
* Integration with pytest, flake8, and hypothesis.
* Type annotations support.
* `External validators support. <https://deal.readthedocs.io/details/validators.html>`_
* `Contracts for importing modules. <https://deal.readthedocs.io/details/module_load.html>`_
* `Can be enabled or disabled on production. <https://deal.readthedocs.io/basic/runtime.html>`_
* `Colorless <colorless>`_\ : annotate only what you want. Hence, easy integration into an existing project.
* Colorful: syntax highlighting for every piece of code in every command.
* `Memory leaks detection. <https://deal.readthedocs.io/basic/tests.html#memory-leaks>`_ Deal makes sure that a pure function doesn't leave unexpected objects in the memory.
* DRY: test discovery, error messages generation.
* Partial execution: linter executes contracts to statically check possible values.

Deal in 30 seconds
------------------

.. code-block:: python

   # the result is always non-negative
   @deal.post(lambda result: result >= 0)
   # the function has no side-effects
   @deal.pure
   def count(items: List[str], item: str) -> int:
       return items.count(item)

   # test case
   @pytest.mark.parametrize('case', deal.cases(count))
   def test_count(case: deal.TestCase):
       case()

Now we can:


* Run ``python3 -m deal lint`` or ``flake8`` to statically check errors.
* Run ``python3 -m deal test`` or ``pytest`` to generate and run tests.
* Just use the function in the project and check errors in runtime.

Read more in the `documentation <https://deal.readthedocs.io/>`_.

Installation
------------

.. code-block:: bash

   python3 -m pip install --user deal

Contributing
------------

Contributions are welcome! A few ideas what you can contribute:


* Add new checks for the linter.
* Improve documentation.
* Add more tests.
* Improve performance.
* Found a bug? Fix it!
* Made an article about deal? Great! Let's add it into the ``README.md``.
* Don't have time to code? No worries! Just tell your friends and subscribers about the project. More users -> more contributors -> more cool features.

Thank you :heart:
