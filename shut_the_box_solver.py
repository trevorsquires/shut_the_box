import itertools


def get_partitions(num):
    # The two dice case is fairly easy, we can manually output partitions w/o using DP
    if num == 1:
        return [[1]]
    elif num == 2:
        return [[2]]
    elif num == 3:
        return [[1,2], [3]]
    elif num == 4:
        return [[1,3], [4]]
    elif num == 5:
        return [[5], [1,4], [2,3]]
    elif num == 6:
        return [[6], [1,5], [2,4], [1,2,3]]
    elif num == 7:
        return [[7], [1,6], [2, 5], [3,4], [1,2,4]]
    elif num == 8:
        return [[8], [1,7], [2,6], [3,5], [1,3,4], [1,2,5]]
    elif num == 9:
        return [[9], [1,8], [2,7], [3,6], [4,5], [2,3,4], [1,3,5], [1,2,6]]
    elif num == 10:
        return [[10], [1,9], [2,8], [3,7], [4,6], [1,2,7], [1,3,6], [1,4,5], [2,3,5], [1,3,6]]
    elif num == 11:
        return [[11], [1,10], [2,9], [3,8], [4,7], [5,6], [1,2,8], [1,3,7], [1,4,6], [2,3,6], [2,4,5], [1,2,3,5]]
    else:
        return [[12], [1,11], [2,10], [3,9], [4,8], [5,7], [1,2,9], [1,3,8], [1,4,7], [1,5,6], [2,3,7], [2,4,6], [3,4,5], [1,2,3,6], [1,2,4,5]]


def get_actions(dice, tile_set):
    actions = []
    possible_actions = get_partitions(dice)
    for action in possible_actions:
        if set(action).issubset(tile_set):
            actions.append(action)
    return actions


# Initialize State Space
board_size = 9
tiles = list(range(1, board_size+1))
state_dict = {(dice, tuple([a for a, b in zip(tiles, board_state) if b])):
                  {'actions': {}, 'best_action': {}, 'value': 0, 'next_states': []}
              for dice in range(2, 13) for board_state in itertools.product(*[(False, True)] * board_size)}

# Generate state information
for (dice, state_tiles) in state_dict.keys():
    viable_actions = get_actions(dice, set(state_tiles))
    if not viable_actions:
        state_dict[(dice, state_tiles)]['actions'][tuple()] = []
        tiles_left = set(range(1, board_size+1))
        for next_roll in range(2, 13):
            # if you have no actions, your only action is to start over
            state_dict[(dice, state_tiles)]['actions'][tuple()].append({
                    'next_state': (next_roll, tuple(sorted(tiles_left))),
                    'probability': (6-abs(next_roll-7))/36,
                }
            )
    for action in viable_actions:
        tiles_left = set(state_tiles) - set(action)
        state_dict[(dice, state_tiles)]['actions'][tuple(action)] = []
        for next_roll in range(2,13):
            # append the future state to this state's next_states
            state_dict[(dice, state_tiles)]['actions'][tuple(action)].append({
                'next_state': (next_roll, tuple(sorted(tiles_left))),
                'probability': (6-abs(next_roll-7))/36,
            })


# Begin value iteration
discount_factor = 0.9
iterations = 100
state_action_value = {}
for i in range(iterations):
    for (dice, state_tiles) in state_dict.keys():
        best_action_reward = -1
        best_action = None
        for action in state_dict[(dice, state_tiles)]['actions'].keys():
            immediate_reward = 100 if sum(state_tiles) == dice else 0
            future_reward = 0
            for entry in state_dict[(dice, state_tiles)]['actions'][action]:
                value, probability = state_dict[entry['next_state']]['value'], entry['probability']
                future_reward += value*probability
            total_reward = immediate_reward + discount_factor*future_reward

            # Keep track of best action/values for updates
            best_action_reward = max(best_action_reward, total_reward)
            best_action = action if best_action_reward == total_reward else best_action
            state_action_value[(dice, state_tiles, action)] = total_reward

        state_dict[(dice, state_tiles)]['value'] = best_action_reward
        state_dict[(dice, state_tiles)]['best_action'] = best_action

