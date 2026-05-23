from sqlmodel import SQLModel, Field

class UsuarioCreate(SQLModel):
    username: str = Field(index=True, min_length=5, max_length=100)
    password: str

class UsuarioRead(SQLModel):
    id: int
    username: str
    is_active: bool
    is_aluno: bool
    is_monitor: bool
    is_professor: bool
    is_admin: bool

class UsuarioTrocaSenha(SQLModel):
    id: int
    old_password: str
    new_password: str

class UsuarioUpdate(SQLModel):
    is_active: bool
    is_aluno: bool
    is_monitor: bool
    is_professor: bool
    is_admin: bool