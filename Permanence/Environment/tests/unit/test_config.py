import os
from unittest.mock import patch
from permanence_env.core.config import Config

def test_config_env_override():
    """Verify environment variables override default settings."""
    with patch.dict(os.environ, {"TARGET_FPS": "120"}):
        config = Config()
        assert config.target_fps == 120
