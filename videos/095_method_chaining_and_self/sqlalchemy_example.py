from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    addresses = relationship("Address",
                             back_populates="user",
                             cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"




def demo_method_chaining(session):
    stmt = (
        select(Address)
            .join(Address.user)
            .where(User.name == "sandy")
            .where(Address.email_address == "sandy@sqlalchemy.org")
    )

    print(type(stmt))
    print()
    print(stmt)






    # sandy_address = session.scalars(stmt).one()
    # print(sandy_address)


def add_demo_users(session):
    """Add spongebob, sandy, patrick to db"""
    spongebob = User(
        name="spongebob",
        fullname="Spongebob Squarepants",
        addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    )
    sandy = User(
        name="sandy",
        fullname="Sandy Cheeks",
        addresses=[
            Address(email_address="sandy@sqlalchemy.org"),
            Address(email_address="sandy@squirrelpower.org"),
        ],
    )
    patrick = User(name="patrick", fullname="Patrick Star")
    session.add_all([spongebob, sandy, patrick])
    session.commit()



def main():
    # use in-memory database for demonstration purposes
    engine = create_engine("sqlite://", echo=False, future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        add_demo_users(session)
        demo_method_chaining(session)


if __name__ == '__main__':
    main()
