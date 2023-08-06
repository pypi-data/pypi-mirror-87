import logging
from typing import Optional, Text, Union, List, Dict
logger = logging.getLogger(__name__)
import uuid
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from sqlalchemy.orm import Session
from ragex.community.database.service import DbService
from ragex.community.database.response import IntentResTemplate
from ragex.community.utils import QueryResult


class ResponseService(DbService):
    def __init__(self, session: Session, image_directory: Text):
        self.image_directory = image_directory
        super().__init__(session)

    def get_response_templates(self, project_id: Text,
                               limit: Optional[int] = None,
                               offset: Optional[int] = None) -> QueryResult:
            # List[Dict[Text, Union[Text, List[Text]]]]:
        response_templates = self.query(IntentResTemplate)

        total_number_response_templates = response_templates.count()

        response_templates = (
            response_templates.order_by(IntentResTemplate.intent.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        results = []
        for r in response_templates:
            response = r.as_dict()
            response["id"] = uuid.uuid4().hex
            results.append(response)

        return QueryResult(results, total_number_response_templates)

    def get_response_intent_template(self, project_id: Text,
                              intent: Optional[Text] = None) -> QueryResult:
        response_template = self.query(IntentResTemplate).filter(IntentResTemplate.intent == intent)

        total_number_response = response_template.count()
        response_template = (
            response_template.order_by(IntentResTemplate.intent.asc())
            .all()
        )

        result = [r.as_dict() for r in response_template]

        return QueryResult(result, total_number_response)

    """
    @ deprecated method
    """
    def get_response_template(self, project_id: Text,
                              intent: Optional[Text] = None,
                              response_type: Optional[Text] = None) -> QueryResult:
        response_template = self.query(IntentResTemplate).filter(
            and_(IntentResTemplate.intent == intent , IntentResTemplate.response_type == response_type))

        total_number_response = response_template.count()
        response_template = (
            response_template.order_by(IntentResTemplate.response_type.asc())
            .all()
        )

        result = [r.as_dict() for r in response_template]

        return QueryResult(result, total_number_response)

    def delete_response_template(self, intent: Optional[Text] = None):
        """ intent 일치하는 항목 삭제
            response_type 항목 삭
         """
        self.query(IntentResTemplate).filter(
            and_(IntentResTemplate.intent == intent)
        ).delete()

    def add_response_template(self, intent: Text, use_yn: Text, response_template: Text, response_title: Text, content_type: Text):

        exist_row = self.query(IntentResTemplate).filter(
            and_(
                IntentResTemplate.intent == intent
            )
        ).first()

        exist_y = self.query(IntentResTemplate).filter(
            and_(
                IntentResTemplate.intent == intent,
                IntentResTemplate.use_yn == "Y"
            )
        ).first()

        if exist_row is not None:
            raise ValueError("check exist row intent response template ")

        if exist_y is not None and use_yn == "Y":
            raise ValueError("check unique intent response template use_yn Y")

        if use_yn not in ['Y', 'N']:
            raise ValueError("check unique intent response template use_yn range")

        add_response = IntentResTemplate(
            intent=intent,
            use_yn=use_yn,
            response_template=response_template,
            response_title=response_title,
            content_type=content_type
        )

        self.add(add_response)

    def update_response_template(self,intent: Text, use_yn: Text, response_template: Text, response_title: Text, content_type: Text):

        if use_yn not in ['Y', 'N']:
            raise ValueError("check unique intent response template use_yn range")

        exist_row = self.query(IntentResTemplate).filter(
            and_(
                IntentResTemplate.intent == intent
            )
        ).first()

        if exist_row is None:
            raise ValueError("check not exist row intent response template ")

        # 주석 처리 - 2020.03.18
        # exist_y = self.query(IntentResTemplate).filter(
        #     and_(
        #         IntentResTemplate.intent == intent,
        #         IntentResTemplate.use_yn == "Y"
        #     )
        # ).first()
        #
        # if exist_y is not None and use_yn == "Y":
        #     raise ValueError("check unique intent response template use_yn Y")

        update_response = IntentResTemplate(
            intent=intent,
            use_yn=use_yn,
            response_template=response_template,
            response_title=response_title,
            content_type=content_type
        )

        self.merge(update_response)
