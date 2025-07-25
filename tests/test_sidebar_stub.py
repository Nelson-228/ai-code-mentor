import os
import pytest

def test_sidebar_html_exists():
    """Test that the sidebar HTML file exists and has the required structure"""
    html_path = os.path.join('src', 'webview', 'sidebar.html')
    
    # Check if file exists
    assert os.path.exists(html_path), f"Sidebar HTML file not found at {html_path}"
    
    # Read the file content
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for required elements
    assert '<h2>AI Insights</h2>' in content, "Missing h2 title 'AI Insights'"
    assert '<ul id="insights">' in content, "Missing insights list with id 'insights'"
    assert 'background-color: #1e1e1e' in content, "Missing dark background color"
    
    # Check for basic HTML structure
    assert '<!DOCTYPE html>' in content, "Missing DOCTYPE declaration"
    assert '<html' in content, "Missing html tag"
    assert '<head>' in content, "Missing head tag"
    assert '<body>' in content, "Missing body tag"

def test_sidebar_ts_exists():
    """Test that the sidebar TypeScript file exists"""
    ts_path = os.path.join('src', 'sidebar.ts')
    
    # Check if file exists
    assert os.path.exists(ts_path), f"Sidebar TypeScript file not found at {ts_path}"
    
    # Read the file content
    with open(ts_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for required class and method
    assert 'class SidebarProvider' in content, "Missing SidebarProvider class"
    assert 'createOrShow' in content, "Missing createOrShow method"
    assert 'aiInsights' in content, "Missing webview panel ID" 