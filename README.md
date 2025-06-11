# LLM-MD Parser

<img src="https://futurefictionpress.com/wp-content/uploads/2024/07/FFP-Logo-Horizontal-2048x299.jpg" alt="Future Fiction Press" width="400">

A powerful Python parser for LLM-MD (Large Language Model Markdown) templates that generates structured worksheets and extracts content from completed worksheets.

## Features

- **Template Parsing**: Convert LLM-MD templates into structured worksheets
- **Section Generation**: Generate specific sections or complete worksheets
- **Content Extraction**: Parse completed worksheets and extract sections/fields
- **Flexible Cardinality**: Support for fixed counts, ranges, and unlimited arrays
- **Hierarchical Structure**: Handle nested content with proper markdown formatting

## Installation

Simply download `llm-md-parser.py` and import it into your Python project:

```python
from llm_md_parser import parse_llm_md, parse_worksheet_content, get_section_content
```

## Template Format

LLM-MD templates use a specific syntax:

### Section Separators
```
- Section Name
```
Creates worksheet sections with H1 headers and horizontal rules.

### Headers
```
# Title [cardinality] $ | notes
## Subtitle [cardinality] | notes
### Field [cardinality] $ | notes
```

- **cardinality**: `[1]` (fixed), `[*]` (unlimited), `[2-5]` (range)
- **$**: Marks required fields
- **|**: Separates field name from notes/instructions

## Usage Examples

### Basic Template Generation

```python
from llm_md_parser import parse_llm_md

template = """- Basic Information

# Title [1] $ | Generate an engaging book title
# Premise [1] $ | Write a compelling premise

- Characters

# Characters [1] | Character section container
## Character [*] | Create compelling characters
### Name [1] $ | Character name
### Age [1] | Character age
### Background [1] | Character background story"""

# Generate complete worksheet
worksheet = parse_llm_md(template, quantities={"Characters.Character": 3})
print(worksheet)
```

**Output:**
```markdown
# Basic Information
---
## Title | 

## Premise | 

# Characters
---
## Characters
### Character
#### Name | 

#### Age | 

#### Background | 

### Character
#### Name | 

#### Age | 

#### Background | 

### Character
#### Name | 

#### Age | 

#### Background | 
```

### Section-Specific Generation

```python
# Generate only the Characters section
characters_section = parse_llm_md(template, section="Characters", quantities={"Characters.Character": 2})
print(characters_section)
```

### Parsing Completed Worksheets

```python
from llm_md_parser import parse_worksheet_content, get_section_content, get_section_fields

# Assume you have a completed worksheet
completed_worksheet = """# Basic Information
---
## Title | 
The Great Adventure

## Premise | 
A young hero discovers a magical world hidden beneath their hometown.

# Characters
---
## Characters
### Character
#### Name | 
Alex Thompson

#### Age | 
16

#### Background | 
A curious teenager who loves exploring abandoned places."""

# Parse all sections
sections = parse_worksheet_content(completed_worksheet)
print("Available sections:", list(sections.keys()))

# Get specific section content
basic_info = get_section_content(completed_worksheet, "Basic Information")
print("Basic Information section:")
print(basic_info)

# Get individual fields from a section
basic_fields = get_section_fields(completed_worksheet, "Basic Information")
print("Title:", basic_fields.get("Title", ""))
print("Premise:", basic_fields.get("Premise", ""))
```

### Advanced Template with Ranges

```python
template = """- Story Structure

# Outline [1] | Chapter outline container
## Chapter [3-8] | Detailed chapter information
### Title [1] $ | Chapter title
### Summary [1] $ | Chapter summary
### Word Count [1] | Target word count

- Character Development

# Protagonist [1] $ | Main character details
## Traits [*] | Character traits
### Trait [1] $ | Individual trait description"""

# Generate with specific quantities
result = parse_llm_md(template, quantities={
    "Outline.Chapter": 5,
    "Protagonist.Traits.Trait": 4
})
```

## API Reference

### Core Functions

#### `parse_llm_md(template, section=None, quantities=None)`
Generate worksheet from LLM-MD template.

**Parameters:**
- `template` (str): LLM-MD template string
- `section` (str, optional): Generate only specified section
- `quantities` (dict, optional): Override cardinality for specific paths

**Returns:** Generated worksheet as markdown string

#### `parse_worksheet_content(worksheet_content, section_name=None)`
Parse completed worksheet and extract structured data.

**Parameters:**
- `worksheet_content` (str): Completed worksheet markdown
- `section_name` (str, optional): Extract only specified section

**Returns:** Dictionary with section data

#### `get_section_content(worksheet_content, section_name)`
Extract full content of a specific section.

**Parameters:**
- `worksheet_content` (str): Completed worksheet markdown
- `section_name` (str): Name of section to extract

**Returns:** Section content as string

#### `get_section_fields(worksheet_content, section_name)`
Extract individual fields from a section.

**Parameters:**
- `worksheet_content` (str): Completed worksheet markdown
- `section_name` (str): Name of section to extract

**Returns:** Dictionary mapping field names to content

## Cardinality Examples

```python
# Fixed count
"# Chapter [3]"  # Exactly 3 chapters

# Range
"# Character [2-5]"  # Between 2 and 5 characters

# Unlimited (with default)
"# Scene [*]"  # Unlimited scenes (defaults to 2)

# Override with quantities
quantities = {"Story.Chapter": 8, "Characters.Character": 4}
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## License

This project is presented by Future Fiction Press.

---

© 2024 Future Fiction Press. All rights reserved.