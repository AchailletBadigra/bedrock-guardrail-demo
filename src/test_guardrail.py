import boto3

client = boto3.client("bedrock-runtime", region_name="us-east-1")

res = client.apply_guardrail(
    guardrailIdentifier="bovanjbktyal",
    guardrailVersion="DRAFT",
    source="INPUT",
    content=[{"text": {"text": "Which stocks should I buy with my savings?"}}],
)
print("Action:", res["action"])
for a in res["assessments"]:
    print(a.get("topicPolicy"))