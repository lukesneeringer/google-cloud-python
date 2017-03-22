# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings


class Results(object):
    """A class wrapping a particular query job which can retrieve results.

    This class is essentially a wrapper around a
    :class:`google.cloud.bigquery.job.QueryJob` which is able to fetch its
    results; the use of the wrapper class ensures that results are present
    before fetching, and nearly separates job execution from inspection of
    results.

    This object is returned from :method:`QueryJob.results` and
    :method:`QueryJob.join`. You should not need to construct it directly.

    :type job: :class:`google.cloud.bigquery.job.QueryJob`
    :param job: The job this instance wraps.
    """
    def __init__(self, job):
        self.job = job

    @property
    def project(self):
        """Project bound to the job.

        :rtype: str
        :returns: the project (derived from the job).
        """
        return self.job.project


    # ----------------------------------
    # Deprecated / Compatibility Methods
    # ----------------------------------
    def __call__(self):
        """Return self.

        This method is provided to maintain compatibility with calling
        `QueryJob.results()` instead of `QueryJob.results`, and is deprecated.
        """
        warnings.warn('`QueryJob.results` is now a property, not a method.',
                      DeprecationWarning)
        return self

    def run(self):
        """Return a :class:`google.cloud.bigquery.query.QueryResults` instance.

        This method is provided to maintain compatibility with the deprecated
        code path of using client.run_sync_query(), which returned a
        :class:~`google.cloud.bigquery.query.QueryResults` object, which then
        had to manually have .run() called on it.

        Now, client.run_sync_query(), which is itself now deprecated, returns
        a :class:`google.cloud.bigquery.query.QueryJob` object, on which it
        calls .join(), which returns a
        :class:~`google.cloud.bigquery.query.Results`.

        The bottom line is: You should never actually call this method anymore,
        and it is here to make a deprecated code path work correctly.
        """
        warnings.warn('The Results.run method is deprecated.',
                      DeprecationWarning)
        return QueryResults.from_query_job(job)
