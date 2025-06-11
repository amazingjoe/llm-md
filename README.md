# LLM-MD Parser

A Python library for parsing structured markdown templates into dynamic worksheets, designed for content creation workflows with LLMs (Large Language Models).

## Overview

LLM-MD Parser transforms template files with special markdown syntax into structured worksheets that can be filled out and parsed back into structured data. It's particularly useful for content planning, creative writing, project management, and any scenario where you need to generate structured forms from templates.

## Features

- **Template-to-Worksheet Generation**: Convert structured templates into fillable worksheets
- **Dynamic Cardinality**: Control how many instances of each section are generated
- **Section-Specific Generation**: Generate only specific parts of a template
- **Worksheet Parsing**: Extract structured data from completed worksheets
- **Hierarchical Structure Support**: Handle nested sections and fields
- **Flexible Field Types**: Support for required fields, optional fields, and range-based quantities

## Quick Start

### Basic Usage

```python
import importlib
llm_md_parser = importlib.import_module('llm-md-parser')

# Define a template
template = """
- Basic Information

### Title [1] $ | Project title
### Description [1] | Project description

- Tasks

# Task List [1] | Container for tasks
## Task [*] | Individual task items
### Name [1] $ | Task name
### Priority [1] | Task priority level
### Status [1] | Current status
"""

# Generate a worksheet with 3 tasks
result = llm_md_parser.parse_llm_md(
    template, 
    quantities={"Task List.Task": 3}
)
print(result)
```

### Advanced Example

See `test.py` for a comprehensive book planning example with characters, chapters, and detailed content structure.

## Template Syntax

### Worksheet Sections
Define major sections with a dash prefix:
```markdown
- Section Name
```

### Headers and Fields
Use standard markdown headers with special syntax:
```markdown
### Field Name [cardinality] $ | notes
```

- **Field Name**: The display name for the field
- **[cardinality]**: Controls how many instances are generated
- **$**: Marks the field as required
- **| notes**: Optional description or instructions

### Cardinality Options

| Syntax | Description | Default Behavior |
|--------|-------------|------------------|
| `[1]` | Exactly one instance | Single field |
| `[*]` | Unlimited instances | 2 instances |
| `[3-5]` | Range of instances | Minimum value (3) |
| `[3]` | Fixed number | Exactly 3 instances |

### Example Template Structure

```markdown
- Project Planning

### Project Name [1] $ | Enter a descriptive project name

# Team [1] | Team member information
## Member [*] | Individual team members
### Name [1] $ | Full name
### Role [1] | Job title or role
### Skills [2-4] | Key skills or expertise areas

- Timeline

# Phases [1] | Project phases
## Phase [3] | Three main phases
### Name [1] $ | Phase name
### Duration [1] | Time estimate
### Deliverables [2-5] | Expected outputs
```

## API Reference

### Core Functions

#### `parse_llm_md(template, section=None, quantities=None)`
Generate a worksheet from a template.

**Parameters:**
- `template` (str): The LLM-MD template string
- `section` (str, optional): Generate only this section
- `quantities` (dict, optional): Override default quantities for fields

**Returns:** Generated worksheet as markdown string

**Example:**
```python
result = llm_md_parser.parse_llm_md(
    template,
    section="Characters",
    quantities={"Characters.Character": 5}
)
```

#### `parse_worksheet_content(worksheet_content, section_name=None)`
Parse completed worksheet content into structured data.

**Parameters:**
- `worksheet_content` (str): Completed worksheet markdown
- `section_name` (str, optional): Extract only this section

**Returns:** Dictionary with section data and field values

#### `get_section_content(worksheet_content, section_name)`
Extract the full content of a specific section.

**Returns:** Section content as string

#### `get_section_fields(worksheet_content, section_name)`
Extract field values from a specific section.

**Returns:** Dictionary mapping field names to values

## Use Cases

### Creative Writing
- **Book Planning**: Characters, plot outlines, chapter summaries
- **Screenplay Development**: Scene breakdowns, character arcs
- **World Building**: Locations, cultures, histories

### Project Management
- **Project Planning**: Tasks, milestones, team assignments
- **Requirements Gathering**: Features, specifications, acceptance criteria
- **Meeting Planning**: Agendas, action items, participants

### Content Creation
- **Course Development**: Modules, lessons, assessments
- **Marketing Campaigns**: Channels, messaging, timelines
- **Product Planning**: Features, user stories, roadmaps

## Installation

Currently, the parser is a single Python file. Simply download `llm-md-parser.py` and import it into your project:

```python
import importlib
llm_md_parser = importlib.import_module('llm-md-parser')
```

### Requirements
- Python 3.6+
- No external dependencies (uses only standard library)

## Testing

Run the comprehensive test suite:

```bash
python3 test.py
```

The test suite includes:
- Template parsing demonstrations
- Section-specific generation examples
- Worksheet content parsing
- Error handling verification
- Realistic book planning scenario

## Examples

### Simple Task List

**Template:**
```markdown
- Tasks
## Task [*] | Task items
### Description [1] $ | What needs to be done
### Priority [1] | High, Medium, or Low
```

**Generated Worksheet:**
```markdown
# Tasks
---
## Task
### Description | 
### Priority | 
## Task
### Description | 
### Priority | 
```

### Character Development

**Template:**
```markdown
- Characters
# Character Profiles [1]
## Character [*] | Main characters
### Name [1] $ | Character name
### Age [1] | Character age
### Background [1] | Character history
### Goals [2-3] | Character motivations
```

**Usage:**
```python
characters = llm_md_parser.parse_llm_md(
    template,
    section="Characters",
    quantities={"Character Profiles.Character": 4}
)
```

## Contributing

This is a single-file Python library focused on simplicity and functionality. Contributions are welcome for:

- Bug fixes and improvements
- Additional template syntax features
- Performance optimizations
- Documentation enhancements

## License

This project is available under the MIT License. See the full license text below:

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Support

For questions, issues, or feature requests, please create an issue in the project repository.