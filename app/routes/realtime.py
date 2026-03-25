from flask import Blueprint, jsonify, flash, current_app, stream_with_context, Response, session, redirect, url_for
import requests #ek separate Python library hai jo HTTP requests bhejne ke liye use hoti hai(External HTTP client library)
#but request --> flask ka object hai jo client se aane wale request ko handle karta hai
import time

realtime_bp = Blueprint('realtime', __name__) #Creating a Blueprint for realtime routes

#------------------REALTIME DATA STREAM ROUTE-----------------------------
@realtime_bp.route('/realtime-aqi/<city>', methods=['GET'])

def realime_aqi(city):

    # If user already logged in, redirect to prediction page
    if 'user_id' not in session:
        flash('Please log in to access real-time AQI data.', 'warning')
        return redirect(url_for('auth.login'))

    """Route to stream real-time AQI data for a specified city using server-sent events (SSE) protocol."""
    API_KEY = current_app.config['AQI_API_KEY']
    AQI_API_URL = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"

    # Function to fetch AQI data and yield it for SSE
    def generate_aqi_data():
        """Generate real-time AQI data for streaming to clients using SSE."""
        while True:
            try:
                response = requests.get(AQI_API_URL) #Fetching data from AQI API
                data = response.json() #Parsing JSON response

                if data['status'] == 'ok': #If data fetch is successful
                    aqi = data['data']['aqi'] #Extracting AQI value
                    see_data = f"data: {{\"city\": \"{city}\", \"aqi\": {aqi}}}\n\n" #Formatting data for SSE 
                else: #If data fetch fails
                    see_data = f"data: {{\"error\": \"Could not fetch AQI data for {city}.\"}}\n\n" #Error message for SSE
                yield see_data #Yielding data for SSE
            
            
            except Exception as e: #Handling exceptions
                yield f"data: {{\"error\": \"An error occurred: {str(e)}\"}}\n\n" #Yielding error message for SSE

            time.sleep(10) #Wait for 10 seconds before fetching new data

    return Response(stream_with_context(generate_aqi_data()), mimetype='text/event-stream') #Returning SSE response with appropriate MIME type
    """Stream real-time AQI data for the specified city.""" 
    # The route uses server-sent events (SSE) to continuously send AQI updates to the client.
    # Clients can connect to this route to receive live AQI updates every 10 seconds.