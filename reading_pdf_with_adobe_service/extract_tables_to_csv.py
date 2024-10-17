import logging
import os.path

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_renditions_element_type import \
    ExtractRenditionsElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.table_structure_type import TableStructureType
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

try:
    # get base path.
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    input_file = base_path + "/reading-pdf-with-adobe-service/resources/itau_extrato_032024.pdf"
    output_file = base_path + "/reading-pdf-with-adobe-service/output/itau_extrato_032024_v2.zip"

    # print(base_path)

    # exit(0)

    # Initial setup, create credentials instance.
    credentials = Credentials.service_principal_credentials_builder(). \
        with_client_id(os.getenv('PDF_SERVICES_CLIENT_ID')). \
        with_client_secret(os.getenv('PDF_SERVICES_CLIENT_SECRET')). \
        build()

    # Create an ExecutionContext using credentials and create a new operation instance.
    execution_context = ExecutionContext.create(credentials)
    extract_pdf_operation = ExtractPDFOperation.create_new()

    # Set operation input from a source file.
    source = FileRef.create_from_local_file(input_file)
    extract_pdf_operation.set_input(source)

    # Build ExtractPDF options and set them into the operation
    extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
        .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \
        .with_element_to_extract_renditions(ExtractRenditionsElementType.TABLES) \
        .with_table_structure_format(TableStructureType.CSV) \
        .build()
    
    # extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
    #     .with_element_to_extract(ExtractElementType.TEXT) \
    #     .with_element_to_extract(ExtractElementType.TABLES) \
    #     .with_table_structure_format(TableStructureType.CSV) \
    #     .build()
    
    extract_pdf_operation.set_options(extract_pdf_options)

    # Execute the operation.
    result: FileRef = extract_pdf_operation.execute(execution_context)

    # Save result to output path
    if os.path.exists(output_file):
        os.remove(output_file)

    # Save the result to the specified location.
    result.save_as(output_file)
except (ServiceApiException, ServiceUsageException, SdkException):
    logging.exception("Exception encountered while executing operation")