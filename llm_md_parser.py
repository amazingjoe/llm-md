import re
from typing import Dict, List, Optional, Any

def parse_llm_md(template: str, section: Optional[str] = None, quantities: Optional[Dict[str, int]] = None) -> str:
    """
    Parse LLM-MD template and generate worksheet output.
    
    Args:
        template: LLM-MD template string
        section: Optional worksheet section name to generate only that section
        quantities: Optional dict mapping array field paths to desired quantities
                   e.g., {"Characters.Character": 3, "Outline.Chapter": 8}
    
    Returns:
        Generated worksheet as markdown string
    """
    if quantities is None:
        quantities = {}
    
    lines = template.strip().split('\n')
    parsed_structure = _parse_template_structure(lines)
    
    if section:
        # Find and generate only the specified section
        section_structure = _find_section_structure(parsed_structure, section)
        if not section_structure:
            raise ValueError(f"Section '{section}' not found in template")
        return _generate_worksheet(section_structure, quantities)
    else:
        # Generate complete worksheet (excluding worksheet separators)
        content_structure = _filter_content_structure(parsed_structure)
        return _generate_worksheet(content_structure, quantities)

def _parse_template_structure(lines: List[str]) -> List[Dict[str, Any]]:
    """Parse template lines into structured data."""
    structure = []
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('- '):
            # Worksheet section separator
            section_name = line[2:].strip()
            current_section = {
                'type': 'worksheet_section',
                'name': section_name,
                'content': []
            }
            structure.append(current_section)
        elif line.startswith('#'):
            # Header line
            parsed_header = _parse_header_line(line)
            
            if current_section and current_section['type'] == 'worksheet_section':
                current_section['content'].append(parsed_header)
            else:
                # No worksheet section, add directly to structure
                structure.append(parsed_header)
    
    return structure

def _parse_header_line(line: str) -> Dict[str, Any]:
    """Parse a single header line into structured data."""
    # Count header level
    level = 0
    for char in line:
        if char == '#':
            level += 1
        else:
            break
    
    # Remove header markers
    content = line[level:].strip()
    
    # Extract components using regex
    # Pattern: Title [cardinality] $ | notes
    pattern = r'^([^|\[\$]+?)(?:\s*(\[[^\]]*\]))?(?:\s*(\$))?(?:\s*\|\s*(.*))?$'
    match = re.match(pattern, content)
    
    if not match:
        raise ValueError(f"Invalid header format: {line}")
    
    name = match.group(1).strip()
    cardinality_str = match.group(2) or '[1]'
    required = match.group(3) is not None
    notes = match.group(4) or ''
    
    # Parse cardinality
    cardinality = _parse_cardinality(cardinality_str)
    
    return {
        'type': 'header',
        'level': level,
        'name': name,
        'cardinality': cardinality,
        'required': required,
        'notes': notes,
        'children': []
    }

def _parse_cardinality(cardinality_str: str) -> Dict[str, Any]:
    """Parse cardinality notation like [1], [*], [3-5]."""
    cardinality_str = cardinality_str.strip('[]')
    
    if cardinality_str == '*':
        return {'type': 'unlimited', 'min': 0, 'max': None}
    elif cardinality_str.isdigit():
        count = int(cardinality_str)
        return {'type': 'fixed', 'count': count}
    elif '-' in cardinality_str:
        min_val, max_val = cardinality_str.split('-')
        return {'type': 'range', 'min': int(min_val), 'max': int(max_val)}
    else:
        raise ValueError(f"Invalid cardinality format: {cardinality_str}")

def _find_section_structure(structure: List[Dict[str, Any]], section_name: str) -> Optional[List[Dict[str, Any]]]:
    """Find content for a specific worksheet section."""
    for item in structure:
        if item.get('type') == 'worksheet_section' and item.get('name') == section_name:
            return item['content']
    return None

