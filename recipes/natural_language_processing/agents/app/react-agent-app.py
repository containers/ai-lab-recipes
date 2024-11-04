import os
from typing import Dict, List
import requests
import time
import json
import streamlit as st
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from typing import Any, List, Dict, Union

# Load env file
load_dotenv()

# Model service
model_service = os.getenv("MODEL_ENDPOINT", "http://localhost:8001")
model_service = f"{model_service}/v1"

# Spotify API Configuration
SPOTIFY_BASE_URL = "https://api.spotify.com/v1"

class SpotifyAPI:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        
        # If not in .env, access it through UI
        if not self.client_id or not self.client_secret:
            if hasattr(st.session_state, 'spotify_client_id') and hasattr(st.session_state, 'spotify_client_secret'):
                self.client_id = st.session_state.spotify_client_id
                self.client_secret = st.session_state.spotify_client_secret
            
        if not self.client_id or not self.client_secret:
            raise ValueError("Spotify credentials not found. Please provide them in the sidebar.")
            
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        """Get Spotify access token using client credentials flow"""
        auth_url = "https://accounts.spotify.com/api/token"
        auth_response = requests.post(
            auth_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
        )
        
        if auth_response.status_code != 200:
            raise Exception("Failed to get access token")
            
        return auth_response.json()["access_token"]

    def search_playlists(self, query: str, limit: int = 5) -> Dict:
        """Search for playlists using Spotify API"""
        enhanced_query = f"{query} playlist top popular"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        params = {
           "q": enhanced_query,
            "type": "playlist",
            "limit": limit,
            "market": "US"
        }
        
        response = requests.get(
            f"{SPOTIFY_BASE_URL}/search",
            headers=headers,
            params=params
        )
        
        if response.status_code != 200:
            raise Exception(f"Search failed: {response.json().get('error', {}).get('message')}")
            
        return response.json()
    
    def get_trending_tracks(self, location: str = None, limit: int = 10) -> Dict:
        """Get trending tracks for a specific location"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        #include location in query
        query = f"top charts popular {location}" if location else "top charts"

        params = {
            "q": query,
            "type": "track",
            "limit": limit,
            "market": "US",
            "offset": 0,
            "include_external": "audio"
        }
        
        response = requests.get(
            f"{SPOTIFY_BASE_URL}/search",
            headers=headers,
            params=params
        )
        
        if response.status_code != 200:
            raise Exception(f"Search failed: {response.json().get('error', {}).get('message')}")
            
        return response.json()

class SpotifySearchTool(BaseTool):
    name: str = "spotify_search"
    description: str = """
    Search for playlists on Spotify.
    Input should be a search query string.
    The tool will return relevant playlists with their details.
    """
    spotify: Any = None

    def __init__(self) -> None:
        super().__init__()
        self.spotify = SpotifyAPI()
    
    def _run(self, query: str) -> List[Dict]:
        try:
            results = self.spotify.search_playlists(query)
            playlists = []
            for item in results['playlists']['items']:
                playlist = {
                    'name': item['name'],
                    'description': item['description'],
                    'tracks_total': item['tracks']['total'],
                    'url': item['external_urls']['spotify'],
                    'owner': item['owner']['display_name'],
                    'followers': item['followers']['total'] if 'followers' in item else 0
                }
                playlists.append(playlist)
            return playlists
        except Exception as e:
            return f"Error searching Spotify: {str(e)}"
        
class SpotifyTrendingTool(BaseTool):
    name: str = "spotify_trending"
    description: str = """
    Get trending tracks for a specific location on Spotify.
    Input should be a location string (e.g., 'Berkeley', 'Bay Area').
    Returns top trending tracks in that area.
    """
    spotify: Any = None

    def __init__(self) -> None:
        super().__init__()
        self.spotify = SpotifyAPI()
    
    def _run(self, location: str) -> List[Dict]:
        try:
            results = self.spotify.get_trending_tracks(location)
            tracks = []
            for item in results['tracks']['items']:
                track = {
                    'name': item['name'],
                    'artist': ', '.join([artist['name'] for artist in item['artists']]),
                    'album': item['album']['name'],
                    'url': item['external_urls']['spotify'],
                    'popularity': item['popularity']
                }
                tracks.append(track)
            return tracks
        except Exception as e:
            return f"Error getting trending tracks: {str(e)}"

def format_spotify_response(tool_responses: Dict) -> str:
    """Format the Spotify API responses into a readable message"""
    response = ""
    
    # Format trending tracks
    trending_tracks = tool_responses.get("trending", [])
    if isinstance(trending_tracks, list) and trending_tracks:
        response += "📊 Trending Tracks:\n"
        for i, track in enumerate(trending_tracks[:5], 1):
            response += f"{i}. {track['name']} by {track['artist']}\n"
            response += f"   - Album: {track['album']}\n"
            response += f"   - Listen: {track['url']}\n\n"
    else:
        response += "📊 No trending tracks found for this location.\n\n"
    
    # Format playlists
    playlists = tool_responses.get("playlists", [])
    if isinstance(playlists, list) and playlists:
        response += "🎵 Related Playlists:\n"
        for i, playlist in enumerate(playlists[:3], 1):
            response += f"{i}. {playlist['name']}\n"
            response += f"   - Tracks: {playlist['tracks_total']}\n"
            response += f"   - Description: {playlist['description']}\n"
            response += f"   - Listen: {playlist['url']}\n\n"
    else:
        response += "No related playlists found.\n"
    
    return response

# Model service check
@st.cache_resource(show_spinner=False)
def checking_model_service():
    start = time.time()
    print("Checking Model Service Availability...")
    ready = False
    while not ready:
        try:
            request_cpp = requests.get(f'{model_service}/models')
            request_ollama = requests.get(f'{model_service[:-2]}api/tags')
            if request_cpp.status_code == 200:
                server = "Llamacpp_Python"
                ready = True
            elif request_ollama.status_code == 200:
                server = "Ollama"
                ready = True        
        except:
            pass
        time.sleep(1)
    print(f"{server} Model Service Available")
    print(f"Time taken: {time.time()-start} seconds")
    return server

def get_models():
    try:
        response = requests.get(f"{model_service[:-2]}api/tags")
        return [i["name"].split(":")[0] for i in json.loads(response.content)["models"]]
    except:
        return None

# ReAct prompt template
REACT_PROMPT = """You are a helpful assistant that can search for music on Spotify.
You have access to the following tools:

