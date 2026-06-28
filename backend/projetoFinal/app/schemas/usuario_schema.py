from sqlmodel import SQLModel, Field

class UsuarioCreate(SQLModel):
    username: str
    password: str
    is_aluno: bool = True       
    is_professor: bool = False 

class UsuarioRead(SQLModel):
    id: int
    username: str
    is_active: bool
    is_aluno: bool
    is_professor: bool
    is_admin: bool

class UsuarioTrocaSenha(SQLModel):
    id: int
    old_password: str
    new_password: str

class UsuarioUpdate(SQLModel):
    is_active: bool
    is_aluno: bool
    is_professor: bool
    is_admin: bool