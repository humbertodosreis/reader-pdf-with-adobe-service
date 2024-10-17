from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_renditions_element_type import \
    ExtractRenditionsElementType
import os.path
import zipfile
import json
import pandas as pd
import re
import openpyxl
from datetime import datetime


def adobeLoader(input_pdf, output_zip_path,client_id, client_secret):
    """
    Function to run adobe API and create output zip file
    """
    # Initial setup, create credentials instance.
    credentials = Credentials.service_principal_credentials_builder() \
        .with_client_id(client_id) \
        .with_client_secret(client_secret) \
        .build()

    # Create an ExecutionContext using credentials and create a new operation instance.
    execution_context = ExecutionContext.create(credentials)
    extract_pdf_operation = ExtractPDFOperation.create_new()

    # Set operation input from a source file.
    source = FileRef.create_from_local_file(input_pdf)
    extract_pdf_operation.set_input(source)

    # Build ExtractPDF options and set them into the operation
    extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
        .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \
        .with_elements_to_extract_renditions([ExtractRenditionsElementType.TABLES,
                                                ExtractRenditionsElementType.FIGURES]) \
        .build()
    extract_pdf_operation.set_options(extract_pdf_options)

    # Execute the operation.
    result: FileRef = extract_pdf_operation.execute(execution_context)

    # Save result to output path
    if os.path.exists(output_zip_path):
        os.remove(output_zip_path)
    result.save_as(output_zip_path)


if __name__ == '__main__':
    print('Reading PDF with Adobe Service')

    # Define input and output file path
    input_pdf = 'input.pdf'
    output_zip_path = 'output.zip'
    client_id = ''
    client_secret = ''

    # Define client_id and client_secret
    adobeLoader(input_pdf, output_zip_path, client_id, client_secret)

    print('Reading PDF with Adobe Service - Done')