from rag_engine import retrieve_schemes
import boto3
import streamlit as st
import json

client = boto3.client(
    "bedrock-runtime",
    region_name=st.secrets["AWS_DEFAULT_REGION"],
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
)

def explain_schemes(profile, schemes):

    prompt = f"""
You are Bharat Sahayak AI helping Indian citizens understand government schemes.

Citizen profile:
{profile}

Relevant schemes:
{schemes}

Explain why these schemes match the citizen in simple Hindi.
"""

    body = {
        "prompt": prompt,
        "max_gen_len": 512,
        "temperature": 0.5
    }

    response = client.invoke_model(
        modelId="meta.llama3-8b-instruct-v1",
        body=json.dumps(body)
    )

    result = json.loads(response["body"].read())

    return result["generation"]


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
