#!/bin/bash

# Define the root directory name
ROOT_DIR="."

# Create the main directory structure
echo "Creating directory structure for $ROOT_DIR..."
mkdir -p "$ROOT_DIR/data_ingestion"
mkdir -p "$ROOT_DIR/tools"
mkdir -p "$ROOT_DIR/agents"

# Create root level files
touch "$ROOT_DIR/config.py"
touch "$ROOT_DIR/state.py"
touch "$ROOT_DIR/app.py"
touch "$ROOT_DIR/pipeline.py"

# Create data_ingestion files
touch "$ROOT_DIR/data_ingestion/__init__.py"
touch "$ROOT_DIR/data_ingestion/file_processor.py"
touch "$ROOT_DIR/data_ingestion/text_splitter.py"

# Create tools files
touch "$ROOT_DIR/tools/__init__.py"
touch "$ROOT_DIR/tools/structured_tool.py"
touch "$ROOT_DIR/tools/vector_rag_tool.py"
touch "$ROOT_DIR/tools/summary_tool.py"
touch "$ROOT_DIR/tools/web_scraper_tool.py"

# Create agents files
touch "$ROOT_DIR/agents/supervisor.py"

echo "Project structure generated successfully!"
