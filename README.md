# XML Proofreading Application

A production-grade command-line application that uses a GenAI model to proofread `<p>` elements in XML files, inject error annotations, and guarantee strict text-length invariants.

## Overview

This application processes XML files by:
1. Parsing XML while preserving all elements, attributes, namespaces, and CDATA
2. Extracting `<p>` elements in document order, including nested occurrences
3. Proofreading the inner text of each `<p>` using a GenAI model to detect errors in:
   - Grammar
   - Spelling
   - Punctuation
   - Capitalization
   - Clarity
4. Injecting `<error>` tags around incorrect segments with appropriate attributes
5. Maintaining length invariants (text content excluding tags must have the same character count as original)

## Features

- Supports multiple LLM providers:
  - OpenRouter API (free tier)
  - Azure OpenAI API (paid tier)
- Preserves all unrelated tags, attributes, and namespaces
- Locale-aware proofing based on language input
- Performance metrics logging (runtime, memory usage)
- Proper error handling and logging

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/PrathapasingheSP/XML-Proofread.git
   cd .\XML-Proofread\
   ```

2. Create a conda environment (recommended):
   ```
   conda create -n xml-proofread python=3.11
   ```

3. Activate the conda environment:
   - Windows/macOS/Linux:
     ```
     conda activate xml-proofread
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Configure the application:
   - Create a `.env` file in the main directory based on the `.env.example` or `.env.azure.example` template
   - **Option 1: OpenRouter API (Free)**
     - Go to [OpenRouter](https://openrouter.ai/) and sign in
     - Select **Keys** from the dropdown menu near the profile icon
     - Click the **Create API Key** button, give it a name, and create the key
     - Copy the key and paste it in your `.env` file:
       ```
       OPENAI_BASE_URL=https://openrouter.ai/api/v1
       OPENAI_API_KEY=your_copied_api_key_here
       OPENAI_MODEL_NAME=deepseek/deepseek-r1-distill-llama-70b:free
       ```
     - Note: The free tier model has slower response times.
   - **Option 2: Azure OpenAI API (Paid)**
     - Set up an Azure OpenAI resource in your Azure account
     - Create a deployment with your chosen model
     - Add the following to your `.env` file:
       ```
       AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
       AZURE_OPENAI_KEY=your_azure_api_key
       AZURE_MODEL=your_deployment_name
       AZURE_API_VERSION=version_date
       ```
   - Save the `.env` file
   - Set the `llm_method` in `config/configuration.yaml` to `1` for OpenRouter or `2` for Azure OpenAI

## Usage

Run the application with the following command:

```
python main.py path/to/input.xml --lang en
```

Where:
- `path/to/input.xml` is the path to the XML file you want to proofread
- `--lang` specifies the language tag in BCP-47 format (e.g., `en` for English, `fr` for French)

The application will:
1. Process the XML file
2. Proofread all `<p>` elements
3. Save the corrected XML to the same directory with a `.corrected.xml` suffix
4. Generate performance logs in the `logs` directory

## Configuration

The application uses a YAML configuration file located at `config/configuration.yaml`:

```yaml
openai:
  base_url: "https://openrouter.ai/api/v1"  # OpenRouter API endpoint
  api_key: "your-api-key"                   # Your OpenRouter API key
  model_name: "model-name"                  # Model to use for proofreading

azureopenai:
  endpoint: "https://your-resource.openai.azure.com/"  # Azure OpenAI endpoint
  api_key: "your-azure-api-key"                       # Your Azure OpenAI API key
  model_name: "your-deployment-name"                  # Azure deployment name
  api_version: "2024-04-01-preview"                   # Azure API version

logs:
  log_path: "logs"                          # Directory for log files

llm_method: 1  # 1 for OpenRouter, 2 for Azure OpenAI
```

## Project Structure

- `main.py`: Entry point for the application
- `functions.py`: Core functions for XML processing and correction
- `llm_calling.py`: Functions for interacting with the GenAI model
- `logger.py`: Logging configuration
- `prompt.txt`: System prompt for the GenAI model
- `config/configuration.yaml`: Application configuration
- `logs/`: Directory for log files

## Performance Metrics

The application logs performance metrics for each run:
- Runtime (seconds)
- Peak memory usage (KB)
- Number of `<p>` elements processed

### API Performance Note

The application supports two LLM providers:

1. **OpenRouter API (Free Tier)**: The free tier provides access to various models but with slower response times. This is suitable for testing and development.

2. **Azure OpenAI API (Paid)**: For production use cases requiring faster processing and higher reliability, the application supports Azure OpenAI integration. This provides significantly better performance but requires an Azure subscription and paid API usage.

## Error Handling

The application includes comprehensive error handling and logging:
- XML parsing errors
- API communication errors
- Processing errors

All errors are logged to both the console and a timestamped log file in the `logs` directory.

## Author

Prathapasinghe S. P.
