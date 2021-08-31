"""
Author: Maurice Snoeren <macsnoeren(at)gmail.com>
Version: 0.1 beta (use at your own risk)
Date: 2021-08-31
"""

class FSM:
    
    def __init__(self):
        self.states        = {}
        self.transitions   = {}
        self.start_state   = None
        self.state_current = self.start_state

    def add_state(self, name, method_pre, method_loop, method_post):
        name = name.upper()
        self.states[name] = { "method_pre": method_pre, "method_loop": method_loop, "method_post": method_post}

    def set_state_start(self, name):
        self.start_state   = name.upper()
        self.state_current = self.start_state

    def add_transition(self, state_from, event, state_to):
        state_from = state_from.upper()
        state_to   = state_to.upper()
        event      = event.upper()

        if not state_from in self.transitions.keys():
            self.transitions[state_from] = {}

        self.transitions[state_from][event] = state_to

    def event(self, event):
        event = event.upper()
        if self.state_current in self.transitions.keys():
            if event in self.transitions[self.state_current].keys():
                state_new = self.transitions[self.state_current][event]
                print("Transit from " + self.state_current + " to " + state_new + " due to event " + event)

                if self.state_current in self.states.keys():
                    if self.states[self.state_current]["method_post"] != None:
                        self.states[self.state_current]["method_post"]() # Call the post method!

                else:
                    print("Strange?! Cannot find the old state in the state data! " + self.state_current)

                if state_new in self.states.keys():
                    if self.states[state_new]["method_pre"] != None:
                        self.states[state_new]["method_pre"]()                    

                else:
                    print("Strange?! Cannot find the new state in the state data! " + state_new)

                self.state_current = state_new

            else:
                print("Could not find the event " + event)
        else:
            print("Could not find the current state in the transition data " + event)

    def loop(self):
        if self.state_current in self.states.keys():
            if self.states[self.state_current]["method_loop"] != None:
                self.states[self.state_current]["method_loop"]() # Call the post method!

        else:
            print("Strange?! Cannot find the old state in the state data! " + self.state_current)
