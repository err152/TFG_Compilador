from typing import List;
from abc import ABC,abstractmethod
from Interprete import Interprete

class LoxCallable(ABC):

   @abstractmethod
   def call(self, interpreter: Interprete, arguments : List[any]) -> any:
      pass

   @abstractmethod
   def arity(self) -> int:
      pass