def _filter_content_structure(structure: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return structure as-is since we now want to include worksheet sections as H1 headers."""
    return structure

def _generate_worksheet(structure: List[Dict[str, Any]], quantities: Dict[str, int]) -> str:
    """Generate worksheet markdown from parsed structure."""
    result = []
    
    # Process structure including worksheet sections
    for item in structure:
        if item.get('type') == 'worksheet_section':
            # Add line break above, H1, then horizontal rule below
            if result:  # Only add line break above if there's already content
                result.append('')
            result.append(f"# {item['name']}")
            result.append('---')
            
            # Build hierarchical structure for section content
            hierarchy = _build_hierarchy(item['content'])
            
            # Generate output for section content
            for content_item in hierarchy:
                _generate_item_output(content_item, result, quantities, [])
        elif item.get('type') == 'header':
            # Direct header (not in a worksheet section)
            _generate_item_output(item, result, quantities, [])
    
    return '\n'.join(result)

def _build_hierarchy(structure: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Build hierarchical structure from flat list."""
    root_items = []
    stack = []
    
    for item in structure:
        level = item['level']
        
        # Pop stack until we find the right parent level
        while stack and stack[-1]['level'] >= level:
            stack.pop()
        
        if stack:
            # Add as child to parent
            stack[-1]['children'].append(item)
        else:
            # Root level item
            root_items.append(item)
        
        stack.append(item)
    
    return root_items

def _generate_item_output(item: Dict[str, Any], result: List[str], quantities: Dict[str, int], path: List[str]) -> None:
    """Generate output for a single item and its children."""
    current_path = path + [item['name']]
    path_key = '.'.join(current_path)
    
    # Determine how many instances to generate
    if item['cardinality']['type'] == 'unlimited':
        count = quantities.get(path_key, 2)  # Default to 2 for unlimited
    elif item['cardinality']['type'] == 'range':
        count = quantities.get(path_key, item['cardinality']['min'])
    else:
        count = item['cardinality']['count']
    
    # Generate instances
    if count == 1 and not item['children']:
        # Single field
        header = '#' * item['level'] + ' ' + item['name'] + ' | '
        result.append(header)
        if item['level'] == 1:
            result.append('')  # Extra line after top-level
    elif count == 1 and item['children']:
        # Single container
        header = '#' * item['level'] + ' ' + item['name']
        result.append(header)
        if item['level'] == 1:
            result.append('')  # Extra line after top-level
        
        # Generate children
        for child in item['children']:
            _generate_item_output(child, result, quantities, current_path)
    else:
        # Multiple instances
        for i in range(count):
            if item['children']:
                # Container with children
                if item['level'] == 2:
                    # Special case for numbered chapters
                    if 'chapter' in item['name'].lower():
                        header = '#' * item['level'] + ' ' + item['name'] + ' ' + str(i + 1)
                    else:
                        header = '#' * item['level'] + ' ' + item['name']
                else:
                    header = '#' * item['level'] + ' ' + item['name']
                
                result.append(header)
                
                # Generate children
                for child in item['children']:
                    _generate_item_output(child, result, quantities, current_path)
                
                if item['level'] == 1:
                    result.append('')  # Extra line after top-level containers
            else:
                # Simple repeated field
                header = '#' * item['level'] + ' ' + item['name'] + ' | '
                result.append(header)

def parse_worksheet_content(worksheet_content: str, section_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Parse generated worksheet content and extract sections.
    
    Args:
        worksheet_content: Generated worksheet markdown string
        section_name: Optional section name to extract only that section
    
    Returns:
        Dictionary containing parsed sections and their content
        If section_name is provided, returns only that section's data
        Format: {
            'section_name': {
                'title': 'Section Title',
                'content': 'Full content including headers and text',
                'fields': {
                    'field_name': 'field_content',
                    ...
                }
            }
        }
    """
    lines = worksheet_content.strip().split('\n')
    sections = {}
    current_section = None
    current_content = []
    current_field = None
    current_field_content = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for section header (H1 followed by ---)
        if line.startswith('# ') and i + 1 < len(lines) and lines[i + 1].strip() == '---':
            # Save previous section if exists
            if current_section:
                _finalize_section(sections, current_section, current_content, current_field, current_field_content)
            
            # Start new section
            section_title = line[2:].strip()
            current_section = {
                'title': section_title,
                'content': [],
                'fields': {}
            }
            current_content = [line, lines[i + 1]]  # Include the header and separator
            current_field = None
            current_field_content = []
            i += 2  # Skip the --- line
            continue
        
        # Check for field headers (any level # ending with |)
        if line.startswith('#') and line.endswith('|'):
            # Save previous field if exists
            if current_field and current_section:
                field_content = '\n'.join(current_field_content).strip()
                current_section['fields'][current_field] = field_content
            
            # Start new field
            header_match = re.match(r'^(#+)\s*(.+?)\s*\|\s*(.*)$', line)
            if header_match:
                field_name = header_match.group(2).strip()
                current_field = field_name
                current_field_content = []
                current_content.append(line)
        
        # Check for regular headers (structure headers without |)
        elif line.startswith('#'):
            # Save previous field if exists
            if current_field and current_section:
                field_content = '\n'.join(current_field_content).strip()
                current_section['fields'][current_field] = field_content
                current_field = None
                current_field_content = []
            
            current_content.append(line)
        
        # Regular content line
        else:
            current_content.append(line)
            if current_field:
                current_field_content.append(line)
        
        i += 1
    
    # Finalize last section
    if current_section:
        _finalize_section(sections, current_section, current_content, current_field, current_field_content)
    
    # Return specific section or all sections
    if section_name:
        return sections.get(section_name, {})
    return sections

def _finalize_section(sections: Dict[str, Any], current_section: Dict[str, Any], 
                     current_content: List[str], current_field: Optional[str], 
                     current_field_content: List[str]) -> None:
    """Helper function to finalize a section's data."""
    # Save last field if exists
    if current_field:
        field_content = '\n'.join(current_field_content).strip()
        current_section['fields'][current_field] = field_content
    
    # Save full content
    current_section['content'] = '\n'.join(current_content)
    
    # Store section
    sections[current_section['title']] = current_section

def get_section_content(worksheet_content: str, section_name: str) -> str:
    """
    Convenience function to get just the content of a specific section.
    
    Args:
        worksheet_content: Generated worksheet markdown string
        section_name: Name of the section to extract
    
    Returns:
        Full content of the section as a string, or empty string if not found
    """
    section_data = parse_worksheet_content(worksheet_content, section_name)
    return section_data.get('content', '')

def get_section_fields(worksheet_content: str, section_name: str) -> Dict[str, str]:
    """
    Convenience function to get just the fields of a specific section.
    
    Args:
        worksheet_content: Generated worksheet markdown string
        section_name: Name of the section to extract
    
    Returns:
        Dictionary of field names to their content
    """
    section_data = parse_worksheet_content(worksheet_content, section_name)
    return section_data.get('fields', {})
