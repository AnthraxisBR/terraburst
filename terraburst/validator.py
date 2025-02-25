import json
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)

LEVEL_LOW = "Low"
LEVEL_MID = "Mid"
LEVEL_HIGH = "High"
LEVEL_CRITICAL = "Critical"


def load_validation_rules(file_path: str):
    with open(file_path, "r") as file:
        return json.load(file)


VALIDATION_RULES = load_validation_rules("validation_rules.json")


def classify_change(change: Dict) -> str:
    change_type = change.get("change", {}).get("actions", [])
    resource_type = change.get("type", "")
    if resource_type in VALIDATION_RULES:
        for action in change_type:
            if action in VALIDATION_RULES[resource_type]:
                return VALIDATION_RULES[resource_type][action]

    logging.warning(f"No specific validation rules found for {resource_type} with actions {change_type}")
    return LEVEL_LOW


def validate_plan(plan_json: str) -> Dict[str, int]:
    try:
        with open(plan_json, "r") as file:
            plan = json.load(file)

        resource_changes = plan.get("resource_changes", [])
        validation_results = {LEVEL_LOW: 0, LEVEL_MID: 0, LEVEL_HIGH: 0, LEVEL_CRITICAL: 0}

        for change in resource_changes:
            change_detail = change.get("change", {})
            before = change_detail.get("before", {})
            after = change_detail.get("after", {})

            if before != after or "replace" in change.get("change", {}).get("actions", []):
                level = classify_change(change)
                validation_results[level] += 1

        logging.info(f"Terraform Plan Validation Summary: {validation_results}")
        return validation_results

    except Exception as e:
        logging.error(f"Error validating Terraform plan: {str(e)}")
        return {LEVEL_LOW: 0, LEVEL_MID: 0, LEVEL_HIGH: 0, LEVEL_CRITICAL: 0}
