
Markov Chain (j5r_mc)
============

The class "MarkovChain" allows you to simulate a Markov Chain.
You can use the "MCmaker(n)" to build a MarkovChain object with random parameters,
for n states.
The "example" is an instance of MarkovChain.

For using the MarkovChain class, you must pass a row-wise probability matrix "P"
and an initial distribution "d".


Documentation
============

----

**class MarkovChain(builtins.object)**
 |  MarkovChain(P: numpy.array, d: numpy.array)
 |  
 |  Methods defined here:
 |  
 |  __init__(self, P: numpy.array, d: numpy.array)
 |      This function receives a row-wise Probability Matrix P and an initial
 |      distribution d and returns an integer generator object, 
 |      which one is a Markov chain state.
 |  
 |  __len__(self)
 |      It returns the number of states of the Markov chain. The same as self.N.
 |  
 |  __repr__(self)
 |      Return repr(self).
 |  
 |  distribution(self, n_steps=1)
 |      n is the number of steps to forwadly update the distribution. Each call
 |      of this method makes a new update. For example
 |      self.distribution()  -> d0
 |      self.distribution()  -> d1
 |      self.distribution()  -> d2
 |      self.distribution(4) -> d6
 |
 |  limit_distribution(self, n: int)
 |      This method resets the distribution to the initial one, and returns
 |      a sequence of distributions from the initial to the n-th one.
 |  
 |  pop(self)
 |      It returns an integer regarding to the Markov state at each call.
 |   
 |  
 |  reset_distribution(self)
 |      It resets the distribution to the initial one.
 |  
 |  reset_state(self)
 |      It resets the state to None. Use the pop() method to take a new state.
 |      This new state can be accessed by "self.state".


---

   **Readonly properties defined here:**
 |  
 |  N : number of states of the Markov chain.
 |  
 |  P : the probability matrix.
 |  
 |  d : the distribution vector.
 |  
 |  state: the current Markov state.


