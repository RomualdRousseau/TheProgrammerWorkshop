from unittest.mock import patch, MagicMock
from permanence_env.utils.loader import load_tmx_map, get_tile_texture

def test_load_tmx_map():
    """Verify load_tmx_map calls TiledMap with the correct path."""
    with patch("pytmx.TiledMap") as mock_tiled_map:
        path = "assets/tilemaps/room.tmx"
        load_tmx_map(path)
        mock_tiled_map.assert_called_once_with(path)

def test_get_tile_texture():
    """Verify get_tile_texture calls load_texture and uses caching."""
    # Clear the LRU cache for testing (using .cache_clear() if available)
    get_tile_texture.cache_clear()
    
    with patch("pyray.load_texture") as mock_load_texture:
        mock_texture = MagicMock()
        mock_load_texture.return_value = mock_texture
        
        path = "assets/images/table.png"
        
        # First call
        tex1 = get_tile_texture(path)
        assert tex1 == mock_texture
        mock_load_texture.assert_called_once_with(path)
        
        # Second call (should be cached)
        tex2 = get_tile_texture(path)
        assert tex2 == mock_texture
        assert mock_load_texture.call_count == 1
