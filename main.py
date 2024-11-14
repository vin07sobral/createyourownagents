import streamlit as st
import openai
from langchain_community.llms import OpenAI
from langchain_community.llms import LlamaCpp
# from langchain import ChatOpenAI  # Commented out due to ImportError
import json
from pathlib import Path
import toml
import datetime
import pandas as pd

# Set page config
st.set_page_config(
    page_title="AI Agent Creator",
    page_icon="🤖",
    layout="wide"
)

# Initialize LM Studio connection
def init_lm_studio():
    try:
        llm = LlamaCpp(
            model_path="http://127.0.0.1:1234", # Path to your model
            temperature=0.7,
            max_tokens=2000,
            top_p=1,
            n_ctx=2048,
            verbose=True
        )
        return llm
    except Exception as e:
        st.error(f"Error connecting to LM Studio: {str(e)}")
        return None

# Add account link and sign in/sign up buttons in header
col1, col2, col3, col4 = st.columns([4,1,1,1])
with col2:
    if st.button("My Account"):
        st.session_state.current_tab = "account"
with col3:
    if st.button("Sign In"):
        st.session_state.current_tab = "signin"
with col4:
    if st.button("Sign Up"):
        st.session_state.current_tab = "signup"

# Sign In page
if hasattr(st.session_state, 'current_tab') and st.session_state.current_tab == "signin":
    st.title("Sign In")
    
    # Back button
    if st.button("Back"):
        st.session_state.current_tab = "main"
        st.experimental_set_query_params(rerun=str(datetime.datetime.now()))
        
    # Sign in form
    with st.form("signin_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign In")
        
        if submit:
            # Here you would implement actual authentication
            st.success("Successfully signed in!")
            st.session_state.current_tab = "main"
            st.experimental_set_query_params(rerun=str(datetime.datetime.now()))
            
    st.markdown("Don't have an account? [Sign Up](/?tab=signup)")

# Sign Up page
elif hasattr(st.session_state, 'current_tab') and st.session_state.current_tab == "signup":
    st.title("Sign Up")
    
    # Back button
    if st.button("Back"):
        st.session_state.current_tab = "main"
        st.experimental_set_query_params(rerun=str(datetime.datetime.now()))
        
    # Sign up form
    with st.form("signup_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")
        
        if submit:
            if password != confirm_password:
                st.error("Passwords don't match!")
            else:
                # Here you would implement actual user registration
                st.success("Successfully registered! Please sign in.")
                st.session_state.current_tab = "signin"
                st.experimental_set_query_params(rerun=str(datetime.datetime.now()))
                
    st.markdown("Already have an account? [Sign In](/?tab=signin)")

# Account tab content
elif hasattr(st.session_state, 'current_tab') and st.session_state.current_tab == "account":
    st.title("My Account")
    
    # Back to Creating button
    if st.button("Back to Creating"):
        st.session_state.current_tab = "main"
        st.experimental_set_query_params(rerun=str(datetime.datetime.now()))
    
    # User Profile Section
    st.header("Profile")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Name", value="John Doe")
        st.text_input("Email", value="john@example.com") 
    with col2:
        st.selectbox("Current Plan", ["Free", "Pro", "Enterprise"])
        if st.button("Upgrade Plan"):
            st.info("Redirecting to billing page...")

    # Usage Statistics
    st.header("Usage Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Agents", "5")
    with col2:
        st.metric("Workflows Created", "3")
    with col3:
        st.metric("Tasks Completed", "27")

    # Recent Activity
    st.header("Recent Activity")
    activity_data = pd.DataFrame({
        "Date": ["2024-01-20", "2024-01-19", "2024-01-18"],
        "Activity": ["Created new agent", "Ran workflow", "Modified agent"],
        "Details": ["Marketing Assistant", "Content Generation", "Updated parameters"]
    })
    st.dataframe(activity_data)

    if st.button("Return to Main"):
        st.session_state.current_tab = "main"
        st.experimental_set_query_params(rerun=str(datetime.datetime.now()))

