#  system functions for the effects of time on a player

def raise_hunger(db, messenger, object):
    if object['hunger'] >= 9:
        #  player is going to die, so let's just skip the database
        #  TODO: don't do this, and let an event driven system pick up players who have gotten too hungry
        username = object['entity']
        db.set_component_for_entity('player_status', {'location': '0;0'}, username)
        db.set_component_for_entity('inventory', {}, username)
        return [
            messenger.plain_text('You have died of hunger!', username),
            messenger.plain_text('You have lost everything in your inventory!', username),
            messenger.plain_text('You have been resurrected at The Origin!', username)
        ]
    db.increment_property_of_component('player_status', object['entity'], 'hunger', 1)
    if 2 <= object['hunger'] < 3:
        return [messenger.plain_text('You begin to feel hungry', object['entity'])]
    if 4 <= object['hunger'] < 5:
        return [messenger.plain_text('You hunger is giving way to hangriness', object['entity'])]
    if 6 <= object['hunger'] < 7:
        return [messenger.plain_text('Your hunger hurts, making anything but eating mentally difficult', object['entity'])]
    if 8 <= object['hunger'] < 9:
        return [messenger.plain_text('You are about to die of hunger! Eat, NOW!', object['entity'])]
    return []

