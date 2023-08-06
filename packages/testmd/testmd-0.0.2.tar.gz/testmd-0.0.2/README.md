# testmd

testmd is a python package and command line utility to perform tests against
markdown frontmatter.

This can be used to ensure that fields like `title` and `date` are set and
perform some simple validations against content.

In particular this can be useful for defining and then checking for documents
that have 'expired'.

When used in conjunction with scheduled CI, this can provide a useful mechanism
for tracking and maintaining up-to-date documentation or other types of content.
