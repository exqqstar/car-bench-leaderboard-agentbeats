import importlib
import sys
import types
import unittest
from unittest import mock

sys.modules.setdefault("tomli_w", types.SimpleNamespace(dumps=lambda data: ""))
sys.modules.setdefault("requests", types.SimpleNamespace())

generate_compose = importlib.import_module("generate_compose")


class ResolveImageTests(unittest.TestCase):
    def test_resolve_image_uses_amber_manifest_when_docker_image_missing(self) -> None:
        agent = {"agentbeats_id": "purple-id"}
        response = mock.Mock()
        response.text = """
        {
          program: {
            image: "ghcr.io/example/purple:latest",
          },
        }
        """
        response.raise_for_status.return_value = None

        with mock.patch.object(
            generate_compose,
            "fetch_agent_info",
            return_value={
                "docker_image": None,
                "amber_manifest_url": "https://example.com/amber-manifest.json5",
            },
        ), mock.patch.object(generate_compose.requests, "get", create=True, return_value=response):
            generate_compose.resolve_image(agent, "participant 'agent'")

        self.assertEqual(
            agent["image"],
            "ghcr.io/example/purple:latest",
        )


if __name__ == "__main__":
    unittest.main()
