"""
list address: curl -X GET https://main-wjaxre4ena-uc.a.run.app/usage_addresses
usage by address: curl -X GET https://main-wjaxre4ena-uc.a.run.app/usage_records/<address>
google storage bucket: https://storage.googleapis.com/contextpilot/summary_data/<session_id>.json
please complete python code for fetching data from the url above. replace url to env variables.
1. listing addresses from first url;
   response: ["0x7d6eAFf632Bb4c36207D8e1363D4B40EC323c41c","0xe9627177fCf4fB212bA20f8ebf184e91E5Aeccdf","0x032995de5c5D6ee2352595887fE5379e77606004","0x40FCB3d0C045C00AdcfDDB3E20d8F336d2155D0C","0xDummyAddress","0x93513A4fAe6df9A730aE19F538205b8170AE5D6F","0x5C9d7Aa2104Ca9C5e397aA85b9589499561b6CaC","0x7742673DfE616d8f8242B6666E765BACf1E72F9c"]
2. batch fetching usage records by address retrieve from step 1 and insert into database.
    response: ["afb5aa85-460e-49bf-9b2c-8688f8bdf9fd","f3514c2f-766e-44e0-9b0b-62eefcf180af","5d1f7ae1-d248-4508-a5ea-264d8c922340","273c2e34-0705-4eb0-b42b-bbc583222bf5","c1c68cd4-bd77-4f32-a6c7-e84eb1393215","a7923ef2-9c7f-48ee-80f0-ec6a46739db5","44e1c38d-7443-4536-9c03-b3d385c52fbb","6301b88f-f413-40fa-9383-eaeddafa243d","081b114c-b680-498c-97d0-4bba89a1941b","a07b49e9-1b34-45ed-9242-a32b39b2ecb3","7aa4b74e-d175-4973-a6c0-675fcfbf1fce","0417bdf8-c5c5-4566-af6a-3a6aef87f0c5","788dc27a-1980-4edd-9fa3-8976c5e53c1f","25646ee9-5366-4c84-b400-1c0deda511a4","8fe547cb-14db-45d5-a97f-fde626e10ccc","c4ef937e-1a03-45c9-be1b-b68836ddb1fb","56aa717e-35d8-4d85-84d8-93a7f732ae64"]
3. batch fetching json data from url 3 using session id retrieving step2.
    response: {"summary": "The chat consists of a conversation between a user seeking help with Python code and a system trained to provide software engineering advice. The user asks for assistance in writing code to extract a structure from a JSON representation and subsequently convert it into a formatted output.\n\n### User's Request and Code:\n1. **Primary Task**: The user is working on a Python script, `extract.py`, to extract data from a structured JSON object, and aims to complete a \"TODO\" section for reading file content and converting it to JSON. \n2. **Initial Code Sample**: The user provides an initial JSON structure starting with \"root\" and containing child nodes, along with a function `extract_structure(node)` designed to extract given fields from the JSON structure and return them in an organized way.\n\n### System\u2019s Explanation:\nThe system provides feedback and suggestions:\n1. **Understanding the JSON Structure**: The provided JSON is a nested structure representing a hierarchy with nodes and sub-nodes.\n2. **Example of Extraction Code**: The system explains how to utilize Python\u2019s `json` module for extracting and processing the JSON data efficiently.\n3. **Correcting Mistakes**: It points out a mistake in the user's use of the function call `'extract_structure'` which should just be `extract_structure`, emphasizing correct function call syntax.\n4. **File Reading**: Guidance is given on how to read from a JSON file using `json.load()`, process the data, and handle both dictionary and list types efficiently.\n\n### User's Follow-up Request:\nThe user subsequently shares additional details about their source data structure (from a `score_criteria.json`), which involves evaluation criteria organized into categories, each containing sub-criteria. The user also shares their proposed coding approach to adapt their previous logic for processing this new data.\n\n### System\u2019s Guidance:\nThe system provides further corrections and enhancements:\n1. It emphasizes the need to confirm the data type of the loaded JSON and handle it accordingly.\n2. It instructs on effectively formatting the output using `json.dump()` to write results back into a new output file.\n3. It reminds to maintain the correct JSON structure in outputs, summarizing that only JSON content should be written without extraneous information.\n\n### Conclusion:\nOverall, the conversation revolves around formulating a method to extract, convert, and format JSON data structures within Python, with the system providing step-by-step corrections, code examples, and clarifications to assist the user's programming efforts."}
Others:
1. you need to create table like this:
    class Book(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100), nullable=False)
        author = db.Column(db.String(100), nullable=False)
        published_date = db.Column(db.Date, nullable=False)
        price = db.Column(db.Float, nullable=False)

2. project using flask and Flask-SQLAlchemy framework
"""

import os
import re
import json
import requests
import logging
import google.generativeai as genai # pylint: disable=E0401
from datetime import datetime
from flask import Blueprint
from app.models import db, User, Score, ScoreRecord, ChatRecord

logger = logging.getLogger(__name__)

summary_score_manager = Blueprint('summary_score_manager', __name__)

