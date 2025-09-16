import requests
import json

def execute(data):
    prompt = data['prompt']
    language = data['language']
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtb2RlbElkIjoyMCwidXNlcklkIjo5LCJpYXR9OjE3NDI5OTgxMzF9.gMROStdwnnJjhUHWDFjQJ_lCX7ehObaeNqYVIbMpxLg'

    slug = 'mdl-gpt-4o-mini-ilvjr38x'
    h = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    data = {
        "input": {
            "prompt": f"Translate and enhance the following prompt into {language} to make it more detailed, clear, and effective. Return only the final version in {language} with no additional text, explanations, or formatting: [{prompt}]"
        }
    }
    # Use json=data instead of data=data
    r = requests.post(f'https://api.mlgrid.com/v1/model/{slug}/exec', headers=h, json=data)

    result = r.json()['output']['result']

    return {
        "result": result
    }