from pygame.sprite import Group
from pygame import Rect
from riichiroyale.sprites import TILE_SIZE, SMALL_TILE_SIZE, TileRender


def render_discard_pile(board_render, player_id, seat):
    group = Group()
    match = board_render.match
    player = match.players[player_id]

    if player.discard_pile is None:
        return group

    rect = Rect(board_render.surface.get_rect())
    rect.center = (0, 0)

    side_calculation = (SMALL_TILE_SIZE[1] + 10) * 3
    if seat == 0:
        rect.bottom = side_calculation + TILE_SIZE[1] + 20
    if seat == 2:
        rect.top = -side_calculation

    tile_offset = 10
    tiles_per_row = 12
    i = 0
    row = 0
    row_offset = SMALL_TILE_SIZE[1] + tile_offset
    full_width = tiles_per_row * (SMALL_TILE_SIZE[0] + tile_offset) - tile_offset
    beginning_of_across_line = (rect.width - full_width) / 2
    beginning_of_across_line += full_width if seat == 2 else 0
    across = beginning_of_across_line
    for tile in player.discard_pile:
        tile_pos = (across, -rect.y + (row * row_offset))
        tile_sprite = TileRender(
            board_render.small_dictionary,
            tile,
            tile_pos,
            small_tile=True,
            rotation=seat,
        )
        group.add(tile_sprite)
        across += (
            SMALL_TILE_SIZE[0] + tile_offset
            if seat == 0
            else -(SMALL_TILE_SIZE[0] + tile_offset)
        )
        i += 1
        if i >= tiles_per_row:
            i = 0
            row += 1 if seat == 0 else -1
            across = beginning_of_across_line
    return group


def render_vertical_discard_pile(board_render, player_id, seat):
    group = Group()
    match = board_render.match
    player = match.players[player_id]

    if player.discard_pile is None:
        return group

    rect = Rect(board_render.surface.get_rect())
    rect.center = (0, 0)

    side_calculation = (SMALL_TILE_SIZE[1] + 10) * 4
    if seat == 1:
        rect.right = side_calculation + 180
    if seat == 3:
        rect.left = -side_calculation - 180

    tile_offset = 10
    tiles_per_row = 8
    i = 0
    row = 0
    row_offset = SMALL_TILE_SIZE[1] + tile_offset
    full_width = tiles_per_row * (SMALL_TILE_SIZE[0] + tile_offset) - tile_offset
    beginning_of_across_line = rect.height - ((rect.height - full_width) / 2)
    beginning_of_across_line -= full_width if seat == 3 else 0
    across = beginning_of_across_line
    for tile in player.discard_pile:
        tile_pos = (-rect.x + (row * row_offset), across)
        tile_sprite = TileRender(
            board_render.small_dictionary,
            tile,
            tile_pos,
            small_tile=True,
            rotation=seat,
        )
        group.add(tile_sprite)
        across -= (
            SMALL_TILE_SIZE[0] + tile_offset
            if seat == 1
            else -(SMALL_TILE_SIZE[0] + tile_offset)
        )
        i += 1
        if i >= tiles_per_row:
            i = 0
            row += 1 if seat == 1 else -1
            across = beginning_of_across_line
    return group
