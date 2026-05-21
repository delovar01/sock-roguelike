from src.core import constants


def test_tile_size_is_positive():
    assert constants.TILE_SIZE > 0
    assert constants.SCREEN_WIDTH > 0
    assert constants.SCREEN_HEIGHT > 0


def test_screen_dimensions_divisible_by_tile():
    # окно должно вмещать целое число тайлов
    assert constants.SCREEN_WIDTH % constants.TILE_SIZE == 0
    assert constants.SCREEN_HEIGHT % constants.TILE_SIZE == 0
