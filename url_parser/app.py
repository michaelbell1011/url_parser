import streamlit as st
import pandas as pd
import requests
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_url(url):
    """Parse URL into its components"""
    try:
        parsed = urlparse(url)
        components = {
            'Scheme': parsed.scheme,
            'Netloc': parsed.netloc,
            'Path': parsed.path,
            'Params': parsed.params,
            'Query': parsed.query,
            'Fragment': parsed.fragment
        }
        return components
    except Exception as e:
        st.error(f"Error parsing URL: {e}")
        return None

def check_url_status(url):
    """Check the HTTP status of a URL"""
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        return {
            'status_code': response.status_code,
            'status_text': response.reason,
            'final_url': response.url,
            'redirected': response.url != url,
            'content_type': response.headers.get('content-type', 'Unknown'),
            'content_length': len(response.content) if response.content else 0
        }
    except requests.exceptions.Timeout:
        return {'status_code': 'Timeout', 'status_text': 'Request timed out', 'error': True}
    except requests.exceptions.ConnectionError:
        return {'status_code': 'Connection Error', 'status_text': 'Could not connect', 'error': True}
    except requests.exceptions.RequestException as e:
        return {'status_code': 'Error', 'status_text': str(e), 'error': True}

def reconstruct_url(components):
    """Reconstruct URL from components"""
    try:
        # Convert query string back to proper format
        query = components.get('Query', '')
        if query and '=' in query:
            # If it looks like a query string, keep it as is
            pass
        else:
            # If it's empty or malformed, make it empty
            query = ''
        
        reconstructed = urlunparse((
            components.get('Scheme', ''),
            components.get('Netloc', ''),
            components.get('Path', ''),
            components.get('Params', ''),
            query,
            components.get('Fragment', '')
        ))
        return reconstructed
    except Exception as e:
        st.error(f"Error reconstructing URL: {e}")
        return None

