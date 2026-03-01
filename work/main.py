"""
Pipeline: image + body params → GPT-4o → design.yaml
"""

import argparse
import os

from agent import Agent
from utils import (
    load_yaml,
    save_yaml,
    extract_yaml_from_response,
    compact_to_design,
)
from utils.io import load_prompt, build_user_prompt, DEFAULT_TEMPLATE
import shutil


def main():
    parser = argparse.ArgumentParser(
        description="Generate design.yaml from garment image + body measurements"
    )
    parser.add_argument("--img", required=True, help="Garment image path")
    parser.add_argument("--body", required=True, help="Body param YAML path")
    parser.add_argument("--output", default="./output", help="Output directory")
    parser.add_argument(
        "--template",
        default=str(DEFAULT_TEMPLATE),
        help="Design template YAML with range/type metadata",
    )
    args = parser.parse_args()

    # Load inputs
    body = load_yaml(args.body)
    system_prompt = load_prompt()
    user_text = build_user_prompt(body)

    # Call LLM
    agent = Agent()
    response = agent.call(system_prompt, user_text, image_path=args.img)
    print("=== GPT Response ===")
    print(response)
    print("====================")

    # Parse GPT output (compact format) → full design param
    compact = extract_yaml_from_response(response)
    design = compact_to_design(compact, template_path=args.template)

    # Save
    os.makedirs(args.output, exist_ok=True)
    out_path = os.path.join(args.output, "design.yaml")

    save_yaml(design, out_path)
    print(f"\nDesign saved to {out_path}")


if __name__ == "__main__":
    main()
