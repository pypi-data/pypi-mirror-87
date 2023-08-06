"""Main module."""


from typing import List


def typename(obj:object) -> str:
    """
    Returns the name of a object type.
    :param obj:
    :return: string
    """
    return type(obj).__name__


class FibonacciSequence():
    """
    This class manages a list representing the Fibonacci Sequence.
    """

    def __init__(self):
        """
        Constructor for FibonacciSequence.
        """

        self.__sequence = [0, 1]


    def __repr__(self):
        """
        Representation for FibonacciSequence
        """
        return f"{typename(self)}(__sequence={self.__sequence})"


    def __getitem__(self, index:int) -> int:
        """
        Return element of nth index of FibonacciSequence object.
        """
        try:
            return self.__sequence[index]
        except IndexError:
            print('Please choose an index number within range.')


    @property
    def sequence(self) -> List[int]:
        """

        :return:
        """
        if len(self.__sequence) == 0:
            return []
        elif len(self.__sequence) == 1:
            return self.__sequence[1].copy()
        return self.__sequence.copy()


    def add_next_fibonacci_number(self) -> None:
        """
        Add next number to Fibonaccy sequence.
        """
        try:
            fibonacci_number = self.__sequence[-2] + self.__sequence[-1]
            self.__sequence.append(fibonacci_number)
        except IndexError:
            print('This function needs a list with at least two elements to work.')


    def increase_sequence(self, length_sequence: int) -> None:
        """
        Sets the Fibonacci sequence to the length_sequence integer.
        @param length_sequence: int
        """
        try:
            for i in range(length_sequence - 2):
                self.add_next_fibonacci_number()
        except TypeError:
            print('Please give an integer as input value.')



#Business logic
class FibonacciSequenceService():
    """
    This class alters the Fibonacci Sequence class sequence list representation.
    """

    def __init__(self):
        """
        Constructor for FibonacciNumber.
        """
        self.Sequence = FibonacciSequence()


    def get_sequence(self) -> List[int]:
        """
        :return: List[int]
        """
        return self.Sequence.sequence


    def increase_sequence_length(self, length_sequence: int):
        """
        Sets the Fibonacci sequence to the length_sequence integer.
        @param length_sequence: int
        """
        self.Sequence.increase_sequence(length_sequence)


    def get_nth(self, nth: int) -> int:
        """
        Returns the set nth Fibonacci number from the sequence.
        @param nth: int
        """
        try:
            print(self.Sequence[nth-1])
            return self.Sequence[nth-1]
        except TypeError:
            print('Please give integer as input.')


    def get_sequence_index(self, number: int) -> int:
        """
        Calculates the Fibonacci sequence till the given len_sequence
        and returns a list with the sequence.
        @param number: int
        """
        self.Sequence = FibonacciSequence()
        if number == 0 or number == 1:
            return self.Sequence.sequence[number]
        else:
            try:
                for i in range(number):
                    self.Sequence.add_next_fibonacci_number()
                    try:
                        return self.Sequence.sequence.index(number)
                    except ValueError:
                        if number > self.Sequence.sequence[-2] and number < self.Sequence.sequence[-1]:
                            closest = min(self.Sequence.sequence, key=lambda x: abs(x - number))
                            return self.Sequence.sequence.index(closest)

            except TypeError:
                print('Please give an integer as input value.')


print(FibonacciSequence())
print(FibonacciSequenceService())