def main():
    st.set_page_config(page_title="URL Parser & Status Checker", page_icon="🔗", layout="wide")
    
    st.title("🔗 URL Parser & Status Checker")
    st.markdown("Enter a URL to parse its components and check its status")
    
    # # Debug section
    # with st.expander("🔧 Debug & Logs"):
    #     st.write("**Current Session State:**")
    #     for key, value in st.session_state.items():
    #         st.write(f"- {key}: {value}")
        
    #     st.write("**Browser Info:**")
    #     st.write(f"- User Agent: {st.get_option('browser.gatherUsageStats')}")
        
    #     # Check if we're running locally
    #     st.write("**Server Info:**")
    #     st.write(f"- Running locally: {st.get_option('server.headless')}")
    #     st.write(f"- Server address: {st.get_option('server.address')}")
    #     st.write(f"- Server port: {st.get_option('server.port')}")
    
    # URL input
    # Use rebuild URL if available, otherwise use empty string
    if st.session_state.get('rebuild_url'):
        url_input = st.text_input(
            "Enter URL:",
            value=st.session_state.rebuild_url,
            placeholder="https://example.com/path?param=value#fragment",
            help="Enter a complete URL including protocol (http:// or https://)"
        )
        # Clear the rebuild URL after using it
        st.session_state.rebuild_url = None
    else:
        url_input = st.text_input(
            "Enter URL:",
            placeholder="https://example.com/path?param=value#fragment",
            help="Enter a complete URL including protocol (http:// or https://)"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        parse_button = st.button("🔍 Parse", type="primary", use_container_width=True)
    
    with col2:
        # Go button - will be a link button if URL is available
        if url_input:
            # Use the reconstructed URL if components have been edited, otherwise use original
            target_url = url_input
            if st.session_state.url_components:
                reconstructed = reconstruct_url(st.session_state.url_components)
                if reconstructed:
                    target_url = reconstructed
            
            go_button = st.link_button("🚀 Go", target_url, use_container_width=True)
        else:
            go_button = st.button("🚀 Go", disabled=True, use_container_width=True)
    
    # Initialize session state
    if 'url_components' not in st.session_state:
        st.session_state.url_components = None
    if 'url_status' not in st.session_state:
        st.session_state.url_status = None
    if 'original_url' not in st.session_state:
        st.session_state.original_url = None
    if 'target_url' not in st.session_state:
        st.session_state.target_url = None
    if 'rebuild_url' not in st.session_state:
        st.session_state.rebuild_url = None
    
    # Parse button functionality
    if parse_button and url_input:
        with st.spinner("Parsing URL..."):
            components = parse_url(url_input)
            if components:
                st.session_state.url_components = components
                st.session_state.original_url = url_input
                st.success("URL parsed successfully!")
    
    # Check URL status when URL is entered (for status display)
    if url_input and not st.session_state.get('url_status'):
        # Use the reconstructed URL if components have been edited, otherwise use original
        target_url = url_input
        if st.session_state.url_components:
            reconstructed = reconstruct_url(st.session_state.url_components)
            if reconstructed:
                target_url = reconstructed
        
        # Check status in background
        with st.spinner("Checking URL status..."):
            status_info = check_url_status(target_url)
            st.session_state.url_status = status_info
            st.session_state.original_url = target_url
            logger.info(f"Status check completed: {status_info.get('status_code', 'Unknown')}")
    
    # Show current URL being used
    if url_input:
        current_url = url_input
        if st.session_state.url_components:
            reconstructed = reconstruct_url(st.session_state.url_components)
            if reconstructed:
                current_url = reconstructed
        
        st.info(f"🌐 **Current URL:** {current_url}")
    
    # Display URL components in editable table
    if st.session_state.url_components:
        st.subheader("📋 URL Components")
        
        # Create DataFrame for editing
        df = pd.DataFrame(list(st.session_state.url_components.items()), 
                         columns=['Component', 'Value'])
        
        # Display editable table
        edited_df = st.data_editor(
            df,
            column_config={
                "Component": st.column_config.TextColumn(
                    "Component",
                    help="URL component name",
                    disabled=True
                ),
                "Value": st.column_config.TextColumn(
                    "Value",
                    help="URL component value (editable)"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Update session state with edited values
        if not edited_df.equals(df):
            st.session_state.url_components = dict(zip(edited_df['Component'], edited_df['Value']))
        
        # Show reconstructed URL
        reconstructed = reconstruct_url(st.session_state.url_components)
        if reconstructed:
            # st.subheader("🔗 Reconstructed URL")
            # st.code(reconstructed, language="text")
            
            # Button to rebuild URL in input box
            if st.button("🔧 Rebuild URL"):
                # Store the reconstructed URL and trigger a rerun
                st.session_state.rebuild_url = reconstructed
                st.rerun()
    
    # Display URL status information
    if st.session_state.url_status:
        st.subheader("📊 URL Status Information")
        
        status_info = st.session_state.url_status
        
        if not status_info.get('error', False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Status Code", status_info['status_code'])
                st.metric("Status Text", status_info['status_text'])
            
            with col2:
                st.metric("Content Type", status_info.get('content_type', 'Unknown'))
                st.metric("Content Length", f"{status_info.get('content_length', 0):,} bytes")
            
            with col3:
                st.metric("Redirected", "Yes" if status_info.get('redirected', False) else "No")
                if status_info.get('final_url'):
                    st.text("Final URL:")
                    st.code(status_info['final_url'], language="text")
        else:
            st.error(f"❌ {status_info['status_text']}")
    
    # Instructions
    with st.expander("ℹ️ How to use this app"):
        st.markdown("""
        **Parse Button:**
        - Breaks down the URL into its components (scheme, domain, path, etc.)
        - Displays components in an editable table
        - Shows the reconstructed URL after editing
        
        **Go Button:**
        - Opens the URL (with any revisions) directly in a new browser tab
        - Automatically uses the reconstructed URL if components have been edited
        - Also checks the HTTP status and shows response details
        - Handles timeouts and connection errors gracefully
        
        **Features:**
        - Edit URL components in the table to modify the URL
        - Use "Rebuild URL" to populate the reconstructed URL back into the input box
        - View detailed status information including redirects
        - Responsive design that works on different screen sizes
        """)

if __name__ == "__main__":
    main()
