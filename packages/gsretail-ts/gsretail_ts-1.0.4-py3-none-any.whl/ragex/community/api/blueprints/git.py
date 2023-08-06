from typing import Text, Optional
import logging

from ragex.community import utils
from ragex.community.api.decorators import validate_schema, rasa_x_scoped
from ragex.community.constants import REQUEST_DB_SESSION_KEY
from ragex.community.services.git_service import GitService
from ragex.community.utils import error
from sanic import response, Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse

logger = logging.getLogger(__name__)


def _git(
    request: Request, project_id: Text, repository_id: Optional[int] = None
) -> GitService:
    return GitService(
        request[REQUEST_DB_SESSION_KEY],
        project_id=project_id,
        repository_id=repository_id,
    )


def blueprint() -> Blueprint:
    git_endpoints = Blueprint("git_endpoints")

    @git_endpoints.route(
        "/projects/<project_id:string>/git_repositories", methods=["GET", "HEAD"]
    )
    @rasa_x_scoped("repositories.list")
    async def get_repositories(request: Request, project_id: Text) -> HTTPResponse:
        """List all stored Git repository credentials."""

        git_service = _git(request, project_id)
        repositories = git_service.get_repositories()
        return response.json(repositories, headers={"X-Total-Count": len(repositories)})

    @git_endpoints.route(
        "/projects/<project_id:string>/git_repositories", methods=["POST"]
    )
    @rasa_x_scoped("repositories.create", allow_api_token=True)
    @validate_schema("git_repository")
    async def add_repository(request: Request, project_id: Text) -> HTTPResponse:
        """Store a new Git repository."""

        git_service = _git(request, project_id)
        try:
            saved = git_service.save_repository(request.json)
            git_service.trigger_immediate_project_synchronization()

            return response.json(saved, 201)
        except ValueError as e:
            logger.error(e)
            return error(
                422,
                "RepositoryCreationFailed",
                f"Insufficient permissions for remote repository.",
                details=e,
            )

    @git_endpoints.route(
        "/projects/<project_id:string>/git_repositories/<repository_id:int>",
        methods=["GET", "HEAD"],
    )
    @rasa_x_scoped("repositories.get")
    async def get_repository(
        request: Request, project_id: Text, repository_id: int
    ) -> HTTPResponse:
        """Get information for a specific Git repository."""

        git_service = _git(request, project_id, repository_id)
        try:
            repository = git_service.get_repository()
            return response.json(repository)
        except ValueError as e:
            logger.debug(e)
            return error(
                404,
                "RepositoryNotFound",
                f"Repository with ID '{repository_id}' could not be found.",
                details=e,
            )

    @git_endpoints.route(
        "/projects/<project_id:string>/git_repositories/<repository_id:int>",
        methods=["PUT"],
    )
    @rasa_x_scoped("repositories.update")
    @validate_schema("git_repository")
    async def update_repository(
        request: Request, project_id: Text, repository_id: int
    ) -> HTTPResponse:
        """Update a specific Git repository."""

        git_service = _git(request, project_id, repository_id)
        try:
            git_service.update_repository(request.json)
            return response.text("", 204)
        except ValueError as e:
            logger.debug(e)
            return error(
                404,
                "RepositoryNotFound",
                f"Repository with '{repository_id}' could not be found.",
                details=e,
            )

    @git_endpoints.route(
        "/projects/<project_id:string>/git_repositories/<repository_id:int>",
        methods=["DELETE"],
    )
    @rasa_x_scoped("repositories.delete")
    async def delete_repository(
        request: Request, project_id: Text, repository_id: int
    ) -> HTTPResponse:
        """Delete a stored Git repository."""

        git_service = _git(request, project_id, repository_id)
        try:
            git_service.delete_repository()
            return response.text("", 204)
        except ValueError as e:
            logger.debug(e)
            return error(
                404,
                "RepositoryNotFound",
                f"Repository with ID '{repository_id}' could not be found.",
                details=e,
            )

    @git_endpoints.route(
        "/projects/<project_id:string>/git_repositories/<repository_id:int>/status",
        methods=["GET"],
    )
    @rasa_x_scoped("repository_status.get")
    async def get_repository_status(
        request: Request, project_id: Text, repository_id: int
    ) -> HTTPResponse:
        """Gets the status of the repository."""

        git_service = _git(request, project_id, repository_id)
        try:
            repository_status = git_service.get_repository_status()
            return response.json(repository_status, 200)
        except ValueError as e:
            logger.debug(e)
            return error(
                404,
                "RepositoryNotFound",
                f"Repository with ID '{repository_id}' could not be found.",
                details=e,
            )

    @git_endpoints.route(
        "/projects/<project_id:string>/git_repositories/<repository_id:int>/branches/<branch_name:string>",
        methods=["PUT"],
    )
    @rasa_x_scoped("branch.update")
    async def checkout_branch(
        request: Request, project_id: Text, repository_id: int, branch_name: Text
    ) -> HTTPResponse:
        """Change the current branch of the repository."""

        git_service = _git(request, project_id, repository_id)
        discard_any_changes = utils.bool_arg(request, "force", False)

        try:
            git_service.checkout_branch(branch_name, force=discard_any_changes)
            return response.text("", 204)
        except ValueError as e:
            logger.debug(e)
            return error(
                404,
                "RepositoryNotFound",
                f"Branch '{branch_name}' for repository with ID '{repository_id}' could not be found.",
                details=e,
            )

    @git_endpoints.route(
        "/projects/<project_id:string>/git_repositories/<repository_id:int>/branches/<branch_name:string>/commits",
        methods=["POST"],
    )
    @rasa_x_scoped("commit.create")
    async def create_commit(
        request: Request, project_id: Text, repository_id: int, branch_name: Text
    ) -> HTTPResponse:
        """Commit and push the current local changes."""

        git_service = _git(request, project_id, repository_id)
        try:
            commit = git_service.commit_and_push_changes_to(branch_name)
            return response.json(commit, 201)
        except ValueError as e:
            logger.debug(e)
            return error(
                404,
                "RepositoryNotFound",
                f"Branch '{branch_name}' for repository with ID '{repository_id}' could not be found.",
            )

    return git_endpoints
