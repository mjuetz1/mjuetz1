import os
import pickle

from google.auth.transport.requests import Request

from google_auth_oauthlib.flow import InstalledAppFlow
from llama_index import GPTSimpleVectorIndex, download_loader


os.environ['OPENAI_API_KEY'] = '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'


def authorize_gdocs():
    google_oauth2_scopes = [
        "https://www.googleapis.com/auth/documents.readonly"
    ]
    cred = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", 'rb') as token:
            cred = pickle.load(token)
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", google_oauth2_scopes)
            cred = flow.run_local_server(port=0)
        with open("token.pickle", 'wb') as token:
            pickle.dump(cred, token)


if __name__ == '__main__':

    authorize_gdocs()
    GoogleDocsReader = download_loader('GoogleDocsReader')
    gdoc_ids = ['1s5EYVLXqQQtpRE_yf16wzZXPO3Gw8h1o36qwb1G94Q0']
    loader = GoogleDocsReader()
    documents = loader.load_data(document_ids=gdoc_ids)
    index = GPTSimpleVectorIndex(documents)

    while True:
        prompt = input("Type prompt...")
        response = index.query(prompt)
        print(response)

        # Get the last token usage
        last_token_usage = index.llm_predictor.last_token_usage
        print(f"last_token_usage={last_token_usage}")
# # Save your index to a index.json file
# index.save_to_disk('index.json')
# # Load the index from your saved index.json file
# index = GPTSimpleVectorIndex.load_from_disk('index.json')