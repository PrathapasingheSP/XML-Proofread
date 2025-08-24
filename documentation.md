# XML Proofreading Application Documentation

## Project Overview

The XML Proofreading Application is a production-grade command-line tool designed to proofread XML files by identifying and annotating errors in `<p>` elements. The application uses a GenAI model to detect various types of errors (grammar, spelling, punctuation, capitalization, clarity) and injects `<e>` tags around incorrect segments while maintaining strict text-length invariants.

## Architecture

### High-Level Architecture

The application follows a modular architecture with the following main components:

```
┌─────────────────┐     ┌───────────────┐     ┌─────────────────┐
│                 │     │               │     │                 │
│  XML Parsing    │────▶│  LLM Service  │────▶│  XML Generation │
│  & Processing   │     │               │     │  & Output       │
│                 │     │               │     │                 │
└─────────────────┘     └───────────────┘     └─────────────────┘
        │                      │                     │
        │                      │                     │
        ▼                      ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                     Logging & Configuration                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

1. **Entry Point (`main.py`)**
   - Handles command-line arguments
   - Orchestrates the overall workflow
   - Manages performance tracking (time, memory)
   - Implements error handling

2. **XML Processing (`functions.py`)**
   - Parses XML while preserving structure
   - Extracts `<p>` elements
   - Processes text with tags
   - Applies corrections to XML content

3. **LLM Integration (`llm_calling.py`)**
   - Manages communication with multiple LLM providers:
     - OpenRouter API (free tier)
     - Azure OpenAI API (paid tier)
   - Formats input for the LLM
   - Processes and parses LLM responses

4. **Logging System (`logger.py`)**
   - Configures console and file logging
   - Provides consistent logging format
   - Manages log file creation and storage

5. **Configuration Management**
   - Loads settings from YAML configuration
   - Integrates environment variables
   - Provides centralized configuration access

## Data Flow

1. **Input Processing**
   - XML file is read and parsed into an ElementTree
   - Outermost `<p>` elements are identified using a parent map
   - Text content with inline tags is extracted while preserving structure

2. **LLM Processing**
   - Extracted content is sent to the selected LLM provider (OpenRouter or Azure OpenAI) with a specialized prompt
   - LLM identifies errors and returns annotated content
   - Response is parsed and validated

3. **Output Generation**
   - Original XML is modified with error annotations
   - Corrected XML is saved with `.corrected.xml` suffix
   - Performance metrics are logged

## Technical Details

### Core Functions

1. **`main()` (in `main.py`)**
   - Entry point that orchestrates the entire process
   - Handles command-line arguments
   - Manages XML parsing and processing
   - Tracks performance metrics

2. **`process_for_correction()` (in `functions.py`)**
   - Replaces content between `<p>` tags with corrected content
   - Preserves XML structure and attributes
   - Uses a stack-based approach to handle nested tags

3. **`get_text_with_tags()` (in `functions.py`)**
   - Recursively extracts text with inline tags from XML elements
   - Preserves tag structure for LLM processing

4. **`load_config()` (in `functions.py`)**
   - Loads YAML configuration
   - Substitutes environment variables

5. **`chat_with_gpt()` (in `llm_calling.py`)**
   - Formats input for the LLM
   - Manages API communication
   - Parses and validates responses

6. **`get_logger()` (in `logger.py`)**
   - Configures logging to both console and file
   - Ensures consistent log formatting

### Configuration System

The application uses a layered configuration approach:
1. Default settings in `config/configuration.yaml`
2. Environment variables from `.env` file
3. Command-line arguments

Configuration parameters include:
- OpenAI API settings (base URL, API key, model name)
- Azure OpenAI API settings (endpoint, API key, model name, API version)
- LLM provider selection (OpenRouter or Azure OpenAI)
- Logging settings (log directory)

### Error Handling

The application implements comprehensive error handling:
- XML parsing errors
- API communication errors
- Processing errors
- File I/O errors

All errors are logged with appropriate context and stack traces.

## Performance Considerations

The application tracks and logs key performance metrics:
- Runtime (seconds)
- Peak memory usage (KB)
- Number of `<p>` elements processed

Memory usage is optimized by:
- Processing XML elements sequentially
- Using efficient string operations
- Avoiding unnecessary data duplication

### API Performance Note

The application supports two LLM providers with different performance characteristics:

1. **OpenRouter API (Free Tier)**
   - Provides access to various models but with slower response times
   - Suitable for testing and development purposes
   - Limited by rate restrictions of the free tier
   - Processing time: ~22 seconds for a sample French XML file

2. **Azure OpenAI API (Paid)**
   - Offers significantly better performance and reliability
   - Provides lower latency and higher throughput
   - Requires an Azure subscription and paid API usage
   - Recommended for production deployments and larger XML files
   - Processing time: ~7 seconds for the same sample French XML file (3x faster)

#### Performance Comparison

Based on actual testing with the same French XML file:

| LLM Provider | Processing Time | Relative Speed |
|--------------|-----------------|----------------|
| OpenRouter   | 22 seconds      | 1x (baseline)  |
| Azure OpenAI | 7 seconds       | 3.1x faster    |

This significant performance difference makes Azure OpenAI the recommended choice for production environments where processing speed is important.

## Prompt Engineering

The system uses a carefully crafted prompt (`prompt.txt`) that instructs the LLM to:
1. Detect specific types of errors (grammar, spelling, punctuation, capitalization, clarity)
2. Wrap errors with `<e>` tags and appropriate attributes
3. Maintain strict text-length invariants
4. Preserve all XML structure, attributes, and whitespace

The prompt includes validation rules to ensure the LLM output meets requirements.

## XML Processing Logic

### Parsing Strategy
The application uses Python's `xml.etree.ElementTree` to parse XML files while preserving structure. The parsing process:

1. Reads the XML file with UTF-8 encoding
2. Constructs an ElementTree from the content
3. Creates a parent map to identify outermost `<p>` elements
4. Extracts text content with inline tags

### Error Annotation
The error annotation process:

1. LLM identifies errors in the text
2. Errors are wrapped with `<e>` tags including:
   - `type` attribute (grammar, spelling, punctuation, capitalization, clarity)
   - `correction` attribute with the suggested correction
3. Original XML structure is preserved

### Length Invariance
The application ensures that the visible text content (excluding tags) remains unchanged in length after processing. This is critical for maintaining document integrity.

## Deployment and Usage

### Prerequisites
- Python 3.8+
- Dependencies from `requirements.txt`:
  - openai
  - lxml
  - pyyaml>=6.0
  - python-dotenv

### Installation
1. Clone the repository
2. Create and activate a Python environment
3. Install dependencies
4. Configure API access through `.env` file (OpenRouter) or `.env.azure` file (Azure OpenAI)

### Execution
```
python main.py path/to/input.xml --lang en
```

Where:
- `path/to/input.xml` is the path to the XML file to proofread
- `--lang` specifies the language tag in BCP-47 format (e.g., `en` for English, `fr` for French)

## Project Structure

```
XML-Proofread/
├── XML_Files/               # Sample XML files for testing
├── config/
│   └── configuration.yaml   # Configuration settings
├── logs/                    # Log output directory
├── .env.example             # Template for OpenRouter environment variables
├── .gitignore               # Git ignore file
├── Prompt.txt               # System prompt for the LLM
├── README.md                # Project README
├── functions.py             # Core XML processing functions
├── llm_calling.py           # LLM API integration
├── logger.py                # Logging configuration
├── main.py                  # Main application entry point
└── requirements.txt         # Project dependencies
```

## Future Enhancements

Potential areas for improvement:
1. Parallel processing for large XML files
2. Support for additional XML element types
3. Batch processing of multiple files
4. Web interface or API endpoint
5. Optimizing Azure OpenAI integration for enterprise deployments
6. Custom error type definitions

## Conclusion

The XML Proofreading Application provides a robust solution for automated proofreading of XML content. Its architecture ensures accurate error detection while maintaining document structure and length invariants. The modular design allows for easy maintenance and future enhancements.
