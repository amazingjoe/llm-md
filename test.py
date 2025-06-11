"""
LLM-MD Parser Test Suite

This module demonstrates the functionality of the LLM-MD parser with comprehensive examples.
"""

import importlib
import sys
from typing import Dict, Any

# Import the parser module
try:
    llm_md_parser = importlib.import_module('llm-md-parser')
except ImportError as e:
    print(f"Error importing llm-md-parser: {e}")
    sys.exit(1)


def print_section_header(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print(f"{'=' * 60}")


def print_subsection(title: str) -> None:
    """Print a formatted subsection header."""
    print(f"\n{'-' * 40}")
    print(f"{title}")
    print(f"{'-' * 40}")


def test_template_parsing() -> None:
    """Test the template parsing functionality with a comprehensive book planning template."""
    
    print_section_header("TEMPLATE PARSING DEMONSTRATION")
    
    template = """
- Basic Information

### Title [1] $ | Generate an engaging and marketable book title

### Premise [1] $ | Write a compelling 2-3 sentence premise that captures the book's main concept

### Genre [1] $ | Primary genre classification

- Characters

# Characters [1] | Character section container
## Character [*] | Create compelling characters with depth and complexity
### Name [1] $ | Character name that fits the story's setting and tone
### Age [1] | Character's age in years
### Zodiac Sign [1] | Assign a zodiac sign that complements personality
### Emotional Wound [1] | Describe past trauma that shapes behavior
### Primary Goal [1] $ | What the character wants most in the story

- Structure

# Outline [1] | Chapter outline container
## Chapter [*] | Detailed chapter information
### Title [1] $ | Engaging chapter title that reflects the content
### Target Wordcount [1] | Intended word count for this chapter
### Summary [1] $ | Comprehensive summary of chapter events and themes
### Key Scenes [2-4] | Important scenes within the chapter

- Style

### Writing Style [1] | Describe the intended tone, voice, and style
### Point of View [1] | Narrative perspective (first person, third person, etc.)
### Target Audience [1] | Intended readership demographic

"""
    
    print("Template Structure:")
    print(template.strip())
    
    print_subsection("Generated Worksheet (3 Characters, 5 Chapters)")
    
    # Generate worksheet with specific quantities
    quantities = {
        "Characters.Character": 3,
        "Outline.Chapter": 5,
        "Outline.Chapter.Key Scenes": 3
    }
    
    result = llm_md_parser.parse_llm_md(template, quantities=quantities)
    print(result)


def test_section_specific_generation() -> None:
    """Test generating only specific sections from the template."""
    
    print_section_header("SECTION-SPECIFIC GENERATION")
    
    template = """
- Basic Information

### Title [1] $ | Generate an engaging and marketable book title
### Premise [1] $ | Write a compelling 2-3 sentence premise

- Characters

# Characters [1] | Character section container
## Character [*] | Create compelling characters
### Name [1] $ | Character name
### Role [1] | Character's role in the story
### Motivation [1] | What drives this character

- Plot

# Story Arc [1] | Main plot structure
## Act [3] | Three-act structure
### Description [1] $ | Act summary
### Key Events [2-3] | Major plot points
"""
    
    print_subsection("Characters Section Only")
    characters_only = llm_md_parser.parse_llm_md(
        template, 
        section="Characters", 
        quantities={"Characters.Character": 2}
    )
    print(characters_only)


def test_worksheet_parsing() -> None:
    """Test parsing completed worksheet content."""
    
    print_section_header("WORKSHEET CONTENT PARSING")
    
    # Realistic completed worksheet example
    completed_worksheet = """
# Basic Information
---
### Title | The Clockmaker's Daughter
### Premise | When master clockmaker Elena discovers her father's final creation can manipulate time itself, she must protect it from a secret society while uncovering the truth about her family's mysterious past. Racing against time in both literal and figurative senses, she learns that some secrets are worth any sacrifice.
### Genre | Fantasy Thriller

# Characters
---
# Characters

## Character
### Name | Elena Vasquez
### Age | 28
### Zodiac Sign | Virgo
### Emotional Wound | Abandoned by her mother at age 12, leading to trust issues and fear of abandonment
### Primary Goal | To understand her father's legacy and protect his final invention

## Character
### Name | Marcus Chen
### Age | 35
### Zodiac Sign | Scorpio
### Emotional Wound | Lost his partner in a failed heist, carries guilt and seeks redemption
### Primary Goal | To steal the time device for the Chronos Society to pay off his debts

## Character
### Name | Dr. Amelia Blackwood
### Age | 52
### Zodiac Sign | Capricorn
### Emotional Wound | Her research was stolen and used for military purposes, now seeks to control dangerous technology
### Primary Goal | To acquire the time device to prevent its misuse

# Structure
---
# Outline

## Chapter 1
### Title | The Inheritance
### Target Wordcount | 3500
### Summary | Elena inherits her father's clockmaker shop and discovers his hidden workshop containing the mysterious temporal device. Strange visitors begin appearing, hinting at the device's true significance.
### Key Scenes | Elena discovers the hidden workshop, First glimpse of the time device, Marcus watches from across the street

## Chapter 2
### Title | Unwelcome Visitors
### Target Wordcount | 4000
### Summary | The Chronos Society sends representatives to negotiate for the device. Elena refuses and begins to understand the danger she's in. She seeks help from her father's old journals.
### Key Scenes | Tense negotiation scene, Elena finds her father's encrypted journal, First attempt to break into the shop

## Chapter 3
### Title | Time's Echo
### Target Wordcount | 4200
### Summary | Elena accidentally activates the device, experiencing brief time loops. She realizes the true power of her inheritance while Marcus infiltrates her life as a potential ally.
### Key Scenes | Accidental time loop activation, Elena relives the same hour twice, Marcus's true identity revealed

# Style
---
### Writing Style | Fast-paced thriller with steampunk elements, balancing technical clockwork descriptions with emotional character development
### Point of View | Third person limited, primarily from Elena's perspective with occasional shifts to Marcus
### Target Audience | Adult readers who enjoy fantasy thrillers, steampunk enthusiasts, and fans of time-travel narratives
"""
    
    print("Completed Worksheet Example:")
    print(completed_worksheet.strip())
    
    print_subsection("Parsed Section Analysis")
    
    # Parse the completed worksheet
    sections = llm_md_parser.parse_worksheet_content(completed_worksheet)
    
    print(f"Available sections: {list(sections.keys())}")
    
    # Demonstrate section content extraction
    print_subsection("Basic Information Fields")
    basic_info = sections.get("Basic Information", {})
    if basic_info:
        fields = basic_info.get("fields", {})
        for field_name, field_content in fields.items():
            print(f"{field_name}: {field_content}")
    
    print_subsection("Character Analysis")
    characters_section = sections.get("Characters", {})
    if characters_section:
        content = characters_section.get("content", "")
        # Count characters by parsing the content
        character_count = content.count("## Character")
        print(f"Number of characters defined: {character_count}")
        
        # Extract character names using the parser
        fields = characters_section.get("fields", {})
        names = [value for key, value in fields.items() if "Name" in key]
        if names:
            print(f"Character names: {', '.join(names)}")
    
    print_subsection("Structure Overview")
    structure_section = sections.get("Structure", {})
    if structure_section:
        content = structure_section.get("content", "")
        chapter_count = content.count("## Chapter")
        print(f"Number of chapters planned: {chapter_count}")
        
        # Calculate total target word count
        fields = structure_section.get("fields", {})
        wordcounts = [value for key, value in fields.items() if "Target Wordcount" in key and value.isdigit()]
        if wordcounts:
            total_words = sum(int(wc) for wc in wordcounts)
            print(f"Total target word count: {total_words:,} words")


def test_error_handling() -> None:
    """Test error handling and edge cases."""
    
    print_section_header("ERROR HANDLING TESTS")
    
    print_subsection("Invalid Section Request")
    try:
        template = "### Title [1] | A simple template"
        result = llm_md_parser.parse_llm_md(template, section="NonexistentSection")
        print("Unexpected success - should have raised an error")
    except ValueError as e:
        print(f"✓ Correctly handled invalid section: {e}")
    
    print_subsection("Empty Template Handling")
    try:
        empty_result = llm_md_parser.parse_llm_md("")
        print(f"Empty template result: '{empty_result}'")
        print("✓ Empty template handled gracefully")
    except Exception as e:
        print(f"✗ Error with empty template: {e}")


def main() -> None:
    """Run all test demonstrations."""
    
    print("LLM-MD Parser Comprehensive Test Suite")
    print("=" * 60)
    print("This test suite demonstrates the full functionality of the LLM-MD parser")
    print("with realistic book planning examples and comprehensive data.")
    
    try:
        test_template_parsing()
        test_section_specific_generation()
        test_worksheet_parsing()
        test_error_handling()
        
        print_section_header("TEST SUITE COMPLETED SUCCESSFULLY")
        print("All functionality demonstrated with realistic examples.")
        
    except Exception as e:
        print(f"\n✗ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()


