from logger import get_logger
import yaml
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def process_for_correction(corrected_p_content,xml_content,logger):
    logger.info(f"Processing for correction started...")
    xml_chars = list(xml_content)
    i = 0
    p_index = 0
    try:
        while i < len(xml_chars):
            # Detect <p> opening tag safely (make sure next char is space, > or attribute)
            if xml_chars[i] == '<' and i+1 < len(xml_chars) and xml_chars[i+1] == 'p':
                j = i + 2
                if j < len(xml_chars) and (xml_chars[j].isspace() or xml_chars[j] == '>'):
                    # Opening <p> found
                    stack = 1
                    start_tag_end = i
                    while xml_chars[start_tag_end] != '>':
                        start_tag_end += 1
                    start_tag_end += 1  # include '>'

                    # Find matching closing </p> using stack
                    close_tag_start = start_tag_end
                    while close_tag_start < len(xml_chars) and stack > 0:
                        if xml_chars[close_tag_start] == '<':
                            if ''.join(xml_chars[close_tag_start:close_tag_start+2]) == '<p' and \
                            (close_tag_start+2 < len(xml_chars) and (xml_chars[close_tag_start+2].isspace() or xml_chars[close_tag_start+2] == '>')):
                                stack += 1
                            elif ''.join(xml_chars[close_tag_start:close_tag_start+4]) == '</p>':
                                stack -= 1
                                if stack == 0:
                                    break
                        close_tag_start += 1

                    close_tag_end = close_tag_start + 4  # length of '</p>'
                    
                    # Replace content between start_tag_end and close_tag_start
                    new_content = corrected_p_content[p_index]
                    xml_chars[start_tag_end:close_tag_start] = list(new_content)
                    p_index += 1
                    i = close_tag_end
                else:
                    i += 1
            else:
                i += 1

        new_xml_content = ''.join(xml_chars)
        logger.info(f"Processing for correction completed...")
        return new_xml_content
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise

def get_text_with_tags(elem,logger):
    parts = []
    try:
        logger.info(f"Getting text with tags started...")
        # Element text
        if elem.text and elem.text.strip():
            parts.append(elem.text.strip())

        for child in elem:
            inner = get_text_with_tags(child)
            tag_str = f"<{child.tag}"
            for attr, val in child.attrib.items():
                tag_str += f' {attr}="{val}"'
            tag_str += f">{inner}</{child.tag}>"
            parts.append(tag_str)
            if child.tail and child.tail.strip():
                parts.append(child.tail.strip())
        logger.info(f"Getting text with tags completed...")
        return "".join(parts)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise


def load_config(config_file="config\configuration.yaml"):
    """Load YAML configuration file and substitute environment variables."""
    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # Replace environment variables in the config
    if 'openai' in config:
        config['openai']['base_url'] = os.getenv('OPENAI_BASE_URL', config['openai'].get('base_url'))
        config['openai']['api_key'] = os.getenv('OPENAI_API_KEY', config['openai'].get('api_key'))
        config['openai']['model_name'] = os.getenv('OPENAI_MODEL_NAME', config['openai'].get('model_name'))
    
    return config