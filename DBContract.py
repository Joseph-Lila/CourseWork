import abc


class DBContract(abc.ABC):
    @abc.abstractmethod
    def _insert_(self, insert_into_, what_, values_) -> bool:
        pass

    @abc.abstractmethod
    def _update_(self, update_, set_, where_) -> bool:
        pass

    @abc.abstractmethod
    def _select_(self, select_, from_, where_) -> list:
        pass

    @abc.abstractmethod
    def _delete_(self, from_, where_) -> bool:
        pass

    @abc.abstractmethod
    def _execute_(self, what_) -> bool:
        pass
