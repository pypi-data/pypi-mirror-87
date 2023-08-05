import time
from .tools import BaseSequence, download

    
class BaseSequence:
    counter = 0
    last_cycle_time = 0.0

    def __init__(self):
        self.data = {}
        self.counter = 0
        self.last_cycle_time = 0
        self.seq_state = 0
        
    def update(self):
        raise NotImplementedError('update')
    def __next__(self):
        if not self.next_cycle():
            raise StopIteration()


    def __iter__(self):
        return self

    def next_cycle(self):
        s_time = time.time()
        r = self.run_cycle()
        self.last_cycle_time = time.time()-s_time
        return r

    def run_cycle(self):
        raise NotImplementedError('next_cycle')

    def runner(self, cycle_time=0.1):
        def run(seq=self, cycle_time=cycle_time):
            while seq.next_cycle():
                time.sleep(max( cycle_time-seq.last_cycle_time, 0.0 ))
        return run
        
    def reset(self):
        raise NotImplementedError('reset')


class MoveTwoPosSequence(BaseSequence):
    """ Sequencer that move motor in two positions successively

    At each position a callback can be executed.
    Of course the sequencer is not suitable for time critical application.

    One can simply iter on the object to execute cycles:

        seq = MoveTwoPosSequence(motor, 0.0, 2.0, velocity=0.5, sleep_time=3.0)
        while seq.next_cycle():
            time.sleep(0.1) # this set the min time resolution of the sequencer

    In the exemple above the cycle time of the sequencer is NOT deterministic as
    the time taken by OPC-UA request or the callback can vary. But this should be
    ok in most AIT test situation.

    We can get closer to a deterministic cycle time by doing:

        while seq.next_cycle():
            time.sleep( max(0.1-seq.last_cycle_time, 0.0) )

    Or the exemple above is equivalent on doing:

        > seq.runner(0.1)()

    One can encapsulate the sequencer in a Thread or async func (while it is not an async object)
    The runner method is creating a function ready to be executed in a thread :
    It take one argument, the cycle time:

        seq = MoveTwoPosSequence(motor, 0.0, 2.0, velocity=0.5, sleep_time=3.0)
        t = Thread(target=seq.runner(0.1))
        t.start()
    
    """
    class SEQ_STATE:
        IDL, WAITING_H, WAITING_L, MOVING_L, MOVING_H = range(5)
        STOP = 100

    def __init__(self, motor, l_pos=0.0, h_pos=1.0, velocity=0.1, l_velocity=None,
                 h_velocity=None, sleep_time=0.0, callback=None, h_callback=None, l_callback=None,
                 n_sequence=None
                 ):
        super().__init__()
        self.motor = motor
        self.l_pos = l_pos
        self.h_pos = h_pos
        self.l_velocity = velocity if l_velocity is None else l_velocity
        self.h_velocity = velocity if h_velocity is None else h_velocity

        self.sleep_time = sleep_time

        self.callback = callback
        self.h_callback = callback if h_callback is None else h_callback
        self.l_callback = callback if l_callback is None else l_callback
        self.n_sequence = n_sequence
        
        self.seq_state = self.SEQ_STATE.IDL
        self._action_time = time.time()

    def stop(self):
        self.seq_state = self.SEQ_STATE.STOP

    def reset(self):
        self.seq_state = self.SEQ_STATE.IDL

    def update(self):
        download([self.motor.stat.substate, self.motor.stat.pos_actual], self.data)

    def run_cycle(self):
        S = self.SEQ_STATE
        if self.seq_state == S.STOP:
            self.motor.stop()
            return False


        if self.seq_state in (S.WAITING_H, S.WAITING_L):
            if (time.time()-self._action_time)>self.sleep_time:
                if self.seq_state == S.WAITING_H:

                    self.motor.move_abs(self.l_pos, self.l_velocity)
                    self.seq_state = S.MOVING_L
                else:
                    self.motor.move_abs(self.h_pos, self.h_velocity)
                    self.seq_state = S.MOVING_H
            else:
                return True # need to wait

        elif self.seq_state in (S.MOVING_L, S.MOVING_H):
            self.update()
            if self.data[self.motor.stat.substate.key] == self.motor.SUBSTATE.OP_STANDSTILL:
                if self.seq_state == S.MOVING_H:
                    self.seq_state = S.WAITING_H
                    self._action_time = time.time()
                    if self.h_callback: self.h_callback(self)
                else:
                    self.seq_state = S.WAITING_L
                    self.counter += 1 # counter increase when reaching the low value
                    self._action_time = time.time()
                    if self.h_callback: self.l_callback(self)
                    if self.n_sequence is not None and self.counter>=self.n_sequence:
                        return False

            else:
                return True

        elif self.seq_state == S.IDL:
            self.motor.move_abs(self.l_pos, self.l_velocity)
            self.seq_state = S.MOVING_L
        else:
            raise Exception("BUG seq_state", self.seq_state)

        return True
