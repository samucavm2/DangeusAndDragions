from abc import ABC, abstractmethod

class InterfaceArmas(ABC):
    @abstractmethod
    def ataque_rapido(self) -> int:
        pass

    @abstractmethod
    def ataque_duas_maos(self) -> int:
        pass
