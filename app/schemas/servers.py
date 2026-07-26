from sqlmodel import SQLModel


class Servers(SQLModel):
    name: str
