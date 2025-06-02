Here are the steps on how to make a new release.

1. Create a ``release-VERSION`` branch from ``upstream/master``.
2. Update ``CHANGELOG.rst``.
3. Push the branch to ``upstream``.
4. Once all tests pass, start the ``deploy`` workflow manually or via command-line::

    gh workflow run deploy.yml --ref release-VERSION --field version=VERSION

5. Merge the PR.
