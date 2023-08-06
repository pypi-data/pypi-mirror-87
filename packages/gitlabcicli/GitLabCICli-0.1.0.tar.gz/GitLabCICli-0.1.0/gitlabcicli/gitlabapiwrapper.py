"""A small and simple GitLab API wrapper."""

import requests

from gitlabcicli.script_helpers import debug, error

try:
    from hyper.contrib import HTTP20Adapter
except ImportError:
    HTTP20Adapter = None

API4 = "/api/v4/"


class GitLabApiClient:
    """An API Client for the GitLab API."""

    def __init__(self, server_url: str, token: str):
        self.server_url = server_url
        self.session = requests.Session()
        self.session.headers["PRIVATE-TOKEN"] = token
        if HTTP20Adapter:
            self.session.mount(self.server_url, HTTP20Adapter())

    @classmethod
    def _check_response(cls, response, default):
        """
        Check if the api response is a error message and prints the message.

        Return the response json as dict if there is no error.
        """
        try:
            api = response.json()
        except Exception:
            debug("No JSON in response", 4)
            debug(response.text, 5)
            api = None
        debug(api, 5)
        if not response.ok or api is None:
            if isinstance(api, dict) and "message" in api.keys():
                error(api["message"])
            elif isinstance(api, dict) and "error_description" in api.keys():
                error(api["error_description"])
            else:
                error(f"Server Error. Received status {response.status_code}")
            return default
        return api

    def _request(self, url, method="GET", **kwargs):
        """Make a requests."""
        apiurl = f"{self.server_url}{url}"
        debug(f"{method} {apiurl}", 5)
        if method == "GET":
            return self.session.get(apiurl, **kwargs)
        elif method == "POST":
            return self.session.post(apiurl, **kwargs)
        else:
            raise NotImplementedError(f"Method {method} is not implemented.")

    def _get(self, url, **kwargs):
        """Make a GET requests."""
        return self._request(url=url, method="GET", **kwargs)

    def _get_api(self, apiurl, default_return_value=None, **kwargs):
        """Make a GET Request and check returned json."""
        return GitLabApiClient._check_response(
            self._get(url=f"{API4}{apiurl}", **kwargs),
            default=default_return_value,
        )

    def _post_api(self, apiurl, default_return_value=None, **kwargs):
        """Make a POST Request and check returned json."""
        return GitLabApiClient._check_response(
            self._request(url=f"{API4}{apiurl}", method="POST", **kwargs),
            default=default_return_value,
        )

    def get_pipeline_for_commit(self, project_id, commit_hash):
        """Return the pipeline id for the commit in project on server"""
        commit = self._get_api(
            apiurl=f"projects/{project_id}/repository/commits/{commit_hash}/",
            default_return_value={},
        )
        try:
            pipeline_id = (
                commit["last_pipeline"]["id"] if commit["last_pipeline"] else None
            )
            debug(f"Pipeline ID for commit {commit_hash} is {pipeline_id}", 5)
        except KeyError:
            pipeline_id = None
        return pipeline_id

    def get_pipeline_jobs(self, project_id, pipeline_id):
        """Return a list of jobs for a pipeline."""
        jobs = self._get_api(
            apiurl=f"projects/{project_id}/pipelines/{pipeline_id}/jobs/",
            default_return_value=[],
        )
        return jobs

    def get_job_for_id(self, project_id, job_id):
        """Return the job for the given job id"""
        job = self._get_api(
            apiurl=f"projects/{project_id}/jobs/{job_id}",
            default_return_value={},
        )
        return job

    def _get_raw_job(self, project_path, job_id):
        """Return the raw job output"""
        response = self._get(url=f"{project_path}/-/jobs/{job_id}/raw")
        debug(response.text, 5)
        if not response.ok:
            if response.status_code == 404:
                error(f"No log for job {job_id} found.")
                return ""
            else:
                error(
                    f"Could not get raw job log. Received status code {response.status_code}"
                )

        return response.text

    def get_raw_job_increment(self, project_path, job_id, oldraw=""):
        """Return the raw job output incremental to oldraw"""
        newraw = self._get_raw_job(project_path, job_id)
        return newraw.replace(oldraw, "")

    def get_project_path(self, project_id):
        """Return the full path with namespace for the project with id `project_id`."""
        if not str(project_id).isnumeric:
            debug("interpreting project_id as path.", 4)
            return str(project_id)

        project = self._get_api(
            apiurl=f"projects/{project_id}/",
            default_return_value={},
        )
        return project.get("path_with_namespace", None)

    def get_project_id(self, project):
        """Return the id for the project on server"""
        if project.isnumeric():
            debug("interpreting project argument as id.", 3)
            return int(project)

        query = project.split("/", 2)[-1]
        api = self._get_api(
            apiurl=f"projects/?search={query}",
            default_return_value=[],
            params={"order_by": "last_activity_at", "sort": "desc"},
        )
        for apiproj in api:
            if apiproj["path_with_namespace"] == project:
                pid = apiproj["id"]
                debug(f'Project ID for "{project}" is {pid}', 4)
                return pid
        error(f'Project "{project}" not found on server "{self.server_url}"!')
        return -1

    def get_project_url(self, project_id: int):
        """Return the http url for the project with id `project_id`."""
        project = self._get_api(
            apiurl=f"projects/{project_id}/",
            default_return_value={},
        )
        return project.get("web_url", None)

    def run_action_on_job(self, action, project_id, job_id):
        """Run action (cancel, retry, erase) on job"""
        return self._post_api(
            apiurl=f"projects/{project_id}/jobs/{job_id}/{action}",
            default_return_value={},
        )

    def validate_ciyml(self, gitlabciyml_text):
        """Return:
        valid:
            {"status": "valid", "errors": []}
        invalid:
            {"status": "invalid", "errors": ["description 1", "description 2"]}
        error:
            {"error": "description"}
        """
        api = self._post_api(
            apiurl="/ci/lint",
            default_return_value={"error": "request failed"},
            data={"content": gitlabciyml_text},
        )
        if "error" in api.keys():
            error(api["error"])
        elif (
            "status" not in api.keys()
            or "errors" not in api.keys()
            or api["status"] not in ["valid", "invalid"]
        ):
            debug(api, 4)
            error("Invalid response from api")
        else:
            return api
