import markdown
import requests
import base64
import service.holt_model_service as holt
import service.layoutlm_service as nlp

from io import BytesIO

from persistance.repository import publication_repository as repository
from persistance.entities.model import Publication

from broker.rabbit_broker import message_producer
from broker.events import PublicationResourceEvent

from typing import List
from fpdf import FPDF
from PyPDF2 import PdfReader

from exeption.entity import EntityNotFoundException
from web.dto.publication import (
    PublicationRequest,
    ChatbotSomeRequest,
    ChatbotSomeResponse,
    PublicationResponse,
    PublicationPolarityResponse,
    PolarityFrom,
    ChartData
)


async def get_publications(type) -> List[PublicationResponse]:
    publications = await repository.find_all_publications(type)
    return list(map(_to_response, publications))


async def get_user_publications(userUuid, type) -> List[PublicationResponse]:
    publications = await repository.find_all_user_publications(userUuid, type)
    return list(map(_to_response, publications))


def publication_polarity(userUuid):
    result = repository.get_publication_polarity(userUuid)
    publications_dict = {}
    for row in result:
        publication_body = row.publication
        publication_uuid = row.publication_uuid
        chart_data = ChartData(
            polarity=row.DayPolarity,
            month=row.month,
            day=row.day,
            date=row.date.strftime('%Y-%m-%d')
        )

        if publication_uuid not in publications_dict:
            publications_dict[publication_uuid] = {
                "publication_body": publication_body,
                "polarity": []
            }

        publications_dict[publication_uuid]["polarity"].append(chart_data)

    response_data = [
        PolarityFrom(
            publication=publication_info["publication_body"],
            publication_uuid=publication_uuid,
            polarity=publication_info["polarity"]
        )
        for publication_uuid, publication_info in publications_dict.items()
    ]

    models = holt.holt_models(PublicationPolarityResponse(data=response_data))

    for item in response_data:
        if item.publication_uuid in models:
            item.forecast = models[item.publication_uuid].tolist()

    return PublicationPolarityResponse(data=response_data)


async def get_publication_by_id(publication_id) -> Publication:
    return await repository.find_publication_by_id(publication_id)


async def create_publication(publication_request: PublicationRequest) -> PublicationResponse:
    publication = repository.create_publications(publication_request)

    result = publication_request.resource

    message_producer.send_message(PublicationResourceEvent(
        resource=result,
        resource_type=publication_request.resource_type,
        owner_type='PUBLICATION',
        owner_resource_type='',
        owner_uuid=publication.uuid,
    ))

    return _to_response(publication)


async def chatbot(request: ChatbotSomeRequest):
    publication = await get_publication_by_id(request.publication_uuid)

    if publication is None:
        raise EntityNotFoundException("Publication not found")

    url = f"http://52.7.145.183:3000/api/v1/resources/publication/{request.publication_uuid}"
    document_response = requests.request("GET", url, headers={}, data={})
    document_response = document_response.json()

    response = requests.get(document_response['data'])
    if response.status_code != 200:
        raise Exception("Error while fetching the file")

    file_content = response.content
    pdf_file = BytesIO(file_content)
    pdf_reader = PdfReader(pdf_file)

    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text().replace("\n", " ")

    result = nlp.model(
        question=request.body,
        context=text
    )

    return ChatbotSomeResponse(response=result['answer'])


# def _base64_to_pdf_content(base64_string: str) -> str:
#     pdf_data = base64.b64decode(base64_string)
#     pdf_file = BytesIO(pdf_data)
#     reader = PdfFileReader(pdf_file)
#     content = ""
#     for page_num in range(reader.numPages):
#         page = reader.getPage(page_num)
#         content += page.extract_text()
#     return content
#
#
# def _markdown_to_pdf(md_text: str) -> str:
#     html = markdown.markdown(md_text)
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(0, 10, html)
#
#     pdf_output = BytesIO()
#     pdf.output(pdf_output)
#     pdf_output.seek(0)
#
#     pdf_base64 = base64.b64encode(pdf_output.read()).decode('utf-8')
#     return pdf_base64


def _to_response(publication: Publication) -> PublicationResponse:
    return PublicationResponse(
        publication_uuid=publication.uuid,
        body=publication.body,
        type=publication.type,
        secondary_item_uuid=publication.secondary_item_uuid,
        created_at=publication.created_at.strftime('%Y-%m-%d'),
        user_uuid=publication.user_uuid
    )
