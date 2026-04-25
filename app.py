import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
import json
import socket
import subprocess
import sys

# Page configuration
st.set_page_config(
    page_title="My Frontend App",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 1rem;
    }
    .network-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def get_local_ip():
    """Get the local IP address"""
    try:
        # Create a socket to get the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Data Upload", "API Tester", "Network Info", "About"]
)

# Main content
if page == "Dashboard":
    st.markdown('<div class="main-header">📊 Interactive Dashboard</div>', unsafe_allow_html=True)
    
    # Create sample data
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Users", "1,234", "12%")
    with col2:
        st.metric("Revenue", "$45,678", "8%")
    with col3:
        st.metric("Active Sessions", "567", "-3%")
    
    # Charts
    st.markdown('<div class="sub-header">Sales Trend</div>', unsafe_allow_html=True)
    
    # Sample data for chart
    df = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Sales': [12000, 15000, 18000, 16000, 22000, 25000],
        'Expenses': [8000, 9000, 11000, 10000, 13000, 14000]
    })
    
    fig = px.line(df, x='Month', y=['Sales', 'Expenses'], 
                  title="Monthly Performance",
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Bar chart
    col1, col2 = st.columns(2)
    
    with col1:
        fig2 = px.bar(df, x='Month', y='Sales', title="Sales by Month")
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        # Pie chart
        category_data = pd.DataFrame({
            'Category': ['Product A', 'Product B', 'Product C', 'Product D'],
            'Value': [35, 25, 20, 20]
        })
        fig3 = px.pie(category_data, values='Value', names='Category', title="Product Distribution")
        st.plotly_chart(fig3, use_container_width=True)
    
    # Data table
    st.markdown('<div class="sub-header">Data Overview</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

elif page == "Data Upload":
    st.markdown('<div class="main-header">📁 Data Upload & Visualization</div>', unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        st.success("File uploaded successfully!")
        
        # Show data preview
        st.markdown("### Data Preview")
        st.dataframe(df.head())
        
        # Show basic statistics
        st.markdown("### Basic Statistics")
        st.write(df.describe())
        
        # Column selection for visualization
        st.markdown("### Create Visualization")
        
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        if len(numeric_cols) >= 2:
            x_axis = st.selectbox("Select X-axis", numeric_cols)
            y_axis = st.selectbox("Select Y-axis", numeric_cols)
            
            chart_type = st.selectbox("Chart Type", ["Scatter Plot", "Line Chart", "Bar Chart"])
            
            if st.button("Generate Chart"):
                if chart_type == "Scatter Plot":
                    fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
                elif chart_type == "Line Chart":
                    fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
                else:
                    fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Need at least 2 numeric columns for visualization")
        
        # Download processed data
        st.markdown("### Download Data")
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv"
        )
    else:
        st.info("Please upload a CSV file to begin")

elif page == "API Tester":
    st.markdown('<div class="main-header">🌐 API Testing Tool</div>', unsafe_allow_html=True)
    
    # API endpoint input
    api_url = st.text_input("API Endpoint URL", "https://jsonplaceholder.typicode.com/posts/1")
    
    # HTTP method selection
    method = st.selectbox("HTTP Method", ["GET", "POST", "PUT", "DELETE"])
    
    # Headers input
    st.markdown("### Headers (JSON format)")
    headers_input = st.text_area("Headers", '{"Content-Type": "application/json"}')
    
    # Body input for POST/PUT
    body_input = None
    if method in ["POST", "PUT"]:
        st.markdown("### Request Body (JSON format)")
        body_input = st.text_area("Body", '{"title": "test", "body": "content", "userId": 1}')
    
    if st.button("Send Request", type="primary"):
        try:
            headers = json.loads(headers_input) if headers_input else {}
            
            # Make the request
            if method == "GET":
                response = requests.get(api_url, headers=headers)
            elif method == "POST":
                body = json.loads(body_input) if body_input else {}
                response = requests.post(api_url, json=body, headers=headers)
            elif method == "PUT":
                body = json.loads(body_input) if body_input else {}
                response = requests.put(api_url, json=body, headers=headers)
            else:  # DELETE
                response = requests.delete(api_url, headers=headers)
            
            # Display response
            st.markdown("### Response")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Status Code", response.status_code)
            
            with col2:
                st.metric("Response Time", f"{response.elapsed.total_seconds():.3f}s")
            
            st.markdown("### Response Body")
            
            try:
                response_json = response.json()
                st.json(response_json)
            except:
                st.text(response.text)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif page == "Network Info":
    st.markdown('<div class="main-header">🌐 Network Access Information</div>', unsafe_allow_html=True)
    
    local_ip = get_local_ip()
    
    st.markdown(f"""
    <div class="network-info">
        <h3>📡 Application is accessible at:</h3>
        <ul>
            <li><strong>Local access:</strong> <code>http://localhost:8501</code></li>
            <li><strong>Network access:</strong> <code>http://{local_ip}:8501</code></li>
            <li><strong>All interfaces:</strong> <code>http://0.0.0.0:8501</code></li>
        </ul>
        <h3>⚠️ Important Notes:</h3>
        <ul>
            <li>Make sure your firewall allows incoming connections on port 8501</li>
            <li>Other devices on the same network can access using <code>http://{local_ip}:8501</code></li>
            <li>For internet access, you'll need to configure port forwarding on your router</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Firewall instructions
    st.markdown("### 🔧 Firewall Configuration")
    
    os_name = sys.platform
    if os_name == "linux":
        st.code("""
        # For Linux (ufw):
        sudo ufw allow 8501/tcp
        
        # For Linux (firewalld):
        sudo firewall-cmd --permanent --add-port=8501/tcp
        sudo firewall-cmd --reload
        """)
    elif os_name == "darwin":  # macOS
        st.code("""
        # For macOS:
        sudo pfctl -f /etc/pf.conf
        # Or simply allow in System Preferences > Security & Privacy > Firewall
        """)
    elif os_name == "win32":  # Windows
        st.code("""
        # For Windows (run as Administrator):
        netsh advfirewall firewall add rule name="Streamlit App" dir=in action=allow protocol=TCP localport=8501
        """)
    
    # Test connection
    st.markdown("### 🔍 Test Connection from Another Device")
    st.info(f"From another device on the same network, open a browser and navigate to:\n\n`http://{local_ip}:8501`")

elif page == "About":
    st.markdown('<div class="main-header">ℹ️ About This Application</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## My Frontend Application
    
    This is a modern Python frontend application built with **Streamlit**.
    
    ### Features:
    - 📊 Interactive Dashboard with real-time metrics
    - 📁 CSV file upload and data visualization
    - 🌐 API testing tool
    - 📈 Dynamic charts using Plotly
    - 💾 Data export functionality
    - 🌍 Network-wide access support
    
    ### Technologies Used:
    - **Streamlit**: Web framework
    - **Pandas**: Data manipulation
    - **Plotly**: Interactive visualizations
    - **Requests**: API calls
    
    ### How to Run with Network Access:
    1. Install dependencies: `pip install -r requirements.txt`
    2. Run the app: `streamlit run app.py --server.address 0.0.0.0 --server.port 8501`
    3. Access from any device on your network: `http://YOUR_IP:8501`
    
    ### System Requirements:
    - Python 3.8 or higher
    - Modern web browser
    - Network connection for multi-device access
    
    ---
    Created with ❤️ using Python
    """)
    
    # Progress bar example
    st.markdown("### Application Status")
    progress_bar = st.progress(0)
    for i in range(100):
        progress_bar.progress(i + 1)
    st.success("Application is fully operational!")

# Footer
st.markdown("---")
st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")