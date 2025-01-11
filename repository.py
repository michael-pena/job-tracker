from sqlalchemy.orm import Session
from application import Application

class ApplicationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(Application).all()

    def get_count(self):
        return self.session.query(Application).count()

    def get_count_by_status(self, status):
        return self.session.query(Application).filter(Application.status == status).count()

    def get_count_by_offer(self, offer):
        return self.session.query(Application).filter(Application.offer == offer).count()

    def get_count_by_all_offers(self):
        return self.session.query(Application).filter(Application.offer.in_(['yes', 'no'])).count()
    
    def get_count_by_all_accepted(self):
        return self.session.query(Application).filter(Application.accepted.in_(['yes', 'no'])).count()
    
    def get_count_by_accepted(self, accepted):
        return self.session.query(Application).filter(Application.accepted == accepted).count()

    def insert(self, company, position, date, status, offer, accepted):
        application = Application(company, position, date, status, offer, accepted)
        self.session.add(application)
        self.session.commit()

    def update(self, application_id, **kwargs):
        application = self.session.query(Application).filter(Application.id == application_id).first()
        if application:
            for key, value in kwargs.items():
                setattr(application, key, value)
            self.session.commit()

    def delete(self, application_id):
        application = self.session.query(Application).filter(Application.id == application_id).first()
        if application:
            self.session.delete(application)
            self.session.commit()