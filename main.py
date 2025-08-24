import argparse
import xml.etree.ElementTree as ET
import os
import time
import tracemalloc
from logger import get_logger
from datetime import datetime
from functions import process_for_correction,get_text_with_tags,load_config
from llm_calling import chat_with_gpt


config = load_config()

logs_config = config.get("logs", {})
log_path = logs_config.get("log_path", "logs")

def main():

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_file_path = os.path.join(log_path, f"{timestamp}.log")

    # Get logger with file + console output
    logger = get_logger(log_file=log_file_path)
    logger.info(f"log file path: {log_file_path}")
    logger.info(f"Starting the application...")
    
    try:
        # Start tracking time + memory
        start_time = time.perf_counter()
        tracemalloc.start()

        parser = argparse.ArgumentParser(description="Process an XML file with a language tag.")
        parser.add_argument("xml_file", type=str, help="Path to the XML file")
        parser.add_argument("--lang", type=str, required=True, help="Language tag (BCP-47 format, e.g., en, fr)")

        args = parser.parse_args()

        xml_file_path = args.xml_file
        lang_tag = args.lang

        # Build output file path with .corrected.xml suffix
        base, _ = os.path.splitext(xml_file_path)
        output_file_path = f"{base}.corrected.xml"

        logger.info(f"Starting processing for file: {xml_file_path}")
        logger.info(f"Language tag: {lang_tag}")

        with open(xml_file_path, "r", encoding="utf-8") as file:
            xml_content = file.read().strip()  # .strip() removes leading/trailing whitespace or newlines

        tree = ET.ElementTree(ET.fromstring(xml_content))
        root = tree.getroot()

        # Build parent map to detect outermost <p>
        parent_map = {c: p for p in root.iter() for c in p}

        # All <p> elements
        all_p = list(root.iter("p"))
        logger.info(f"Total <p> elements: {len(all_p)}")

        # Keep only outermost <p> (no <p> ancestor)
        outermost_p = [p for p in all_p if parent_map.get(p) is None or parent_map[p].tag != "p"]
        logger.info(f"Outermost <p> elements: {len(outermost_p)}")


        output_groups = []
        for p in outermost_p:
            # Collect main <p> text with inline tags
            chunk = [get_text_with_tags(p,logger)]
            output_groups.append("|".join(chunk))

        # for i, group in enumerate(output_groups, 1):
        #     print(f"Group {i}: {group}\n")

        llm_response=chat_with_gpt(output_groups,'en',logger)
        logger.info(f"LLM response: {llm_response}")
        new_xml_content=process_for_correction(llm_response,xml_content,logger)
        # Save the XML content
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(new_xml_content)

        logger.info(f"Saved proofread XML to {output_file_path}")

        # Stop timers and memory tracking
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        runtime = end_time - start_time
        memory_usage_kb = peak / 1024

        # Log summary
        logger.info(f"\n--- Performance Summary ---")
        logger.info(f"File: {xml_file_path}")
        logger.info(f"Language tag: {lang_tag}")
        logger.info(f"Runtime: {runtime:.4f} seconds")
        logger.info(f"Peak memory: {memory_usage_kb:.2f} KB")
        logger.info(f"Number of outermost <p> elements: {len(outermost_p)}")
        logger.info(f"Corrected file saved to: {output_file_path}")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()