{tools}

Use the following format in your internal processing:
Thought: First interpret if the user's input is a casual greeting or an actual search query. 
If it seems like a greeting, respond conversationally and suggest some current trending tracks.
If it's a search query, use it directly.

Action: tool_name (either spotify_search or spotify_trending)
Action Input: input to the tool
Observation: tool's response

Final Answer: If the input was conversational, start with a greeting before showing the music results.
Then provide results in this format:

📊 Trending Tracks:
[formatted tracks...]

🎵 Related Playlists:
[formatted playlists...]
"""

# Create ReAct Agent function
def create_react_agent(model_name: str):
    llm = ChatOpenAI(
        base_url=model_service,
        api_key="sk-no-key-required",
        model=model_name,
        streaming=True
    )
    
    # Create both tools
    playlist_tool = SpotifySearchTool()
    trending_tool = SpotifyTrendingTool()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", REACT_PROMPT),
        ("human", "{input}")
    ])
    
    chain = prompt | llm
    
    return chain, [playlist_tool, trending_tool]

#Streamlit
st.title("🎵 Spotify Playlist Explorer")

if "spotify_credentials_set" not in st.session_state:
    st.session_state.spotify_credentials_set = False

# Spotify Credentials Management in Sidebar
with st.sidebar:
    st.markdown("### Spotify Credentials")
    
    # Check if credentials exist in environment variables
    env_credentials_exist = bool(os.getenv("SPOTIFY_CLIENT_ID")) and bool(os.getenv("SPOTIFY_CLIENT_SECRET"))
    
    if not env_credentials_exist:
        st.warning("Spotify credentials not found in environment variables.")
        
        # Initialize session state for credentials
        if "spotify_client_id" not in st.session_state:
            st.session_state.spotify_client_id = ""
        if "spotify_client_secret" not in st.session_state:
            st.session_state.spotify_client_secret = ""
        
        # Input fields for credentials
        client_id = st.text_input(
            "Enter Spotify Client ID",
            value=st.session_state.spotify_client_id,
            type="password"
        )
        client_secret = st.text_input(
            "Enter Spotify Client Secret",
            value=st.session_state.spotify_client_secret,
            type="password"
        )
        
        if st.button("Save Credentials"):
            st.session_state.spotify_client_id = client_id
            st.session_state.spotify_client_secret = client_secret
            st.session_state.spotify_credentials_set = True
            st.success("Credentials saved!")
            st.rerun()  
    else:
        st.success("Using credentials from environment variables")
        st.session_state.spotify_credentials_set = True

# Check if credentials are available before proceeding
credentials_available = env_credentials_exist or st.session_state.spotify_credentials_set

if not credentials_available:
    st.error("Please provide Spotify credentials in the sidebar to continue.")
else:
    
    with st.spinner("Checking Model Service Availability..."):
        server = checking_model_service()

    model_name = os.getenv("MODEL_NAME", "")
    if server == "Ollama":
        with st.sidebar:
            model_name = st.radio(
                label="Select Model",
                options=get_models()
            )

    try:
        agent, tools = create_react_agent(model_name)
        playlist_tool, trending_tool = tools

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("What kind of playlists are you looking for?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                try:
                    tool_responses = {
                        "playlists": playlist_tool._run(prompt),
                        "trending": trending_tool._run(prompt)
                    }
                    
                    agent_response = agent.invoke({
                        "input": prompt,
                        "tools": [tool.description for tool in tools],
                        "query": prompt,
                        "observation": tool_responses,
                        "answer": "Based on the search results, here's what I found:"
                    })
                    
                    with st.expander("See thinking process"):
                        st.markdown(agent_response.content)
                    
                    formatted_response = format_spotify_response(tool_responses)
                    st.markdown(formatted_response)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": formatted_response
                    })
                except Exception as e:
                    error_message = f"Error processing request: {str(e)}"
                    st.error(error_message)
    except Exception as e:
        st.error(f"Error initializing Spotify API: {str(e)}")