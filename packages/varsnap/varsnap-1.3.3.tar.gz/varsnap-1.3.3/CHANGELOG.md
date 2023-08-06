Changelog
=========

1.3.3 (2020-12-05)
------------------

 - Support assigning Trials to TrialGroups


1.3.2 (2020-12-05)
------------------

 - Update dependencies
 - Optimizations and tests


1.3.1 (2020-07-16)
------------------

 - Send formatted trial outputs to Varsnap backend
 - Added tests
 - Dependency updates


1.3.0 (2020-06-30)
------------------

 - Removed deprecated TestVarsnap unittest class
 - Fix mypy issue around implicit imports


1.2.2 (2020-06-28)
------------------

 - Fix compatibility with @staticmethod functions
 - Fix working correctly on functions that mutate inputs
 - Make varsnap annotations available for importers


1.2.1 (2020-06-20)
------------------

 - Switch testing comparator to reuse the python built-in unittest library
 - Refactors


1.2.0 (2020-06-19)
------------------

 - `TestVarsnap` is now deprecated.  Use `test()` instead.
 - Refactors around testing
 - Logging updates
 - Enable mypy type linting in strict mode
 - Dependency updates


1.1.4 (2020-06-14)
------------------

 - Refactor out testing logic from TestVarsnap
 - Backfill a lot of testing


1.1.3 (2020-06-07)
------------------

 - Fix comparison of exception values
 - Fix invalid false negatives when running tests
 - Refactors


1.1.2 (2020-06-06)
------------------

 - Officially add support for python 3.8
 - Add a test.sh script
 - Update dependncies
 - Clean up python package files


1.1.1 (2020-01-24)
------------------

 - Update dependencies
 - Remove consume_watch
 - Remove dependency on mock package


1.1.0 (2020-01-13)
------------------

 - Remove consuming and exporting global variables
 - Add orig_function into varsnap-wrapped function
 - Update dependencies


1.0.1 (2019-12-31)
------------------

 - Switch from pickle to dill for serialization/deserialization
 - Better logging of serialization issues


1.0.0 (2019-12-27)
------------------

 - Dropped python 2 support


0.9.0 (2019-12-23)
------------------

 - Limited length of debug string in test output
 - Fixed flaky test case
 - Updated dependencies


0.8.4 (2019-11-17)
------------------

 - Downcase VarSnap to Varsnap
 - Update deprecated endpoint call


0.8.3 (2019-10-18)
------------------

 - Show test url in test results
 - Consume and test multiple Snap results
 - Add mypy type hints
 - Update dependencies
 - Cleanup


0.8.2 (2019-09-30)
------------------

 - Fix backwards compatibility of 0.8.1
 - Make DeserializeError cover additional exceptions
 - Dependency udpates


0.8.1 (2019-09-22)
------------------

 - Add SerializeError and DeserializeError
 - Make sure trial output data is serialized
 - Various refactors


0.8.0 (2019-09-08)
------------------

 - Clean up tests
 - Report test results to Varsnap
 - Make sure raised exceptions are being compared correctly
 - Better handling of unpickling errors when consuming Snaps


0.7.2 (2019-08-14)
------------------

 - Add more explicit testing output


0.7.1 (2019-08-13)
------------------

 - Be able to work with generic pickle errors


0.7.0 (2019-08-10)
------------------

 - Stop logging when running tests
 - Switch from running tests with background environment to running tests with unittest TestCase


0.6.1 (2019-08-06)
------------------

 - Fix pickle issues
 - Simplify loading globals


0.6.0 (2019-08-05)
------------------

 - Add TestVarsnap unittest test case


0.5.4 (2019-08-04)
------------------

 - Refactors
 - Clean up logging during testing
 - Dependency updates


0.5.3 (2019-07-28)
------------------

 - Add logic to do a deep equal when consuming inputs
 - Consume, compare and show exceptions


0.5.2 (2019-07-27)
------------------

 - Make varsnap decorator not change function name


0.5.1 (2019-07-21)
------------------

 - Add support for snapping global variables
 - Add support for batch consume
 - Fix python 2 support
 - Update dependencies


0.5.0 (2019-06-22)
------------------

 - Add ability to produce snaps with function signatures
 - Add ability to consume snaps filteed by function signatures


0.4.0 (2019-06-19)
------------------

 - Switched to using `VARSNAP_PRODUCER_TOKEN` and `VARSNAP_CONSUMER_TOKEN`
 - Updated varnsap api endpoints.


0.3.1 (2019-06-17)
------------------

 - Clean up reporting varsnap status
 - Switch from print statements to logger


0.3.0 (2019-06-17)
------------------

 - Added tests
 - Removed serialize and deserialize functions for importing
 - Cleaned up thread exiting
 - Run all new snaps, not just those with different inputs


0.2.1 (2019-06-15)
------------------

 - Fix env var lookups


0.2.0 (2019-06-15)
------------------

 - Support python 2 (by switching from asyncio to threading)
 - Fix reading environment variables by deferring the read to runtime


0.1.0 (2019-06-09)
------------------
 - Pass auth token when getting snaps


0.0.1 (2019-06-08)
------------------
 - Initial release
