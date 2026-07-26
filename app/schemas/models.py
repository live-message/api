from sqlmodel import Field, SQLModel


class Servers(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field()
    adress: str = Field()
    port: int = Field()
