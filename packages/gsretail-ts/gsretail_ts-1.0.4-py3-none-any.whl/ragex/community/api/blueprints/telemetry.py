from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse

from rasa.constants import GLOBAL_USER_CONFIG_PATH

from ragex.community.api.decorators import rasa_x_scoped, validate_schema
from ragex.community.services.config_service import ConfigService, ConfigKey
from ragex.community.constants import REQUEST_DB_SESSION_KEY
from ragex.community import metrics, config


def blueprint() -> Blueprint:
    telemetry_endpoints = Blueprint("telemetry_endpoints")

    @telemetry_endpoints.route("/telemetry", methods=["GET", "HEAD"])
    @rasa_x_scoped("telemetry.get", allow_api_token=True)
    async def get_telemetry_config(request: Request) -> HTTPResponse:
        """Read the current telemetry configuration.

        Args:
            request: Received HTTP request.

        Returns:
            HTTP 200 response with telemetry and server information.
        """

        return response.json({"telemetry_enabled": metrics.are_metrics_enabled()})

    @telemetry_endpoints.route("/telemetry", methods=["POST"])
    @rasa_x_scoped("telemetry.create", allow_api_token=True)
    @validate_schema("telemetry_event")
    async def telemetry_event(request: Request) -> HTTPResponse:
        """Attempts to track a telemetry event. The event will only be tracked
        if telemetry is enabled.

        Args:
            request: Received HTTP request.

        Returns:
            HTTP 204 response.
        """

        rj = request.json
        metrics.track(rj["event_name"], rj.get("properties"), rj.get("context"))
        return response.text("", 204)

    @telemetry_endpoints.route("/telemetry", methods=["DELETE"])
    @rasa_x_scoped("telemetry.delete", allow_api_token=True)
    async def disable_telemetry(request: Request) -> HTTPResponse:
        """Updates the telemetry configuration in server mode and sets its
        enabled value to `False`. Changes won't take effect until the Rasa X
        server is restarted.

        In local mode, returns HTTP 400.

        Args:
            request: Received HTTP request.

        Returns:
            HTTP 200 when in server mode, 400 when in local mode.
        """

        if not metrics.are_metrics_enabled():
            return response.text("Telemetry is already disabled.\n")

        if config.LOCAL_MODE:
            return response.text(
                f"To disable telemetry, edit your Rasa configuration file in "
                f"'{GLOBAL_USER_CONFIG_PATH}' instead of using this endpoint.\n"
                f"After editing the file, make sure to restart Rasa X.\nTelemetry is "
                f"enabled.\n",
                400,
            )

        config_service = ConfigService(request[REQUEST_DB_SESSION_KEY])
        config_service.set_value(ConfigKey.TELEMETRY_ENABLED, False)

        return response.text(
            "The telemetry configuration has been updated.\nTo disable telemetry, "
            "restart the Rasa X server.\n"
        )

    return telemetry_endpoints
