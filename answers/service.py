from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from company.dao import CompanyDAO
from entity.dao import EntityDAO
from fields.dao import EntityFieldDAO
from answers.dao import EntityAnswerDAO
from records.dao import EntityRecordDAO
from utils.schema import EntityRecordSchema
from model import EntityRecordInput
from utils.schema import EntityAnswerSchema


class EntityAnswerService:

    def __init__(self, database: Session):
        self.database = database

        self.entity_answer_dao = EntityAnswerDAO(database)
        self.field_dao = EntityFieldDAO(database)
        self.record_dao = EntityRecordDAO(database)
        self.entity_dao = EntityDAO(database)
        self.company_dao = CompanyDAO(database)

    def create(self, data: EntityRecordInput ):

        # --------------------------------------------------
        # 1. Verificar Entity
        # --------------------------------------------------

        entity = self.entity_dao.find_by_id(
            data.entity_id
        )

        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found"
            )

        # --------------------------------------------------
        # 2. Verificar Company
        # --------------------------------------------------

        company = self.company_dao.find_by_id(
            data.company_id
        )

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )

        # --------------------------------------------------
        # 3. Verificar se Entity pertence à Company
        # --------------------------------------------------

        if entity.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Entity does not belong to company"
            )

        # --------------------------------------------------
        # 4. Validar todos os campos enviados
        # --------------------------------------------------

        validated_answers = []

        for answer in data.answers:

            field = self.field_dao.find_by_label_and_entity(answer.label,entity.id)

            if not field:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=(
                        f"Field '{answer.label}' "
                        f"not found for entity {entity.id}"
                    )
                )

            validated_answers.append(
                {
                    "field": field,
                    "value": answer.value
                }
            )

        # --------------------------------------------------
        # 5. Criar apenas UM EntityRecord
        # --------------------------------------------------

        new_record = EntityRecordSchema(
            entity_id=entity.id,
            company_id=company.id
        )

        record_entity = self.record_dao.create(
            new_record
        )

        # --------------------------------------------------
        # 6. Criar todas as respostas
        # --------------------------------------------------

        created_answers = []

        for item in validated_answers:

            field = item["field"]
            value = item["value"]

            new_answer = EntityAnswerSchema(
                entity_record_id=record_entity.id,
                entity_field_id=field.id,
                value=value
            )

            created_answer = (
                self.entity_answer_dao.create(
                    new_answer
                )
            )

            created_answers.append(
                created_answer
            )

        # --------------------------------------------------
        # 7. Retorno
        # --------------------------------------------------

        return {
            "record": record_entity,
            "answers": created_answers
        }





# from utils.database import SessionLocal
# database = SessionLocal()
#
# try:
#     service = EntityAnswerService(database)
#     data = EntityRecordInput(
#         entity_id=1,
#         company_id=1,
#         answers=[
#             {
#                 "label": "Nome",
#                 "value": "Ven"
#             },
#             {
#                 "value": "Mhu",
#                 "label": "Apelido"
#             },
#             {
#                 "value": 53,
#                 "label": "Idade"
#             },
#             {
#                 "label": "Observacao",
#                 "value": "sdsa dfsfs sdfsd s"
#             }
#         ]
#     )
#     result = service.create(data)
#
#     print("RESULTADO:")
#     print(result)
#
# finally:
#     database.close()

