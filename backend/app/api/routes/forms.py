import os
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, UploadFile

from app.parser.xlsform_parser import XLSFormParser


router = APIRouter(
    prefix="/forms",
    tags=["forms"],
)


@router.post("/parse")
async def parse_form(
    file: UploadFile = File(...),
):
    contents = await file.read()

    with NamedTemporaryFile(
        suffix=".xlsx",
        delete=False,
    ) as temporary_file:
        temporary_file.write(contents)
        temporary_path = temporary_file.name

    try:
        parser = XLSFormParser()
        form = parser.parse(temporary_path)

        return {
            "id": form.id,
            "title": form.title,
            "version": form.version,
            "questions": [
                {
                    "name": question.name,
                    "type": question.type.value,
                    "label": question.label,
                    "required": question.required,
                    "choices": [
                        {
                            "value": choice.value,
                            "label": choice.label,
                        }
                        for choice in question.choices
                    ],
                    "relevance": (
                        question.relevance.expression
                        if question.relevance
                        else None
                    ),
                    "constraint": (
                        question.constraint.expression
                        if question.constraint
                        else None
                    ),
                }
                for question in form.questions
            ],
        }
    finally:
        os.unlink(temporary_path)
