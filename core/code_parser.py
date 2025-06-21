"""Code parsing and analysis"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Any
from core.file_system import FileSystem


class CodeParser:
    """Parse and analyze code structure"""
    
    def __init__(self):
        self.fs = FileSystem()
    
    async def analyze_structure(self, path: str, include_docstrings: bool = False) -> Dict[str, Any]:
        """Analyze code structure of a file"""
        content = await self.fs.read_file(path)
        file_ext = Path(path).suffix.lower()
        
        if file_ext == '.py':
            return await self._analyze_python(path, content, include_docstrings)
        elif file_ext in ['.js', '.jsx', '.ts', '.tsx']:
            return await self._analyze_javascript(path, content)
        else:
            return await self._analyze_generic(path, content)
    
    async def _analyze_python(self, path: str, content: str, include_docstrings: bool) -> Dict[str, Any]:
        """Analyze Python code structure"""
        structure = {
            'file': path,
            'language': 'python',
            'imports': [],
            'classes': [],
            'functions': []
        }
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        structure['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        structure['imports'].append(f"{module}.{alias.name}")
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'line': node.lineno,
                        'methods': []
                    }
                    if include_docstrings:
                        class_info['docstring'] = ast.get_docstring(node)
                    
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_info = {
                                'name': item.name,
                                'line': item.lineno
                            }
                            if include_docstrings:
                                method_info['docstring'] = ast.get_docstring(item)
                            class_info['methods'].append(method_info)
                    
                    structure['classes'].append(class_info)
                elif isinstance(node, ast.FunctionDef) and not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree)):
                    func_info = {
                        'name': node.name,
                        'line': node.lineno
                    }
                    if include_docstrings:
                        func_info['docstring'] = ast.get_docstring(node)
                    structure['functions'].append(func_info)
        except:
            pass
        
        return structure
    
    async def _analyze_javascript(self, path: str, content: str) -> Dict[str, Any]:
        """Analyze JavaScript/TypeScript code structure"""
        structure = {
            'file': path,
            'language': 'javascript',
            'imports': [],
            'classes': [],
            'functions': []
        }
        
        # Simple regex-based parsing for JavaScript
        import_pattern = r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]'
        class_pattern = r'class\s+(\w+)'
        function_pattern = r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s+)?\()'
        
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            # Find imports
            import_match = re.search(import_pattern, line)
            if import_match:
                structure['imports'].append(import_match.group(1))
            
            # Find classes
            class_match = re.search(class_pattern, line)
            if class_match:
                structure['classes'].append({
                    'name': class_match.group(1),
                    'line': i
                })
            
            # Find functions
            func_match = re.search(function_pattern, line)
            if func_match:
                name = func_match.group(1) or func_match.group(2)
                if name:
                    structure['functions'].append({
                        'name': name,
                        'line': i
                    })
        
        return structure
    
    async def _analyze_generic(self, path: str, content: str) -> Dict[str, Any]:
        """Generic code analysis for unsupported languages"""
        structure = {
            'file': path,
            'language': 'unknown',
            'imports': [],
            'classes': [],
            'functions': []
        }
        
        # Basic pattern matching for common constructs
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            # Look for function-like patterns
            if re.match(r'\s*(?:def|function|func)\s+\w+', line):
                match = re.search(r'(?:def|function|func)\s+(\w+)', line)
                if match:
                    structure['functions'].append({
                        'name': match.group(1),
                        'line': i
                    })
            
            # Look for class-like patterns
            if re.match(r'\s*class\s+\w+', line):
                match = re.search(r'class\s+(\w+)', line)
                if match:
                    structure['classes'].append({
                        'name': match.group(1),
                        'line': i
                    })
        
        return structure
    
    async def find_definitions(self, path: str, symbol: str) -> List[Dict[str, Any]]:
        """Find symbol definitions in a file"""
        content = await self.fs.read_file(path)
        definitions = []
        
        lines = content.splitlines()
        for i, line in enumerate(lines, 1):
            # Look for various definition patterns
            patterns = [
                rf'(?:def|function|func)\s+{symbol}\s*\(',
                rf'class\s+{symbol}(?:\s|:|\()',
                rf'(?:const|let|var)\s+{symbol}\s*=',
                rf'{symbol}\s*=\s*(?:function|class|\()',
            ]
            
            for pattern in patterns:
                if re.search(pattern, line):
                    def_type = 'function'
                    if 'class' in pattern:
                        def_type = 'class'
                    elif 'const' in pattern or 'let' in pattern or 'var' in pattern:
                        def_type = 'variable'
                    
                    definitions.append({
                        'name': symbol,
                        'type': def_type,
                        'line': i,
                        'text': line.strip()
                    })
                    break
        
        return definitions