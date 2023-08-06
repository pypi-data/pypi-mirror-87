import glob
import json
import os
from copy import copy

from bavard.dialogue_policy.data.agent import AgentDataUtils


class UnsupportedActionException(Exception):
    pass


dir_path = os.path.dirname(os.path.realpath(__file__))
# These actions are either out of domain, or occur only once or twice.
# We can't validate a model's generalization performance on an action
# when it only occurs once in the dataset.
AGENT_ACTION_BLACKLIST = {
    "Restaurant-Request",
    "general-thank",
    "Restaurant-Inform",
    "Train-OfferBook",
    "Police-Inform",
    "Restaurant-Select",
    "Train-Inform",
    "Hospital-Inform",
    "Train-Request",
    "Restaurant-Recommend",
    "NONE"
}

USER_ACTION_BLACKLIST = {
    "Attraction-Inform",
    "Attraction-Request",
    "Restaurant-Request",
    "Train-Inform"
}

# These agent actions correspond to these slot states,
# so information about the result of knowledge-base queries can
# be made available to the agent (since some agent actions are
# dependent on those query reults).
KB_STATE_REP = {
    "Booking-NoBook": {"nomatches": True},  # the KB didn't return any matches
    "Hotel-NoOffer": {"nomatches": True}
}


def load_dialogue_acts():
    acts_file_path = os.path.join(dir_path, '../../../data/MultiWOZ_2.2/dialog_acts.json')

    with open(acts_file_path) as f:
        dialogue_acts = json.load(f)
        return dialogue_acts


def get_service_frame(turn: dict, service: str) -> dict:
    x = list(filter(lambda z: z['service'] == service, turn['frames']))
    assert len(x) == 1
    return x[0]


def get_filled_slots_for_frame(turn: dict, service: str) -> dict:
    frame = get_service_frame(turn, service)
    slots = {}
    for name, values in frame["state"]["slot_values"].items():
        if len(values) > 0:
            # We only support single-valued slots right now,
            # so just use the first value.
            slots[name] = values[0]
    return slots


def span_info_to_tags(span_info):
    tags = []
    for sp in span_info:
        tags.append({
            'tagType': sp[1],
            'value': sp[2],
            # 'start': sp[3],
            # 'end': sp[4]
        })
    return tags


def get_action_from_dialogue_act(dialogue_act: dict, blacklist: set = None) -> str:
    act = dialogue_act['dialog_act']
    action_names = list(act.keys())

    # select one act to be the representative action for this turn, since
    # we aren't supporting multiple action annotations per turn.

    action_name = None

    # If a hotel action is present, just use that.
    for name in action_names:
        if name.startswith('Hotel'):
            action_name = name

    # Otherwise pick the first one
    if action_name is None and len(action_names) > 0:
        action_name = action_names[0]
    elif action_name is None:
        action_name = 'NONE'

    if blacklist and action_name in blacklist:
        raise UnsupportedActionException

    return action_name


def transform_agent_action(turn, dialogue_act) -> tuple:
    action_name = get_action_from_dialogue_act(dialogue_act, AGENT_ACTION_BLACKLIST)
    kb_deps = KB_STATE_REP[action_name] if action_name in KB_STATE_REP else {}
    return {
        'actor': 'AGENT',
        'agentAction': {
            'type': 'UTTERANCE_ACTION',
            'utterance': turn['utterance'],
            'name': action_name,
        }
    }, kb_deps


def transform_user_action(turn, dialogue_act):
    span_info = dialogue_act['span_info']
    tags = span_info_to_tags(span_info)

    return {
        'actor': 'USER',
        'userAction': {
            'type': 'UTTERANCE_ACTION',
            'utterance': turn['utterance'],
            # Our notion of an intent is like MWOZ's user action.
            'intent': get_action_from_dialogue_act(dialogue_act, USER_ACTION_BLACKLIST),
            'tags': tags
        }
    }


def transform_hotel_dialogue(hotel_dialogue, all_acts):
    acts = all_acts[hotel_dialogue['dialogue_id']]
    result_turns = []
    state = {"slots": {}}
    for raw_turn in hotel_dialogue['turns']:
        dialogue_act = acts[raw_turn['turn_id']]
        if raw_turn['speaker'] == 'USER':
            state['slots'] = get_filled_slots_for_frame(raw_turn, 'hotel')
            turn = transform_user_action(raw_turn, dialogue_act)
        else:
            turn, kb_deps = transform_agent_action(raw_turn, dialogue_act)
            # If this agent action is dependent on the results of a knowledge base
            # query, we add a slot for the KB results to the dialogue state. We
            # associate the slot with the prior user turn, so the model can see
            # it when its trying to predict this agent action.
            result_turns[-1]['state']['slots'].update(kb_deps)
        turn['state'] = copy(state)
        result_turns.append(turn)

    return {
        'turns': result_turns
    }


def main():
    acts = load_dialogue_acts()
    train_files_glob = os.path.join(dir_path, '../../../data/MultiWOZ_2.2/train/dialogues_*.json')
    train_files = glob.glob(train_files_glob)

    all_dialogues = []
    for train_file in train_files:
        with open(train_file) as f:
            dialogs = json.load(f)
            all_dialogues += dialogs
    print('Total training dialogues:', len(all_dialogues))

    conversations = []
    for dialog in all_dialogues:
        if dialog['services'] == ['hotel']:
            try:
                conv = transform_hotel_dialogue(dialog, acts)
                conversations.append(conv)
            except UnsupportedActionException:
                continue

    print('Total hotel dialogues:', len(conversations))

    hotel_data_agent = AgentDataUtils.build_from_convs(conversations)

    hotel_data_path = os.path.join(dir_path, '../../../test/data/dialogue_policy/agents/mwoz2_2_hotel_dialogs.json')
    with open(hotel_data_path, 'w', encoding='utf-8') as f:
        json.dump(hotel_data_agent, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
