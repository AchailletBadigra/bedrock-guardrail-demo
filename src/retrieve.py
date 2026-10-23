import boto3

KB_ID = "BKLLJ6TU87"  # paste your ID here
client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

def retrieve(question, top_k=3):
    response = client.retrieve(
        knowledgeBaseId=KB_ID,
        retrievalQuery={"text": question},       
        retrievalConfiguration={"managedSearchConfiguration": {"numberOfResults": top_k}},
    )
    for i, r in enumerate(response["retrievalResults"], 1):
        print(f"\n--- Result {i} | score: {r['score']:.3f}")
        print("Source:", r["location"]["s3Location"]["uri"])
        print(r["content"]["text"][:300], "...")

if __name__ == "__main__":
        retrieve("What are the three steps of RLHF in InstructGPT?")