def fetch_and_store_data():
    """
    fetch data
    """
    list_address_url = os.getenv('LIST_ADDRESS_URL')
    usage_records_url = os.getenv('USAGE_RECORDS_URL')
    google_storage_bucket_url = os.getenv('GOOGLE_STORAGE_BUCKET_URL')

    # Step 1: Fetch list of addresses
    addresses = []
    try:
        logger.info(f"fetch addresses:{list_address_url}")    # pylint: disable=W1203
        response = requests.get(list_address_url, timeout=10)
        response.raise_for_status()  # Check if the request was successful
        logger.info(f"fetch addresses result :{response.text}")    # pylint: disable=W1203
        addresses = json.loads(response.text)
        logger.info(f"convert addresses result :{addresses}")    # pylint: disable=W1203
        if not isinstance(addresses, list):
            logger.error(f"Expected a list, but got {type(addresses)}")    # pylint: disable=W1203
            return
    except requests.exceptions.RequestException as e:
        logger.error(f"URL: {list_address_url}, Error: {str(e)}")    # pylint: disable=W1203
        return
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from {list_address_url}, Error: {str(e)}")    # pylint: disable=W1203
        return
    # Step 2: Batch fetch usage records by address and insert into database
    for address in addresses:
        if not User.query.filter_by(address=address, is_deleted=False).first():
            user = User(address=address)
            db.session.add(user)
    
        fetch_session_uri = f"{usage_records_url}/{address}"
        logger.info(f"fetch session {fetch_session_uri}")    # pylint: disable=W1203
        response = requests.get(fetch_session_uri, timeout=5)
        logger.info(f"fetch session result {response.text}, type: {type(response.text)}")    # pylint: disable=W1203
        session_ids = json.loads(response.text)
        logger.debug(session_ids)

        # Step 3: Batch fetch JSON data using session id and store in database
        for session_id in session_ids:
            if ChatRecord.query.filter_by(session_id=session_id, is_deleted=False).first():
                continue

            fetch_session_content = f"{google_storage_bucket_url}/{session_id}.json"
            logger.info(f"fetch session content {fetch_session_content}")    # pylint: disable=W1203
            response = requests.get(fetch_session_content, timeout=5)
            logger.info(f"fetch session content result: {fetch_session_content}")    # pylint: disable=W1203
            summary_data = json.loads(response.text)

            # Assuming the fetched data needs to insert into "Book" table
            # Here you would typically map the JSON data to your database model
            # For demonstration purposes, let's pretend it contains Book details
            chat_record = ChatRecord(
                address = address,
                session_id = session_id,
                content = json.dumps(summary_data),
                created_at = datetime.now(),
                updated_at = datetime.now(),
            )
            logger.info(f"store chat_record: {chat_record}")    # pylint: disable=W1203
            db.session.add(chat_record)

        db.session.commit()
        logger.info(f"commit chat records for : {address}")    # pylint: disable=W1203

        # summary_score_by_address(address=address)

def batch_summary():
    """
    batch summary
    """
    users = User.query.filter_by(is_deleted=False).all()
    addresses = [user.address for user in users]
    for address in addresses:
        try:
            summary_score_by_address(address=address)
        except Exception as e:
            logger.error(e)

def summary_score_by_address(address):
    """
    query chatRecord by address, and append content as content pass to summary_score
    """
    logger.info(f"summary_score_by_address : {address}")
    records = ChatRecord.query.filter_by(address=address, is_deleted=False)
    contents = [r.content for r in records]
    combined_content = "\n".join(contents)
    logger.info(f"summary_score : {address}")
    result = summary_score(content=combined_content)
    if result:
        # Check if the score for this address already exists
        logger.info(f"query score : {address}")
        score_entry = Score.query.filter_by(address=address, is_deleted=False).first()
        if score_entry:
            # Update the existing score entry
            score_entry.score_json = json.dumps(result)
            score_entry.updated_at = datetime.now()
            logger.info(f"Updated score for address {address}")    # pylint: disable=W1203
        else:
            # Create a new score entry
            score_entry = Score(
                address=address,
                score_json=json.dumps(result),
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            db.session.add(score_entry)
            db.session.commit()
            logger.info(f"Created new score for address {address}")    # pylint: disable=W1203

        # Add entries to ScoreRecord table
        for record in records:
            score_record = ScoreRecord(
                score_id=score_entry.id,
                chat_id=record.id,
                score_json=json.dumps(result),
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            db.session.add(score_record)

        db.session.commit()

def summary_score(content):
    """
    invoke gemini to summary score
    """
    api_key = os.getenv('GEMINI_API_KEY')
    skill_list = os.getenv('SKILL_LIST')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = """
        You are a machine that only returns and replies with valid, iterable RFC8259 compliant JSON in your responses         
        I need you analysis some sentences and find out which skill it descripted, then give a score about this skill for the objective body it descripted. You should only choose skills in skill_list blow.
        skill_list: {}
        content: {}
        It would be an array about score object. The score object contain field: domain, for example java, the second field is score. 
        """
    response = model.generate_content(prompt.format(skill_list, content))
    # Preprocess the response text to extract JSON
    response_text = response.text.strip()

    logger.info(f"=== Get Score Result: {response_text}")

    # Use a regular expression to extract JSON array from response text
    json_match = re.search(r'(\[.*\])', response_text, re.DOTALL)
    logger.info(f"=== json_match: {json_match}")
    if json_match:
        json_text = json_match.group(1)
        try:
            response_json = json.loads(json_text)
            print(response_json)
            return response_json
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
    else:
        print("No JSON array found in response text")

    return {}
    
from . import routes
    

