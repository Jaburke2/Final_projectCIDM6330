import abc
from SocialService.domain import models
from SocialService.adapters import orm


class AbstractSocialServicesRepository(abc.ABC):
    def __init__(self):
        self.seen = []

    def add(self, service: models.Service):
        self._add(service)
        self.seen.append(service)

    def get(self, service_name) -> models.Service:
        service = self._get(service_name)
        if service:
            self.seen.append(service)
        return service

    def get_by_service_name(self, service_name) -> models.Service:
        service = self._get(service_name)
        if service:
            self.seen.add(service)
        return service

    def updateServiceQty(self, service_name, qty) -> models.Service:
        service1 = self._getSocialService(service_name)
        if service1.qty >= qty:
            service = self._update(service_name, service1.qty - qty)

    @abc.abstractmethod
    def _add(self, service: models.Service):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, service_name) -> models.Service:
        raise NotImplementedError

    @abc.abstractmethod
    def _getSocialService(self, service_name) -> models.SocialService:
        raise NotImplementedError

    @abc.abstractmethod
    def _update(self, service_name, qty) -> models.Service:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_by_batchref(self, service_name) -> models.Service:
        raise NotImplementedError


class SqlAlchemySocialServicesRepository(AbstractSocialServicesRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, service):
        self.session.add(service)

    def _get(self, service_name):
        return self.session.query(models.Service).filter_by(service_name=service_name).first()

    def _getSocialService(self, service_name):
        return self.session.query(models.SocialService).filter_by(service_name=service_name).first()

    def _update(self, service_name, quantity):
        return self.session.query(models.SocialService).filter_by(service_name=service_name).update(
            {models.SocialService.qty: quantity}, synchronize_session='evaluate'
        )
    
    def get_by_batchref(self, service_name):
        return self._get_by_batchref(service_name)

    def _get_by_batchref(self, service_name):
        return (
            self.session.query(models.Service)
            .join(models.SocialService)
            .filter(
                orm.socialServices.service_name == service_name,
            )
            .first()
        )
