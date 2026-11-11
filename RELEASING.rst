Here are the steps on how to make a new release.

1. Create a ``release-VERSION`` branch from ``upstream/master``.
2. Update ``CHANGELOG.rst``: rename the ``UNRELEASED`` section to ``VERSION``, and replace ``*UNRELEASED*`` with the release date.
3. Push the branch to ``upstream`` and open a PR from ``release-VERSION`` to ``master``.
   Pushing the branch alone does not run CI; the tests run on the PR.
4. Once all tests pass, start the ``deploy`` workflow manually or via command-line::

    gh workflow run deploy.yml --ref release-VERSION --field version=VERSION

   The ``deploy`` job runs in the ``deploy`` environment, so it waits until a maintainer approves it in the Actions tab.
5. The workflow merges the PR at the end, using a merge commit (not squash), so the tagged commit ends up in ``master``.
   If that step fails, merge the PR manually the same way.
