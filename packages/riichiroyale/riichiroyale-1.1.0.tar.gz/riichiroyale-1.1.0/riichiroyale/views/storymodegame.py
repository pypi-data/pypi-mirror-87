import pygame
import pygame_gui
import numpy
from libmahjong import start_game, EventType, EngineEvent, PieceType
from riichiroyale.game import Player, Match, process_event_queue, DialogManager, loadStory, get_object, save_object
from riichiroyale.utils import load_image_resource
from .game import GameView

ROUND_END_EVENTS = ["on_player_wins", "on_player_loses", "on_both_lose"]

DIALOGUE_EVENT_PRIORITY = ["call_chi", "call_pon", "call_kan", "call_riichi", "call_ron", "on_player_wins", "on_player_loses", "on_both_lose", "intro"][::-1]
EVENT_TYPE_TO_DIALOGUE = {
    EventType.Chi: "call_chi",
    EventType.Pon: "call_pon",
    EventType.Ron: "call_ron",
    EventType.ConvertedKan: "call_kan",
    EventType.ConcealedKan: "call_kan",
    EventType.Kan: "call_kan",
    EventType.Riichi: "call_riichi"
}

class StoryModeGame(GameView):
    def __init__(
        self,
        game_manager,
        screen,
        tile_dict,
        small_tile_dict,
        screen_width,
        screen_height,
        width_ratio,
        height_ratio,
        player_manager=None,
    ):
        self.player_manager = player_manager
        self.ai_list = ["Player"] + ["AngryDiscardoBot"] * 3
        self.match = None
        self.match_dict = None
        self.match_opponent = None
        self.match_dialogue_possibilities = DIALOGUE_EVENT_PRIORITY

        # Custom Flag to tell Board Manager to Fill this View's attribute with specific (watched) ai events
        self.receive_ai_events = 2
        self.watched_ai_event_log = []

        super().__init__(
            game_manager,
            screen,
            tile_dict,
            small_tile_dict,
            screen_width,
            screen_height,
            width_ratio,
            height_ratio,
            player_manager=player_manager,
            name="storymodegame",
            textbox_hook=lambda uiM, bM, dE, t: new_dialogue(self.match_dict, uiM, bM, dE, t)
        )

    def _end_round_dialog(self):
        # Skip for Own Round Handling
        pass

    def load_match(self, match_dict, stage_number):
        self.stage_number = stage_number
        self.ai_list = ["Player"] + match_dict["ais"]
        self.match_dict = match_dict
        prefix = "<b>{}</b><br><br>".format(self.match_dict['opponent'])
        self.match_opponent = self.match_dict['opponent_index']

        self.dialogue_manager = DialogManager()
        
        for possible_event in DIALOGUE_EVENT_PRIORITY:
            if possible_event in self.match_dict:
                self.dialogue_manager.register_dialog_event(possible_event)
                elements = [prefix + self.match_dict[possible_event]] \
                    if isinstance(self.match_dict[possible_event], str) \
                    else list(map(lambda x: prefix + x, self.match_dict[possible_event]))

                self.dialogue_manager.append_dialog_event(possible_event, elements)

    def play_oneshot_dialogue(self, event):
        if event in self.match_dialogue_possibilities:
            self.match_dialogue_possibilities.remove(event)
            self.lock_user_input = self.dialogue_manager.start_event(event)
            return True
        return False

    def on_round_start(self):
        super().on_round_start()
        if 'intro' in self.match_dict:
            self.play_oneshot_dialogue('intro')

    def on_tile_pressed(self, owner, tile_hand_index):
        if owner.my_turn and not self.lock_user_input:
            tile = owner.hand[tile_hand_index]
            if (
                self.game_manager.board_manager.waiting_on_decision
                and len(owner.calls_avaliable) == 0
            ):
                event = EngineEvent()
                event.type = EventType.Discard
                event.piece = int(tile.get_raw_value())
                event.player = owner.player_id
                event.decision = True
                self.player_manager.MakeDecision(event)

    def on_dialogue_event_ending(self, event_name):
        if event_name in ROUND_END_EVENTS:
            self.game_manager.set_active_view("storymodeselect")
            self.game_manager.sound_manager.play_music("lobby")
            self.match.player_manager.reset(clear=True)
            self.match = None
        self.lock_user_input = False

    def process_possible_dialogue_events(self):
        if len(self.watched_ai_event_log) > 0:
            queued_dialogue_events = list(map(lambda event: EVENT_TYPE_TO_DIALOGUE[event.type], self.watched_ai_event_log))
            for event in DIALOGUE_EVENT_PRIORITY:
                if event in queued_dialogue_events:
                    if self.play_oneshot_dialogue(event):
                        self.watched_ai_event_log = []
                        return

    def _determine_winner(self):
        scores = self.match.scores
        delta_scores = self.match.delta_scores
        total_scores = list(map(lambda s: s[0] + s[1], zip(scores, delta_scores)))

        array = numpy.array(total_scores)
        temp = array.argsort()[::-1]
        ranks = numpy.empty_like(temp)
        ranks[temp] = numpy.arange(len(array))
        print(ranks)

        if ranks[self.match.player_manager.player_id] == 0:
            self.play_oneshot_dialogue('on_player_wins')
            matches = get_object('matches')
            i = 0
            for match in matches['matches']:
                if match['stage'] == i:
                    matches['matches'][i]['completed'] = True
                    break
                i += 1
            save_object('matches', matches)
        elif ranks[self.match_dict['opponent_index']] == 0:
            self.play_oneshot_dialogue('on_player_loses')
        else:
            self.play_oneshot_dialogue('on_both_lose')

    def update(self, time_delta):
        self.process_possible_dialogue_events()
        if self.game_manager.board_manager.game_should_end:
            self.game_manager.board_manager.game_should_end = False
            self.match.match_alive = False
            self._determine_winner()

        super().update(time_delta)


def new_dialogue(match_dict, gui_manager, button_map, element_list, text):
    icon_path = None
    for entry in get_object('boticons')['bot']:
        if entry['ai'] == match_dict['ais'][1]:
            icon_path = entry['icon']
            break

    icon_size = (125, 125)
    icon_rect = pygame.Rect(0, 0, icon_size[0], icon_size[1])
    icon_rect.bottomleft = (20, -270)
    logo_surface = pygame.Surface(icon_size, pygame.SRCALPHA)
    load_image_resource(icon_path, logo_surface, size=icon_size)
    icon = pygame_gui.elements.ui_image.UIImage(
        relative_rect=icon_rect,
        image_surface=logo_surface,
        manager=gui_manager,
        anchors={"left": "left", "right": "left", "top": "bottom", "bottom": "bottom"},
    )

    text_box_rect = pygame.Rect(0, 0, 1366 - 40, 200)
    text_box_rect.bottomleft = (20, -70)
    text_box = pygame_gui.elements.UITextBox(
        relative_rect=text_box_rect,
        visible=False,
        html_text=text,
        manager=gui_manager,
        anchors={
            "top": "bottom",
            "bottom": "bottom",
            "left": "left",
            "right": "left",
        },
    )
    text_next_button_rect = pygame.Rect(0, 0, 100, 50)
    text_next_button_rect.bottomleft = (-120, -20)
    text_next = pygame_gui.elements.UIButton(
        relative_rect=text_next_button_rect,
        visible=False,
        text="Next",
        manager=gui_manager,
        anchors={
            "top": "bottom",
            "bottom": "bottom",
            "left": "right",
            "right": "right",
        },
    )

    button_map["text"] = text_box
    button_map["advance_text"] = text_next
    element_list += [icon]