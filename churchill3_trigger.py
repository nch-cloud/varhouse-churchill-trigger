import boto3
import os
import json
from datetime import datetime
from aws_lambda_powertools import Logger, Tracer
from schema.churchillvcfevent import ChurchillVCFEvent
from schema.churchillvcfevent import AWSEvent

logger = Logger()
tracer = Tracer()

CANCER_PROJECTS = {"clinical-cancer"}
REQUIRES_PROBAND_PROJECTS = {"clinical-genome", "clinical-rapid-genome", "clinical-exome"}

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    aws_event: AWSEvent = AWSEvent.from_dict(event)
    detail: ChurchillVCFEvent = aws_event.detail

    if "control" in detail.case_name.lower():
        logger.warning(f"Skipping control sample: {detail.case_name}")
        return

    sample_data = get_sample_data(detail)
    if detail.project in REQUIRES_PROBAND_PROJECTS and not sample_data.get("proband"):
        logger.error("Skipping Varhouse, missing proband sample.")
        return

    execution_input = {
        "case_name": detail.case_name,
        "project": detail.project,
        "reference": "GRCh38" if detail.genome_ver == "38" else detail.genome_ver,
        "jar": "",
        **sample_data
    }

    job_name = generate_job_name(detail)
    start_step_function(execution_input, job_name)

def generate_job_name(detail: ChurchillVCFEvent) -> str:
    date_str = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    if detail.project in CANCER_PROJECTS:
        max_len = 80 - len(date_str) - len("-germ") - 1
        return f"{detail.case_name[:max_len]}-{date_str}"
    return f"{detail.case_name}-{date_str}"

def get_sample_data(detail: ChurchillVCFEvent) -> dict:
    if detail.project in CANCER_PROJECTS:
        return get_cancer_sample_data(detail)
    return get_non_cancer_sample_data(detail)

def get_non_cancer_sample_data(detail: ChurchillVCFEvent) -> dict:
    samples = { "proband": None, "mother": None, "father": None }

    for sample in detail.samples:
        relation = (sample.relation or "").lower()
        if relation in samples:
            samples[relation] = sample.name
        else:
            logger.warning(f"Unrecognized relation '{sample.relation}' for sample {sample.name}")

    return {
        **samples,
        "vcf": detail.merged_vcf
    }

def get_cancer_sample_data(detail: ChurchillVCFEvent) -> dict:
    germline_samples, somatic_samples = [], []

    for sample in detail.samples:
        match sample.type:
            case "normal":
                germline_samples.append(sample.name)
            case "tumor":
                somatic_samples.append(sample.name)
            case _:
                logger.warning(f"Unrecognized sample type '{sample.type}' for sample {sample.name}")

    return {
        "germline_analysis_name": f"{detail.case_name}_germline",
        "mutect2_somatic_analysis_name": f"{detail.case_name}_mutect2_somatic",
        "germline_vcf": detail.merged_vcf,
        "mutect2_somatic_vcf": detail.mutect2_somatic_vcf,
        "germline_samples": ",".join(germline_samples * len(somatic_samples)),
        "somatic_samples": ",".join(somatic_samples),
    }

def start_step_function(execution_input: dict, job_name: str) -> None:
    logger.info(f"Starting Varhouse Step Function for project '{execution_input.get('project')}' and case '{execution_input.get('case_name')}'")

    client = boto3.client("stepfunctions")
    response = client.start_execution(
        stateMachineArn=os.environ["STEP_FUNCTION"],
        name=job_name,
        input=json.dumps(execution_input, indent=4, sort_keys=True, default=str)
    )

    logger.info(response)
