from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
import numpy as np

from bavard.dialogue_policy.data.utils import EncodingContext, LabelBinarizer, TextEncoder


class DummyContext:
    def __init__(self):
        self.intents = ["intent1", "intent2"]
        self.actions = ["action1", "action2", "action3"]
        self.tag_types = ["tagtype1", "tagtype2", "tagtype3", "tagtype4"]
        self.slots = ["slot1", "slot2", "slot3"]
        self.enc_context = EncodingContext(
            intent=LabelBinarizer(),
            action=LabelBinarizer(),
            action_index=LabelEncoder(),
            tags=MultiLabelBinarizer(),
            slots=MultiLabelBinarizer(),
            utterance=TextEncoder()
        )
        self.enc_context.fit(
            intent=self.intents,
            action=self.actions,
            action_index=self.actions,
            tags=[self.tag_types],
            slots=[self.slots]
        )


def check_user_dialogue_turn_feature_vec(
    feature_vec: np.ndarray, ctx: DummyContext, *, slots: tuple, intent: str, tag_types: tuple
):
    """
    Checks the exact contents of the "feature_vec" entry of an encoded UserDialogueTurn instance
    to make sure they're correct.
    """
    # Shape should be correct
    assert feature_vec.shape == (1, len(ctx.slots) + len(ctx.intents) + len(ctx.tag_types))

    # Content should be correct
    slots_enc = feature_vec[:, :len(ctx.slots)]
    slots_decoded = ctx.enc_context.inverse_transform("slots", slots_enc)[0]
    assert slots_decoded == slots, f"{slots_decoded} != {slots}"

    intent_enc = feature_vec[:, len(ctx.slots):len(ctx.slots) + len(ctx.intents)]
    intent_decoded = ctx.enc_context.inverse_transform("intent", intent_enc)[0]
    assert intent_decoded == intent, f"{intent_decoded} != {intent}"

    tags_enc = feature_vec[:, -len(ctx.tag_types):]
    tags_decoded = ctx.enc_context.inverse_transform("tags", tags_enc)[0]
    assert tags_decoded == tag_types, f"{tags_decoded} != {tag_types}"


def check_agent_action_feature_vec(feature_vec: np.ndarray, ctx: DummyContext, *, action: str):
    # Shape should be correct
    assert feature_vec.shape == (1, len(ctx.actions))

    # Contents should be correct
    action_decoded = ctx.enc_context.inverse_transform("action", feature_vec)[0]
    assert action_decoded == action, f"{action_decoded} != {action}"
