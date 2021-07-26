import abc


class AbstractTemplateBuilder(abc.ABC):
    @abc.abstractmethod
    def gentemplate(self) -> str:
        raise NotImplementedError
