"""
Author: Maurice Snoeren <macsnoeren(at)gmail.com>
Version: 0.1 beta (use at your own risk)
Date: 2021-08-31
"""

class FSM:
    """FSM implements a finite state machine to create stable and robust embedded
       Python applications. Create your own FSM by extending this class and
       implement your state transitions and methods."""
    
    def __init__(self):
        """fsm = FSM() constructs a new FSM object."""
        self.transitions   = {}
        self.start_state   = None

    def call_method(self, method_call, params=None):
        """Call a method based on its string."""
        param_line = ""
        try:
            if isinstance(params, list):
                params_array = []
                for i in range(len(params)):
                    params_array.append("params[" + str(i) + "]")
                param_line = ",".join(params_array)

            eval(method_call + "(" + param_line + ")")

        except Exception as e:
            #print("call_method: could not find method: " + method_call + "(" + param_line + ")") # DEBUG
            #print(e)
            pass

    def set_state_start(self, name):
        """Set which state the FSM should start with."""
        self.start_state   = name.upper()
        self.state_current = self.start_state
        self.call_method("self." + self.state_current.lower() + "_pre", [None])

    def add_transition(self, state_from, event, state_to):
        """Adds a transition vector to the FSM. A transition is defined by the state
           it should be in, an event and the state it should go to. Only implement
           transitions that are used for efficiency purposes.
           state_pre(data), state_loop, state_post are the called methods if implemented."""
        state_from = state_from.upper()
        state_to   = state_to.upper()
        event      = event.upper()

        if not state_from in self.transitions.keys():
            self.transitions[state_from] = {}

        self.transitions[state_from][event] = state_to

    def event(self, event, data=None):
        """Raise an event."""
        event = event.upper()
        if self.state_current in self.transitions.keys():
            if event in self.transitions[self.state_current].keys():
                state_new = self.transitions[self.state_current][event]
                print("event " + event + ": " + self.state_current + " => " + state_new)
                self.call_method("self." + self.state_current.lower() + "_post")
                self.call_method("self." + state_new.lower() + "_pre", [data])

                self.state_current = state_new

            else:
                print("event: could not find the event " + event)
        else:
            print("event: could not find the current state in the transition data " + event)

    def get_states(self):
        """Returns an array containing the states that have been configured."""
        return self.transitions.keys()

    def get_events(self):
        """TODO: Returns an array containing the events that have been configured."""

    def get_transitions(self):
        """Returns the transition dict."""
        return self.transitions

    def loop(self):
        """Call the loop method periodically."""
        self.call_method("self." + self.state_current.lower() + "_loop")
