# Shut the Box

This is a very simple script used to generate an optimal policy to the "shut the box" game. 

To get started, simply run the script and evaluate a state using

```
state_dict[(dice_roll, tuple of tiles remaining in the up position)]['best_action']
```

to obtain the best action in your current state. 