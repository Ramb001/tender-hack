from ragflow_client import RAGFlowAPIClient


class AnalyzeDocument:
    def __init__(self):
        self.ragflow_client = RAGFlowAPIClient()
        self.session = None
        self.chat_id = None
        self.documents = []
        self.datasets_ids = []

    def create_session(self, name="New Session", ttl=3600, metadata=None):
        self.session = self.ragflow_client.create_session(
            name=name, ttl=ttl, metadata=metadata
        )
        return self.session

    def upload_document(self, file_path, description=None):
        return self.ragflow_client.upload_document(file_path, description=description)

    def create_and_upload_dataset(
        self, dataset_name, dataset_path, description=None, metadata=None
    ):
        dataset = self.ragflow_client.create_dataset(
            name=dataset_name, description=description, metadata=metadata
        )
        self.ragflow_client.upload_dataset(
            dataset_path, description=description, metadata=metadata
        )
        return dataset

    def list_datasets(self):
        return self.ragflow_client.list_datasets()

    def ask_question(self, question):
        if self.session:
            return self.ragflow_client.ask_question(
                session_id=self.session["id"], question=question
            )
        else:
            raise Exception("Session not created. Please create a session first.")


def analyze_and_ask(document_path, question, session_name="Analysis Session"):
    analyzer = AnalyzeDocument()
    session = analyzer.create_session(name=session_name)
    analyzer.upload_document(
        document_path, description="Analyzing document for insights"
    )
    response = analyzer.ask_question(question)

    return response
