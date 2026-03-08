from rag_engine import retrieve_schemes
import boto3

client = boto3.client(
    "bedrock-runtime",
    region_name=st.secrets["us-east-1"],
    aws_access_key_id=st.secrets["AKIAX4UUU3VRD7Z2CH4B"],
    aws_secret_access_key=st.secrets["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"]
)

def explain_schemes(profile, user_query):

    schemes = retrieve_schemes(user_query)

    prompt = f"""
You are Bharat Sahayak AI helping Indian citizens understand government schemes.

Citizen profile:
{profile}

Relevant schemes retrieved from knowledge base:
{schemes}

Explain which schemes match the citizen and why in simple Hindi.
"""

    response = client.converse(
        modelId="meta.llama3-8b-instruct-v1:0",
        messages=[{
            "role":"user",
            "content":[{"text":prompt}]
        }]
    )

    return response["output"]["message"]["content"][0]["text"]


# -----------------------------------
# AI Application Guide
# -----------------------------------

def application_guide(scheme):

    prompt = f"""
Explain how a citizen can apply for this government scheme.

Scheme:
{scheme['name']}

Give step-by-step instructions in simple Hindi.
"""

    response = client.converse(
        modelId="meta.llama3-8b-instruct-v1:0",
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ]
    )

    return response["output"]["message"]["content"][0]["text"]
