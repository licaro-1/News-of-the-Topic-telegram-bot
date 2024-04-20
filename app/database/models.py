from sqlalchemy.orm import (DeclarativeBase, 
                            Mapped, 
                            mapped_column)


class Base(DeclarativeBase):

    repr_cols_num = 3
    repr_cols = tuple()
    
    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(default="nousername")
    tg_id: Mapped[int]
    messages_count: Mapped[int] = mapped_column(default=0)
    nav_moves_count: Mapped[int] = mapped_column(default=0)
