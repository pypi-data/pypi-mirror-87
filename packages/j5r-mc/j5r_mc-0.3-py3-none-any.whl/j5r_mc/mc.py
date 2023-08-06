# Python 3.8
"""
Markov Chain

The class MarkovChain allows you to simulate a Markov Chain.
You can use the MCmaker(n) to build a MarkovChain object with random parameters,
for n states.
The example is an instance of MarkovChain.

For using the MarkovChain class, you must pass a row-wise probability matrix "P"
and an initial distribution "d".
"""
import numpy as np

# exporting only: class, instance, builder
__all__ = ["MarkovChain", "example", "MCmaker"]


class MarkovChain:

    def __init__(self, P: np.array, d: np.array):
        """
        This method receives a row-wise Probability Matrix P and an initial
        distribution d and returns an integer generator object,
        which one is a Markov chain state.
        """
        self.__P = np.asarray(P)
        self.__d = np.asarray(d).reshape(1, -1).copy()
        self.__dupdate = self.__d.reshape(1, -1).copy()
        self.__theta = None
        self.__popped = False

    def pop(self):
        """
        It returns an integer regarding to the Markov state at each call.
        """
        if not self.__popped:
            self.__theta = np.where(
                np.random.rand() < np.cumsum(self.__d))[0][0]
            return self.__theta

        self.__theta = np.where(np.random.rand() <
                                np.cumsum(self.__P[self.__theta, :])
                                )[0][0]
        return self.__theta

    def __repr__(self):
        return f"<MarkovChain object, with {self.__d.size} states>"

    def distribution(self, n_steps=1):
        """
        n_steps is the number of steps to forwadly update the distribution. Each call
        of this method makes a new update. For example
            self.distribution()  -> d0
            self.distribution()  -> d1
            self.distribution()  -> d2
            self.distribution(4) -> d6
        """
        if n_steps <= 0:
            return None

        for i in range(n_steps):
            self.__dupdate = self.__dupdate @ self.__P
        self.__dupdate /= np.sum(self.__dupdate)

        return self.__dupdate.copy()

    @property
    def d(self):
        return self.__d.copy()

    @property
    def P(self):
        return self.__P.copy()

    @property
    def state(self):
        if self.__theta is None:
            print("Void! Call .pop() first.")
        return self.__theta

    def reset_distribution(self):
        self.__dupdate = self.__d.copy()

    def reset_state(self):
        self.__popped = False
        self.__theta = None

    def limit_distribution(self, n: int):
        """
        This method resets the distribution to the initial one, and returns
        a sequence of distributions from the initial to the n-th one.
        """
        self.reset_distribution()
        return np.vstack([self.distribution() for i in range(n)])

    def __len__(self):
        return self.d.size

    @property
    def N(self):
        return self.__len__()


def MCmaker(n=3):
    P = np.random.rand(n, n)
    for i in range(n):
        P[i, :] = P[i, :] ** 6
        P[i, :] /= P.sum(axis=1)[i]
    d = np.random.rand(n)
    d /= sum(d)
    return MarkovChain(P, d)


example = MCmaker(np.random.randint(2, 4))
