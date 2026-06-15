from sqlmodel import Session, select
from app.core.database import engine
from app.models.curso_model import Curso
from app.models.disciplina_model import Disciplina
from app.models.usuario_model import Usuario
from app.models.professor_model import Professor
from app.models.aluno_model import Aluno
from app.models.turma_model import Turma
from app.core.security import get_password_hash
from faker import Faker


def seed_initial_data():
    fake = Faker()
    with Session(engine) as session:
        # Cursos
        if not session.exec(select(Curso).limit(1)).first():
            cursos = [
                Curso(nome="Engenharia"),
                Curso(nome="Ciência da Computação"),
                Curso(nome="Matemática Aplicada"),
            ]
            session.add_all(cursos)
            session.commit()

        # Disciplinas
        if not session.exec(select(Disciplina).limit(1)).first():
            disciplinas = []
            for i in range(6):
                nome = f"{fake.unique.word().capitalize()} {fake.word().capitalize()}"
                codigo = f"DISC{i+100}"
                disciplinas.append(Disciplina(nome=nome, codigo=codigo))
            session.add_all(disciplinas)
            session.commit()

        # Professores
        if not session.exec(select(Professor).limit(1)).first():
            professors = []
            for _ in range(5):
                name = fake.name()
                email = fake.unique.email()
                professors.append(Professor(nome=name, email=email))
            session.add_all(professors)
            session.commit()

        

        # Alunos
        if not session.exec(select(Aluno).limit(1)).first():
            cursos = session.exec(select(Curso)).all()
            alunos = []
            for i in range(10):
                name = fake.name()
                email = fake.unique.email()
                matricula = str(fake.random_number(digits=8, fix_len=True))
                curso_id = cursos[i % len(cursos)].id
                alunos.append(Aluno(nome=name, email=email, matricula=matricula, curso_id=curso_id))
            session.add_all(alunos)
            session.commit()

        # Usuários
        if not session.exec(select(Usuario).limit(1)).first():
            usuarios = []
            profs = session.exec(select(Professor)).all()
            for p in profs[:3]:
                usuarios.append(Usuario(username=p.email, hashed_password=get_password_hash("password"), is_professor=True, is_aluno=False))

            alunos = session.exec(select(Aluno)).all()
            for a in alunos[:3]:
                usuarios.append(Usuario(username=a.email, hashed_password=get_password_hash("password"), is_professor=False, is_aluno=True))

            usuarios.append(Usuario(username="admin@example.com", hashed_password=get_password_hash("admin123"), is_admin=True, is_aluno=False, is_professor=False))
            session.add_all(usuarios)
            session.commit()

        # Turmas
        if not session.exec(select(Turma).limit(1)).first():
            disciplinas = session.exec(select(Disciplina)).all()
            professores = session.exec(select(Professor)).all()
            turmas = []
            periods = ["2024.1", "2024.2", "2025.1"]
            for i, d in enumerate(disciplinas):
                turma = Turma(
                    descricao=f"{d.nome} - Turma A",
                    horario="Seg 14:00-16:00",
                    periodo=periods[i % len(periods)],
                    codigo_acesso=f"ACESSO{i+1:03}",
                    disciplina_id=d.id,
                    professor_id=professores[i % len(professores)].id,
                )
                turmas.append(turma)
            session.add_all(turmas)
            session.commit()


__all__ = ["seed_initial_data"]
