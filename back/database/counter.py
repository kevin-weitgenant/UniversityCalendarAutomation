from sqlalchemy import Boolean, Column, Integer, String, create_engine, exc
from sqlalchemy.orm import declarative_base, Session, sessionmaker
import os

# Get environment variable for DATABASE_URL or use default
DATABASE_URL = os.getenv('DATABASE_URL', "postgresql://postgres:123@localhost:5432/postgres")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Counter(Base):
    __tablename__ = "calendarCounter"

    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer, default=0)

def get_db():
    try:
        db = SessionLocal()
        try:
            yield db
        except Exception as e:
            print(f"An error occurred while processing the request: {e}")
            db.rollback()
        finally:
            db.close()
    except exc.SQLAlchemyError as e:
        print(f"Could not connect to the database: {e}")


def increment_count():
    try:
        db = next(get_db())
        counter = db.query(Counter).first()
        if counter is None:
            # if counter does not exist, create it
            counter = Counter(count=0)
            db.add(counter)
            
        counter.count += 1
        db.commit()
        print(f"Incremented count to {counter.count}")
    except exc.SQLAlchemyError as e:
        print(f"An error occurred while incrementing count: {e}")
    except StopIteration:
        print("Error while getting database connection.")
    finally:
        db.close()


def get_count():
    try:
        db = next(get_db())
        counter = db.query(Counter).first()
        if counter is not None:
            return counter.count
        else:
            return 0
    except exc.SQLAlchemyError as e:
        print(f"An error occurred while fetching count: {e}")
        return None
    except StopIteration:
        print("Error while getting database connection.")
        return None
    finally:
        db.close()

if __name__ == '__main__':
    print(increment_count())