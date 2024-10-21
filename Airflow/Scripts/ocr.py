import os
import PyPDF2
import re
import glob
import logging

from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.ocr_pdf_job import OCRPDFJob
from adobe.pdfservices.operation.pdfjobs.params.ocr_pdf.ocr_params import OCRParams
from adobe.pdfservices.operation.pdfjobs.params.ocr_pdf.ocr_supported_locale import OCRSupportedLocale
from adobe.pdfservices.operation.pdfjobs.params.ocr_pdf.ocr_supported_type import OCRSupportedType
from adobe.pdfservices.operation.pdfjobs.result.ocr_pdf_result import OCRPDFResult

from adobe.pdfservices.operation.config.client_config import ClientConfig

from adobe.pdfservices.operation.pdfjobs.jobs.split_pdf_job import SplitPDFJob
from adobe.pdfservices.operation.pdfjobs.params.split_pdf.split_pdf_params import SplitPDFParams
from adobe.pdfservices.operation.pdfjobs.result.split_pdf_result import SplitPDFResult

ocr_path = r"C:\Users\Mateusz\pipeline\transform\r"
       
def main():
    try:
        pdf_files = glob.glob(os.path.join(ocr_path, '*.pdf'))
        for f in pdf_files:
            with open(f, 'rb') as file:
                input_stream = file.read()
            file.close()
   
            # Initial setup, create credentials instance
            credentials = ServicePrincipalCredentials(
                client_id,
                client_secret
            )
   
            # Creates client config instance with custom time-outs.
            client_config: ClientConfig = ClientConfig(
                connect_timeout=3*60000,
                read_timeout=3*60000,
            )
   
            # Creates a PDF Services instance
            pdf_services = PDFServices(
                credentials=credentials,
                client_config=client_config
            )
   
            # Creates an asset(s) from source file(s) and upload
            input_asset = pdf_services.upload(input_stream=input_stream,
                                              mime_type=PDFServicesMediaType.PDF)
   
            ocr_pdf_params = OCRParams(
                ocr_locale=OCRSupportedLocale.PL_PL,
                ocr_type=OCRSupportedType.SEARCHABLE_IMAGE
            )
   
            # Implementing PDF page split
            split_pdf_params = SplitPDFParams(page_count=1)
            split_pdf_job = SplitPDFJob(input_asset, split_pdf_params)
            location = pdf_services.submit(split_pdf_job)
            pdf_services_response = pdf_services.get_job_result(location, SplitPDFResult)
            result_assets = pdf_services_response.get_result().get_assets()
   
            # Creates a new job instance
            ocr_pdf_job = OCRPDFJob(input_asset=result_assets[0], ocr_pdf_params=ocr_pdf_params)
   
            # Submit the job and gets the job result
            location = pdf_services.submit(ocr_pdf_job)
            pdf_services_response = pdf_services.get_job_result(location, OCRPDFResult)
   
            # Get content from the resulting asset(s)
            result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)
   
            # Creates an output stream and copy stream asset's content to it
            filename = os.path.basename(f)
            new_path = os.path.join(current_dir, filename)
            with open(new_path, "wb") as file:
                file.write(stream_asset.get_input_stream())
   
    except (ServiceApiException, ServiceUsageException, SdkException) as e:
        logging.exception(f'Exception encountered while executing operation: {e}')
   
if __name__ == "__main__":
    main()