else:
    # Main content
    st.title("Create Your AI Agent 🤖")

    # Predefined agent templates
    PREDEFINED_AGENTS = {
        "Marketing": [
            {
                "name": "Content Strategist",
                "role": "Content strategy and planning",
                "personality": "Creative, analytical, detail-oriented",
                "expertise": ["Writing", "Marketing", "Creative"],
                "background": "Expert in content strategy, SEO, and audience engagement",
                "tasks": "Create content calendars, develop content strategies, analyze content performance",
                "constraints": "Must follow brand guidelines and marketing objectives",
                "communication_style": "Professional",
                "temperature": 0.7
            },
            {
                "name": "Social Media Manager",
                "role": "Social media management and engagement",
                "personality": "Engaging, creative, responsive",
                "expertise": ["Marketing", "Creative", "Writing"],
                "background": "Experienced in social media platforms and community management",
                "tasks": "Create social posts, engage with audience, monitor trends",
                "constraints": "Must maintain brand voice and community guidelines",
                "communication_style": "Friendly",
                "temperature": 0.8
            }
        ],
        "Accountability": [
            {
                "name": "Project Manager",
                "role": "Project oversight and team coordination",
                "personality": "Organized, decisive, communicative",
                "expertise": ["Business", "General Knowledge"],
                "background": "Experienced in project management methodologies",
                "tasks": "Track progress, coordinate teams, manage resources",
                "constraints": "Must follow project management best practices",
                "communication_style": "Professional",
                "temperature": 0.5
            },
            {
                "name": "Quality Assurance",
                "role": "Quality control and standards compliance",
                "personality": "Detail-oriented, thorough, systematic",
                "expertise": ["Business", "Other"],
                "background": "Expert in quality assurance processes",
                "tasks": "Review deliverables, ensure quality standards, provide feedback",
                "constraints": "Must maintain strict quality standards",
                "communication_style": "Very Formal",
                "temperature": 0.3
            }
        ],
        "Software Development": [
            {
                "name": "Lead Developer",
                "role": "Technical leadership and architecture",
                "personality": "Analytical, innovative, mentoring",
                "expertise": ["Programming", "Math"],
                "background": "Senior software developer with architecture experience",
                "tasks": "Design systems, code review, technical decisions",
                "constraints": "Must follow coding standards and best practices",
                "communication_style": "Professional",
                "temperature": 0.6
            },
            {
                "name": "Frontend Developer",
                "role": "UI/UX implementation",
                "personality": "Creative, detail-oriented, user-focused",
                "expertise": ["Programming", "Creative"],
                "background": "Expert in frontend technologies and frameworks",
                "tasks": "Implement UI designs, optimize performance, ensure responsiveness",
                "constraints": "Must follow accessibility guidelines",
                "communication_style": "Casual",
                "temperature": 0.7
            }
        ]
    }

    # Framework Selection
    framework_choice = st.sidebar.selectbox(
        "Select Framework",
        ["LangChain", "CrewAI"],
        key="framework"
    )

    # LLM Selection with LM Studio option
    llm_choice = st.sidebar.selectbox(
        "Select Language Model",
        ["LM Studio", "GPT-3.5", "GPT-4", "Claude", "LLaMA"],
        key="llm"
    )

    # LM Studio specific settings
    if llm_choice == "LM Studio":
        model_path = st.sidebar.text_input("Model Path", placeholder="Enter path to your model file")
        if model_path:
            llm = init_lm_studio()
            if llm:
                st.sidebar.success("LM Studio connected successfully!")
            else:
                st.sidebar.error("Failed to connect to LM Studio")

    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Create Agent", "Manage Agents", "Link Agents", "Run Workflows", "Results"])

    with tab1:
        st.subheader("Design and customize your personal AI assistant")

        # Template Selection
        template_category = st.selectbox(
            "Select Template Category",
            ["Custom"] + list(PREDEFINED_AGENTS.keys())
        )

        if template_category != "Custom":
            template_agent = st.selectbox(
                f"Select {template_category} Agent Template",
                [agent["name"] for agent in PREDEFINED_AGENTS[template_category]]
            )
            
            # Load template data
            template_data = next(agent for agent in PREDEFINED_AGENTS[template_category] 
                               if agent["name"] == template_agent)
            
            # Add submit button for predefined templates
            if st.button("Create Predefined Agent"):
                agent_config = {
                    "name": template_data["name"],
                    "role": template_data["role"],
                    "personality": template_data["personality"],
                    "expertise": template_data["expertise"],
                    "background": template_data["background"],
                    "tasks": template_data["tasks"],
                    "constraints": template_data["constraints"],
                    "communication_style": template_data["communication_style"],
                    "temperature": template_data["temperature"],
                    "llm": llm_choice,
                    "framework": framework_choice
                }
                
                config_path = Path("agents") / f"{template_data['name'].lower().replace(' ', '_')}.json"
                config_path.parent.mkdir(exist_ok=True)
                
                with open(config_path, "w") as f:
                    json.dump(agent_config, f, indent=4)
                
                st.success(f"Predefined Agent '{template_data['name']}' created successfully!")
                
                with st.expander("View Agent Configuration"):
                    st.json(agent_config)
                    
                # Correct way to get query parameters
                query_params = st.experimental_get_query_params()

                # Access a specific parameter
                some_param = query_params.get("some_param", ["default_value"])[0]  # Use indexing to get the first value
                
        else:
            template_data = {
                "name": "",
                "role": "",
                "personality": "",
                "expertise": [],
                "background": "",
                "tasks": "",
                "constraints": "",
                "communication_style": "Professional",
                "temperature": 0.7
            }

        # Agent Configuration Form
        with st.form("agent_creator"):
            # Basic Information
            col1, col2 = st.columns(2)
            
            with col1:
                agent_name = st.text_input("Agent Name", 
                                         value=template_data["name"],
                                         placeholder="Enter a name for your agent")
                agent_role = st.text_input("Role", 
                                         value=template_data["role"],
                                         placeholder="e.g., Personal Assistant, Code Helper, etc.")
            
            with col2:
                agent_personality = st.text_area("Personality Traits", 
                                               value=template_data["personality"],
                                               placeholder="Describe your agent's personality")
                expertise_areas = st.multiselect(
                    "Areas of Expertise",
                    options=["General Knowledge", "Programming", "Writing", "Math", "Science", "Business", "Creative", "Other"],
                    default=template_data.get("expertise", [])
                )
            
            # Detailed Configuration
            st.subheader("Advanced Configuration")
            
            background = st.text_area(
                "Background Knowledge",
                value=template_data["background"],
                placeholder="Provide any specific background knowledge your agent should have"
            )
            
            tasks = st.text_area(
                "Primary Tasks",
                value=template_data["tasks"],
                placeholder="List the main tasks your agent should be able to perform"
            )
            
            constraints = st.text_area(
                "Constraints & Limitations",
                value=template_data["constraints"],
                placeholder="Define any limitations or ethical constraints"
            )
            
            # Communication Style
            communication_style = st.select_slider(
                "Communication Style",
                options=["Very Formal", "Professional", "Casual", "Friendly", "Playful"],
                value=template_data["communication_style"]
            )
            
            # Temperature/Creativity Setting
            temperature = st.slider(
                "Response Creativity",
                min_value=0.0,
                max_value=1.0,
                value=template_data["temperature"],
                help="Lower values make responses more focused and deterministic, higher values make them more creative"
            )
            
            submit_button = st.form_submit_button("Create Agent")

        # Handle form submission
        if submit_button:
            agent_config = {
                "name": agent_name,
                "role": agent_role,
                "personality": agent_personality,
                "expertise": expertise_areas,
                "background": background,
                "tasks": tasks,
                "constraints": constraints,
                "communication_style": communication_style,
                "temperature": temperature,
                "llm": llm_choice,
                "framework": framework_choice
            }
            
            # Save configuration
            config_path = Path("agents") / f"{agent_name.lower().replace(' ', '_')}.json"
            config_path.parent.mkdir(exist_ok=True)
            
            with open(config_path, "w") as f:
                json.dump(agent_config, f, indent=4)
            
            st.success(f"Agent '{agent_name}' created successfully! Configuration saved to {config_path}")
            
            # Preview
            with st.expander("View Agent Configuration"):
                st.json(agent_config)

            # Trigger a rerun by setting a query parameter
            st.experimental_set_query_params(rerun=str(datetime.datetime.now()))

    with tab2:
        st.subheader("Manage Your Agents")
        
        # Get list of existing agents
        agents_dir = Path("agents")
        agents_dir.mkdir(exist_ok=True)
        existing_agents = [f.stem for f in agents_dir.glob("*.json")]
        
        if not existing_agents:
            st.warning("No agents found. Please create some agents first.")
        else:
            # Create a table view of all agents
            agent_list = []
            for agent_name in existing_agents:
                with open(agents_dir / f"{agent_name}.json", "r") as f:
                    agent_data = json.load(f)
                    agent_list.append({
                        "Name": agent_data["name"],
                        "Role": agent_data["role"],
                        "Framework": agent_data.get("framework", "Default Framework"),
                        "LLM": agent_data.get("llm", "Default LLM")
                    })
            
            df = pd.DataFrame(agent_list)
            
            # Display each agent as a card with actions
            for idx, row in df.iterrows():
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                    
                    col1.write(f"**{row['Name']}**")
                    col2.write(row['Role'])
                    
                    if col3.button("Edit", key=f"edit_{idx}"):
                        st.session_state.editing_agent = row['Name']
                        
                    if col4.button("Delete", key=f"delete_{idx}"):
                        agent_path = agents_dir / f"{row['Name'].lower().replace(' ', '_')}.json"
                        agent_path.unlink()
                        st.success(f"Agent '{row['Name']}' deleted successfully!")
                        st.experimental_set_query_params(rerun=str(datetime.datetime.now()))
                    
                    st.markdown("---")

            # Edit form appears if an agent is selected for editing
            if hasattr(st.session_state, 'editing_agent'):
                agent_path = agents_dir / f"{st.session_state.editing_agent.lower().replace(' ', '_')}.json"
                with open(agent_path, "r") as f:
                    agent_data = json.load(f)
                
                with st.form("edit_agent"):
                    st.subheader(f"Editing Agent: {st.session_state.editing_agent}")
                    
                    # Basic Information
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        agent_name = st.text_input("Agent Name", value=agent_data["name"])
                        agent_role = st.text_input("Role", value=agent_data["role"])
                    
                    with col2:
                        agent_personality = st.text_area("Personality Traits", value=agent_data["personality"])
                        expertise_areas = st.multiselect(
                            "Areas of Expertise",
                            ["General Knowledge", "Programming", "Writing", "Math", "Science", "Business", "Creative", "Other"],
                            default=agent_data["expertise"]
                        )
                    
                    background = st.text_area("Background Knowledge", value=agent_data["background"])
                    tasks = st.text_area("Primary Tasks", value=agent_data["tasks"])
                    constraints = st.text_area("Constraints & Limitations", value=agent_data["constraints"])
                    
                    communication_style = st.select_slider(
                        "Communication Style",
                        options=["Very Formal", "Professional", "Casual", "Friendly", "Playful"],
                        value=agent_data["communication_style"]
                    )
                    
                    temperature = st.slider(
                        "Response Creativity",
                        min_value=0.0,
                        max_value=1.0,
                        value=float(agent_data["temperature"])
                    )
                    
                    update_button = st.form_submit_button("Update Agent")
                
                if update_button:
                    # Update configuration
                    updated_config = {
                        "name": agent_name,
                        "role": agent_role,
                        "personality": agent_personality,
                        "expertise": expertise_areas,
                        "background": background,
                        "tasks": tasks,
                        "constraints": constraints,
                        "communication_style": communication_style,
                        "temperature": temperature,
                        "llm": agent_data.get("llm", "Default LLM"),
                        "framework": agent_data.get("framework", "Default Framework")
                    }
                    
                    # Save updated configuration
                    with open(agent_path, "w") as f:
                        json.dump(updated_config, f, indent=4)
                    
                    st.success(f"Agent '{agent_name}' updated successfully!")
                    del st.session_state.editing_agent
                    st.experimental_rerun()

    with tab3:
        st.subheader("Link Agents in Execution Order")
        
        # Get list of existing agents
        agents_dir = Path("agents")
        agents_dir.mkdir(exist_ok=True)
        existing_agents = [f.stem for f in agents_dir.glob("*.json")]
        
        if not existing_agents:
            st.warning("No agents found. Please create some agents first.")
        else:
            st.write("Drag and drop agents to arrange them in execution order:")
            selected_agents = st.multiselect(
                "Select and Order Agents",
                existing_agents
            )
            
            if selected_agents:
                workflow_name = st.text_input("Workflow Name", placeholder="Enter a name for this workflow")
                
                # Add tools configuration section
                st.subheader("Configure Tools for Workflow")
                
                tools_config = {}
                for agent in selected_agents:
                    st.write(f"**Tools for {agent}:**")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        tool_type = st.selectbox(
                            "Tool Type",
                            ["Web Search", "Website Visit", "Research Topic", "Data Analysis", "API Call"],
                            key=f"tool_type_{agent}"
                        )
                    
                    with col2:
                        if tool_type == "Web Search":
                            search_engine = st.selectbox("Search Engine", ["Google", "Bing", "DuckDuckGo"], key=f"search_engine_{agent}")
                            search_query = st.text_input("Default Search Query", key=f"search_query_{agent}")
                            tools_config[agent] = {"type": tool_type, "engine": search_engine, "query": search_query}
                        
                        elif tool_type == "Website Visit":
                            website_url = st.text_input("Website URL", key=f"website_url_{agent}")
                            tools_config[agent] = {"type": tool_type, "url": website_url}
                        
                        elif tool_type == "Research Topic":
                            topic = st.text_input("Research Topic", key=f"topic_{agent}")
                            depth = st.slider("Research Depth", 1, 5, 3, key=f"depth_{agent}")
                            tools_config[agent] = {"type": tool_type, "topic": topic, "depth": depth}
                        
                        elif tool_type == "Data Analysis":
                            data_source = st.text_input("Data Source", key=f"data_source_{agent}")
                            analysis_type = st.selectbox("Analysis Type", ["Statistical", "Predictive", "Descriptive"], key=f"analysis_type_{agent}")
                            tools_config[agent] = {"type": tool_type, "source": data_source, "analysis": analysis_type}
                        
                        elif tool_type == "API Call":
                            api_endpoint = st.text_input("API Endpoint", key=f"api_endpoint_{agent}")
                            api_method = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE"], key=f"api_method_{agent}")
                            tools_config[agent] = {"type": tool_type, "endpoint": api_endpoint, "method": api_method}
                
                if st.button("Save Workflow"):
                    workflow_config = {
                        "name": workflow_name,
                        "agents": selected_agents,
                        "framework": framework_choice,
                        "llm": llm_choice,
                        "tools_config": tools_config,
                        "status": "Not Started",
                        "last_run": None,
                        "output": []
                    }
                    
                    workflow_path = Path("workflows") / f"{workflow_name.lower().replace(' ', '_')}.json"
                    workflow_path.parent.mkdir(exist_ok=True)
                    
                    with open(workflow_path, "w") as f:
                        json.dump(workflow_config, f, indent=4)
                    
                    st.success(f"Workflow '{workflow_name}' saved successfully!")
                    
                    with st.expander("View Workflow Configuration"):
                        st.json(workflow_config)

    with tab4:
        st.subheader("Run Workflows")
        
        # Get list of workflows
        workflows_dir = Path("workflows")
        workflows_dir.mkdir(exist_ok=True)
        workflows = list(workflows_dir.glob("*.json"))
        
        if not workflows:
            st.warning("No workflows found. Please create some workflows first.")
        else:
            # Create a table with workflow information
            workflow_data = []
            for workflow_path in workflows:
                with open(workflow_path, "r") as f:
                    workflow = json.load(f)
                    workflow_data.append({
                        "Workflow Name": workflow["name"],
                        "Status": workflow.get("status", "Not Started"), 
                        "Agents": len(workflow["agents"]),
                        "Framework": workflow["framework"],
                        "LLM": workflow.get("llm", "Unknown"),
                        "Last Run": workflow.get("last_run", "Never"),
                        "Output": workflow.get("output", [])
                    })
            
            # Display workflow table with output
            for index, row in enumerate(workflow_data):
                with st.expander(f"Workflow: {row['Workflow Name']}", expanded=True):
                    cols = st.columns([2, 1, 1, 1, 1, 2])
                    cols[0].write("**Status:**")
                    cols[0].write(row["Status"])
                    cols[1].write("**Agents:**")
                    cols[1].write(row["Agents"])
                    cols[2].write("**Framework:**")
                    cols[2].write(row["Framework"])
                    cols[3].write("**LLM:**")
                    cols[3].write(row["LLM"])
                    cols[4].write("**Last Run:**")
                    cols[4].write(row["Last Run"])
                    
                    if cols[5].button("Run", key=f"run_{index}"):
                        st.info(f"Starting workflow: {row['Workflow Name']}")
                        
                        # Simulate workflow execution
                        workflow_path = workflows_dir / f"{row['Workflow Name'].lower().replace(' ', '_')}.json"
                        with open(workflow_path, "r") as f:
                            workflow_config = json.load(f)
                        
                        # Update workflow status and add sample output
                        workflow_config["status"] = "Completed"
                        workflow_config["last_run"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Add output for each agent
                        workflow_config["output"] = []
                        for agent in workflow_config["agents"]:
                            workflow_config["output"].append({
                                "agent": agent,
                                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "result": f"Completed task for {agent}"
                            })
                        
                        with open(workflow_path, "w") as f:
                            json.dump(workflow_config, f, indent=4)
                        
                        st.success(f"Workflow '{row['Workflow Name']}' completed successfully! All agents have finished their tasks.")
                        st.experimental_set_query_params(rerun=str(datetime.datetime.now()))
                    
                    # Display agent outputs
                    if row["Output"]:
                        st.subheader("Agent Outputs")
                        for output in row["Output"]:
                            st.write(f"**{output['agent']}** ({output['timestamp']})")
                            st.write(output['result'])
                            st.markdown("---")
