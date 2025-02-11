import test_settings
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import json

# 클라이언트 생성
azure_di_client = DocumentAnalysisClient(
    test_settings.AZURE_DI_ENDPOINT_URL,
    AzureKeyCredential(test_settings.AZURE_DI_API_KEY)
)

# 분석 요청
with open(test_settings.FILE_FULL_NAME, 'rb') as rb_file:
    azure_di_poller = azure_di_client.begin_analyze_document('prebuilt-layout', rb_file)
    azure_di_result = azure_di_poller.result()

# 결과 출력
print(json.dumps(azure_di_result.to_dict(), indent=2))
